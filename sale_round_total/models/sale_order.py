import math
import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)

LIVE_ROUNDING_LINE_THRESHOLD = 10


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    sale_rounding_applied = fields.Boolean(
        string='Rounding Applied',
        default=False,
        copy=False,
    )

    def _get_rounding_config(self):
        """Return (increment: float, direction: str).
        direction is one of: 'up', 'nearest', 'down'
        """
        ICP = self.env['ir.config_parameter'].sudo()
        # Use float() so '1.0' and '1.00' both become 1.0 — avoids Selection
        # validation errors if the param was written by a test script or old code.
        increment = float(ICP.get_param('sale_rounding.increment', '0.05') or '0.05')
        direction = ICP.get_param('sale_rounding.direction', '')

        # Migration: fall back to old up_only param if new one not set yet
        if not direction:
            old_up_only = ICP.get_param('sale_rounding.up_only', 'True')
            direction = 'up' if old_up_only in ('True', '1', 'true') else 'nearest'

        return increment, direction

    @staticmethod
    def _calc_target(current_total, increment, direction):
        if increment <= 0:
            return current_total

        units = current_total / increment

        if direction == 'up':
            ceiled = math.ceil(units)
            # If already sitting exactly on a boundary, don't bump up
            if math.isclose(units, round(units), rel_tol=1e-9):
                ceiled = round(units)
            target = ceiled * increment

        elif direction == 'down':
            floored = math.floor(units)
            # If already sitting exactly on a boundary, don't bump down
            if math.isclose(units, round(units), rel_tol=1e-9):
                floored = round(units)
            target = floored * increment

        else:  # 'nearest'
            target = round(units) * increment

        return round(target, 10)

    @staticmethod
    def _dominant_tax_group(eligible_lines):
        groups = {}
        for line in eligible_lines:
            key = tuple(sorted(line.tax_id.ids))
            groups.setdefault(key, []).append(line)
        dominant_key = max(
            groups.keys(),
            key=lambda k: (
                len(groups[k]),
                sum(ln.price_subtotal for ln in groups[k]),
            ),
        )
        return groups[dominant_key]

    def _force_recompute(self, order):
        # Invalidate cached values FIRST so the subsequent compute methods read
        # fresh data from the write-buffer rather than returning stale cache.
        try:
            order.order_line.invalidate_recordset(
                ['price_subtotal', 'price_tax', 'price_total']
            )
            order.invalidate_recordset(
                ['amount_total', 'amount_tax', 'amount_untaxed']
            )
            order.order_line._compute_amount()
            order._compute_amounts()
        except Exception:
            # Fallback: at minimum nuke the totals cache so next read is fresh.
            order.order_line.invalidate_recordset(
                ['price_subtotal', 'price_tax', 'price_total']
            )
            order.invalidate_recordset(
                ['amount_total', 'amount_tax', 'amount_untaxed']
            )

    def _restore_rounding(self):
        for order in self:
            if not order.sale_rounding_applied:
                continue
            eligible = order.order_line.filtered(
                lambda l: not l.display_type
                and l.product_uom_qty
                and l.price_unit_before_rounding
                and not l.is_delivery
                and l.product_id.type != 'service'
            )
            for line in eligible:
                line.with_context(rounding_in_progress=True).write({
                    'price_unit': line.price_unit_before_rounding,
                    'price_unit_before_rounding': 0.0,
                })
            order.sale_rounding_applied = False

    def _apply_rounding(self):
        for order in self:
            # Never round website / eCommerce orders — the exact amount is what
            # the customer sees at checkout and what gets charged to their card.
            if order.website_id:
                if order.sale_rounding_applied:
                    order._restore_rounding()
                continue

            if order.state == 'draft':
                if order.sale_rounding_applied:
                    order._restore_rounding()
                continue

            if order.sale_rounding_applied:
                order._restore_rounding()

            # Flush + invalidate so amount_total reflects the true current state,
            # especially after _restore_rounding() writes and after new lines are
            # added to a confirmed order (ORM cache may lag behind the DB write).
            order.order_line.invalidate_recordset(
                ['price_subtotal', 'price_tax', 'price_total']
            )
            order.invalidate_recordset(
                ['amount_total', 'amount_tax', 'amount_untaxed']
            )
            order.order_line._compute_amount()
            order._compute_amounts()

            increment, direction = order._get_rounding_config()
            current_total = order.amount_total
            target = order._calc_target(current_total, increment, direction)
            delta = target - current_total

            if math.isclose(delta, 0.0, abs_tol=1e-4):
                _logger.info(
                    'Sale order %s: total %s already rounded (%s, %s increment).',
                    order.name, current_total, direction, increment,
                )
                continue

            eligible_lines = order.order_line.filtered(
                lambda l: not l.display_type
                and l.product_uom_qty
                and not l.is_delivery
                and l.product_id.type != 'service'
            )
            if not eligible_lines:
                _logger.warning('Sale order %s: no eligible lines.', order.name)
                continue

            target_lines = self._dominant_tax_group(eligible_lines)
            group_subtotal = sum(ln.price_subtotal for ln in target_lines)
            group_tax = sum(ln.price_tax for ln in target_lines)
            group_tax_rate = (
                group_tax / group_subtotal
                if group_subtotal and not math.isclose(group_subtotal, 0.0, abs_tol=1e-9)
                else 0.0
            )

            subtotal_adj = delta / (1.0 + group_tax_rate)
            n = len(target_lines)
            per_line_adj = subtotal_adj / n

            # Cache before-rounding prices before writing anything
            before_prices = {line.id: line.price_unit for line in target_lines}

            for line in target_lines:
                new_price = before_prices[line.id] + per_line_adj / line.product_uom_qty
                line.with_context(rounding_in_progress=True).write({
                    'price_unit_before_rounding': before_prices[line.id],
                    'price_unit': new_price,
                })

            # One recompute after all lines are written
            self._force_recompute(order)

            fix_line = target_lines[0]
            if n == 1 and fix_line.product_uom_qty and (1.0 + group_tax_rate) > 0:
                # Single-line order: solve directly for the exact price_unit
                # that produces the target total, bypassing iterative rounding.
                # target = price_unit * qty * (1 + tax_rate)
                # → price_unit = target / (qty * (1 + tax_rate))
                exact_price = target / (fix_line.product_uom_qty * (1.0 + group_tax_rate))
                fix_line.with_context(rounding_in_progress=True).write(
                    {'price_unit': exact_price}
                )
                self._force_recompute(order)
                _logger.debug(
                    'Sale order %s: single-line direct solve  exact_price=%.6f -> total=%.2f',
                    order.name, exact_price, order.amount_total,
                )
            else:
                # Multi-line: iterative correction for per-line tax rounding residual.
                # We must invalidate fix_line's price_unit cache before reading it each
                # iteration — otherwise we read the pre-write cached value and stack
                # corrections on top of the wrong base price.
                for attempt in range(3):
                    residual = target - order.amount_total
                    if math.isclose(residual, 0.0, abs_tol=0.005):
                        break
                    fix_unit = (residual / (1.0 + group_tax_rate)) / fix_line.product_uom_qty
                    fix_line.invalidate_recordset(['price_unit'])
                    fix_line.with_context(rounding_in_progress=True).write(
                        {'price_unit': fix_line.price_unit + fix_unit}
                    )
                    self._force_recompute(order)
                    _logger.debug(
                        'Sale order %s: correction #%d  residual=%.4f -> total=%.2f',
                        order.name, attempt + 1, residual, order.amount_total,
                    )

            final_residual = target - order.amount_total
            if not math.isclose(final_residual, 0.0, abs_tol=0.005):
                _logger.warning(
                    'Sale order %s: still %.4f off target after 3 corrections. '
                    'target=%.2f  actual=%.2f',
                    order.name, final_residual, target, order.amount_total,
                )

            order.sale_rounding_applied = True
            _logger.info(
                'Sale order %s: %s -> %s (delta %.4f, %s lines, direction=%s, tax_rate %.4f).',
                order.name,
                round(current_total, 2),
                round(order.amount_total, 2),
                delta, n, direction, group_tax_rate,
            )

    def _rounding_is_live(self):
        eligible_count = len(
            self.order_line.filtered(lambda l: not l.display_type and l.product_uom_qty)
        )
        return eligible_count < LIVE_ROUNDING_LINE_THRESHOLD

    def action_quotation_send(self):
        result = super().action_quotation_send()
        self._apply_rounding()
        return result

    def action_confirm(self):
        result = super().action_confirm()
        self._apply_rounding()
        return result

    def action_draft(self):
        result = super().action_draft()
        self._restore_rounding()
        return result
