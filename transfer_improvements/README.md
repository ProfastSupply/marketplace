# Transfer & Invoice Improvements

Enhances delivery orders and invoices with useful workflow features.

## Delivery Order Features

- ✅ **Create Invoice button** directly on outgoing deliveries
- ✅ **Sales Order link** shown and clickable
- ✅ **Purchase Order link** auto-detected for incoming transfers
- ✅ **Improved return slip** shows "Return of" instead of "Order"
- ✅ Hides redundant "Source Document" field

## Invoice Features

- ✅ **Regenerate Invoice Lines** button on draft invoices
- ✅ Rebuilds invoice from delivered quantities on the sale order
- ✅ **Consolidates multiple draft invoices** for the same order
- ✅ Auto-switches between invoice/credit note based on total amount

## Installation

1. Download or clone this module into your Odoo addons directory
2. Update the apps list in Odoo (Settings → Apps → Update Apps List)
3. Search for "Stock Picking & Invoice Improvements" and install

## Requirements

- Odoo 18.0
- Dependencies: `stock`, `sale_stock`, `purchase_stock`, `account`

## Usage

### Create Invoice from Delivery
1. Go to Inventory → Deliveries
2. Open a completed outgoing delivery
3. Click the "Create Invoice" button in the header

### Regenerate Invoice Lines
1. Open a draft customer invoice or credit note
2. Click "Regenerate Lines" button
3. Confirms and rebuilds lines from delivered quantities

### Multiple Draft Invoices
If multiple draft invoices exist for the same sale order, the regenerate action will:
1. Keep the oldest invoice
2. Delete the others
3. Rebuild lines on the remaining invoice

## License

LGPL-3

## Author

**ProFast Supply**  
Website: [https://profast.supply](https://profast.supply)

## Support

For issues or feature requests, contact us at it@profast.supply
