# Stock Return Max Quantities

One-click return all delivered quantities.

## The Problem

When returning an entire delivery, you have to manually set each line's quantity to the maximum. This is tedious for deliveries with many lines.

## The Solution

This module adds a "Return Max Quantities" button that:
1. Sets all line quantities to their maximum (delivered qty)
2. Processes the return immediately
3. Opens the new return picking

## Features

- ✅ One-click full returns
- ✅ Properly redirects to the new return picking
- ✅ Keeps the original "Return Inputted Quantities" button for partial returns

## Installation

1. Download or clone this module into your Odoo addons directory
2. Update the apps list in Odoo (Settings → Apps → Update Apps List)
3. Search for "Stock Return Max Quantities" and install

## Requirements

- Odoo 18.0
- Dependencies: `stock`

## Usage

1. Go to a completed delivery (Inventory → Deliveries)
2. Click "Return" button
3. In the return wizard, click "Return Max Quantities"
4. The return is created and opened automatically

## License

LGPL-3

## Author

**ProFast Supply**  
Website: [https://profast.supply](https://profast.supply)

## Support

For issues or feature requests, contact us at it@profast.supply
