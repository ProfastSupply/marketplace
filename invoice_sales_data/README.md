# Invoice Profitability

Track cost, revenue, and profit directly on customer invoices and credit notes.

## Features

- **Automatic Cost Calculation**: Computes COGS from product standard prices × quantities
- **Real-time Profit Tracking**: Updates automatically when invoice lines change (within 7 days)
- **Historical Accuracy**: Freezes values after 7 days to prevent retroactive changes
- **Admin-Only Visibility**: Fields visible only to Billing Administrators
- **List View Summary**: Profit column with total sum in invoice list
- **No Manual Buttons**: Fully automatic, no intervention needed

## How It Works

### Cost Calculation

For **Customer Invoices** (`out_invoice`):
```
Cost = Σ (product.standard_price × quantity) for each invoice line
```

For **Credit Notes** (`out_refund`):
- Cost is NOT tracked (treated as pure revenue reduction)
- If you want to track returned goods cost, uncomment the logic in `account_move.py`

### Profit Calculation

For **Customer Invoices**:
```
Profit = amount_untaxed - Cost
```

For **Credit Notes**:
```
Profit = -amount_untaxed
```
(Negative value shows the revenue loss from the refund)

### Historical Freezing (7-Day Window)

**The module uses a date-based freeze to preserve historical accuracy:**

- **New invoices** (invoice_date within last 7 days OR not set):
  - ✅ Recalculates automatically when lines change
  - ✅ Uses current product standard_price
  
- **Old invoices** (invoice_date older than 7 days):
  - ❌ Does NOT recalculate
  - ❌ Not affected by product cost changes
  - ✅ Preserves historical cost/profit data

**Why 7 days?**
- Allows corrections during the normal invoice review period
- Prevents accountants from accidentally changing historical data when fixing old invoices
- Even if an old invoice is reset to draft, cost/profit stay frozen

**Edge case:** If someone deletes and recreates an old invoice, it will get new cost/profit based on current prices (unavoidable, as create_date changes).

## Installation

1. Copy this module to your Odoo addons directory
2. Update the app list
3. Install "Invoice Profitability"

## Usage

### Viewing Profit Data

1. Open any customer invoice or credit note
2. Go to the **Other Info** tab
3. Find the **Profitability** section showing:
   - Cost (total COGS)
   - Profit (revenue - cost)

### List View

In the invoice list (`Invoicing > Customers > Invoices`):
- **Profit** column is available (optional, shown by default)
- Footer shows **Total Profit** sum across all visible invoices

## Technical Details

### Why Date-Based Freezing Instead of State?

**Problem with state-based:** If an accountant needs to fix an old invoice, they reset it to draft. With state-based freezing, the cost/profit would recalculate using current product prices, destroying historical accuracy.

**Solution with invoice_date:** The freeze is based on `invoice_date`, not `state`. An accountant can reset a 2-year-old invoice to draft, edit it, and re-post it without affecting the cost/profit values.

### Field Dependencies

The computation triggers when any of these change **on invoices within the 7-day window**:
- `invoice_line_ids.product_id` - Product selection
- `invoice_line_ids.quantity` - Quantity
- `amount_untaxed` - Invoice total
- `move_type` - Invoice type
- `invoice_date` - Date determines if frozen

**Notable exclusion:** `product_id.standard_price` is NOT in the dependency list. This prevents recalculation when product costs change, protecting historical data.

### Performance

- Fields are **stored** in the database (fast reads)
- Only invoices within the 7-day window recalculate
- Old invoices (99%+ of your database) are never touched
- No scheduled actions or background jobs

## Permissions

All profitability fields require the **Billing Administrator** role (`account.group_account_manager`).

Regular users will not see these fields even if they can view invoices.

## Limitations

- Only applies to customer invoices and credit notes
- Does not track vendor bills (can be added if needed)
- Cost reflects `standard_price` at computation time
- 7-day freeze is hardcoded (can be changed in code if needed)

## Customization

### Change the Freeze Period

Edit `models/account_move.py` and change:
```python
cutoff_date = today - timedelta(days=7)  # Change 7 to whatever you want
```

### Track Credit Note Costs

If you want to track the cost of returned goods in credit notes:

```python
elif record.move_type == 'out_refund':
    line_cost = (product.standard_price or 0.0) * quantity
    cost += line_cost
```

Then adjust profit calculation:
```python
elif record.move_type == 'out_refund':
    profit = -(record.amount_untaxed - cost)
```

### Add Fields to Other Invoice Types

Change the `invisible` domain in the view:
```xml
invisible="move_type not in ('out_invoice', 'out_refund', 'in_invoice')"
```

And update the compute method to handle additional types.

## Migration from Automation

If you have existing invoices with `x_studio_cost` and `x_studio_profit` from an automation:

```python
# One-time script
invoices = env['account.move'].search([
    ('x_studio_cost', '!=', False),
    ('move_type', 'in', ['out_invoice', 'out_refund'])
])

for invoice in invoices:
    invoice.write({
        'invoice_cost': invoice.x_studio_cost,
        'invoice_profit': invoice.x_studio_profit,
    })
```

The computed field will respect the 7-day freeze, so only recent invoices will recalculate.

## Support

For issues or questions, contact ProFast Supply at https://profast.supply

## License

LGPL-3
