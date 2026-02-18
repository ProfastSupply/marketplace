from . import models
import logging
from collections import defaultdict

_logger = logging.getLogger(__name__)


def post_init_hook(env):
    """
    Runs automatically after module installation.
    Computes cost and profit for all existing invoices using a product
    price cache to avoid querying the same product multiple times.
    Uses raw SQL for bulk updates for maximum speed.
    """
    _logger.info('Invoice Sales Data: Starting initial computation...')
    
    # Get all invoices to process
    invoices = env['account.move'].search([
        ('move_type', 'in', ['out_invoice', 'out_refund'])
    ])
    total = len(invoices)
    _logger.info(f'Invoice Sales Data: Found {total} invoices to compute')
    
    if not invoices:
        return
    
    # Build product price cache (query each product ONCE)
    _logger.info('Invoice Sales Data: Building product price cache...')
    all_lines = env['account.move.line'].search([
        ('move_id', 'in', invoices.ids),
        ('product_id', '!=', False)
    ])
    product_ids = all_lines.mapped('product_id').ids
    products = env['product.product'].browse(product_ids)
    
    # Cache: {product_id: standard_price}
    price_cache = {p.id: p.standard_price for p in products}
    _logger.info(f'Invoice Sales Data: Cached prices for {len(price_cache)} unique products')
    
    # Group lines by invoice for faster lookup
    lines_by_invoice = defaultdict(list)
    for line in all_lines:
        lines_by_invoice[line.move_id.id].append({
            'product_id': line.product_id.id,
            'quantity': line.quantity or 0.0
        })
    
    # Process invoices in batches and write to DB
    batch_size = 500
    for i in range(0, total, batch_size):
        batch = invoices[i:i + batch_size]
        batch_end = min(i + batch_size, total)
        _logger.info(f'Invoice Sales Data: Processing batch {i+1}-{batch_end} of {total}')
        
        # Calculate costs/profits for this batch
        updates = []
        for invoice in batch:
            cost = 0.0
            profit = 0.0
            
            # Calculate cost using cached prices (no DB queries!)
            if invoice.move_type == 'out_invoice':
                for line_data in lines_by_invoice.get(invoice.id, []):
                    product_id = line_data['product_id']
                    quantity = line_data['quantity']
                    standard_price = price_cache.get(product_id, 0.0)
                    cost += standard_price * quantity
            
            # Calculate profit
            if invoice.move_type == 'out_invoice':
                profit = invoice.amount_untaxed - cost
            elif invoice.move_type == 'out_refund':
                profit = -invoice.amount_untaxed
            
            updates.append((invoice.id, cost, profit))
        
        # Bulk SQL update for this batch
        if updates:
            env.cr.execute("""
                UPDATE account_move AS am
                SET invoice_cost = v.cost,
                    invoice_profit = v.profit,
                    write_date = (now() at time zone 'UTC'),
                    write_uid = %s
                FROM (VALUES %s) AS v(id, cost, profit)
                WHERE am.id = v.id
            """ % (
                env.uid,
                ','.join(f"({inv_id},{cost},{profit})" for inv_id, cost, profit in updates)
            ))
    
    _logger.info('Invoice Sales Data: Initial computation complete!')
    
    _logger.info('Invoice Profitability: Initial computation complete!')
    
    _logger.info('Invoice Profitability: Initial computation complete!')
