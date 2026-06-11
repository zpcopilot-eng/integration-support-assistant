# Dynamic QR Code Integration Guide

Nguồn: https://docs.zalopay.vn/docs/guides/payment-acceptance/qrcode/dynamic-qr

## Overview

Zalopay's Dynamic QR Code is a payment integration designed for merchants with engineering capabilities. As noted in the documentation, it's "suitable for merchants with engineering capabilities to embed Zalopay into their existing applications."

## Key Prerequisites

Before integrating, merchants must:
- Register and obtain `app_id` and `mac_key` credentials
- Understand the CreateOrder and QueryOrder APIs
- Comprehend callback mechanisms and secure data transmission protocols

## Payment Flow Overview

The process follows these steps:

1. Customer clicks payment button on the merchant's application
2. Backend calls CreateOrder API to generate a payment order
3. Frontend displays QR code to customer
4. Customer scans with Zalopay app and confirms payment
5. Backend receives payment notification via callback
6. Confirmation message displays to customer

## Integration Steps

### Creating an Order

The backend must submit payment details via CreateOrder API. The request includes parameters like `app_id`, `app_trans_id`, amount, and a cryptographic signature (`mac`) for security verification.

### Presenting the QR Code

Once Zalopay processes the order, merchants receive an `order_url` which must be converted to a QR code using any compatible QR code generator library.

### Handling Callbacks

When payment completes, Zalopay sends a POST callback. Critical security requirement: "verify that the request actually came from Zalopay by using the callback key to validate the callback's data."

### Order Status Verification

Orders expire after 15 minutes. The documentation recommends actively querying payment status using the QueryOrder API rather than relying solely on callbacks.

## Resources

- Live demo and example implementations available on GitHub
- Complete working example using NextJs provided by Zalopay
