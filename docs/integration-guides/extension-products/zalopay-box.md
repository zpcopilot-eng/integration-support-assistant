# Zalopay Box Documentation

Nguồn: https://docs.zalopay.vn/docs/guides/extension-products/zalopay-box/intro

## Overview
The Zalopay Box is an intelligent payment device combining audio notifications with QR code display technology. Users can scan QR codes on the device to complete mobile payments quickly. The device is designed for placement at cashier counters and customer gathering areas to enhance the payment experience.

## Supported Features
- Static QR codes
- Dynamic QR codes
- MiniPos (keyboard-enabled variant)

## Integration Process

### Initial Setup
Merchants must provide store information in an Excel file containing:
- Store ID
- POS ID
- Store name

Zalopay then configures devices based on this information.

### Static QR Implementation
"Zalopay configures the QRCode content to display on the Zalopay Box screen." Users scan the code, enter amounts, and receive audio confirmation upon successful payment. No further merchant integration is required.

### Dynamic QR Implementation
QR codes expire after the order validity period (typically 15 minutes). The device returns to standby mode displaying the Zalopay logo after successful payment. Merchants must use the Create Order API and include `store_id` and `pos_id` in the `columninfo` field of `embed_data`.

### MiniPos Variant
This keyboard-equipped device supports both static and dynamic QR functionality. Cashiers can either enter order codes alone (static QR) or combine order codes with amounts using the Fn1 key (dynamic QR).

## Support Contact
- Hotline: 1900 545 436
- Email: op@zalopay.vn
