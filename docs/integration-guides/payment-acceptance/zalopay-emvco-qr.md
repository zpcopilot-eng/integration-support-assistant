# Zalopay QR Multi-Function Payment Solution

Nguồn: https://docs.zalopay.vn/docs/guides/payment-acceptance/zalopay-emvco-qr/intro

## Overview

Zalopay QR multi-function is a payment system enabling transactions through either the ZaloPay app or banking applications using a single QR code integrated with VietQR technology. The solution helps merchants optimize payment acceptance while providing customers with a convenient, secure payment method.

## Key Benefits

**For Businesses:**
- Eliminates need for multiple QR code management systems, reducing infrastructure costs
- Provides integrated management with automatic notifications and reconciliation support
- Enables merchants to accept diverse payment methods, expanding customer reach
- Delivers seamless customer experience

**For Customers:**
- "Make payments with just one QR code across multiple applications"
- Complies with ISO/IEC 27001 security standards

## Deployment Options

### Offline Business
- **Without POS:** Static QR code placed at counter
- **With POS:** Technical API integration to display QR directly on POS machines

### Online Business
- **Desktop:** API integration to generate dynamic QR codes on merchant websites
- **Mobile:** API integration with redirect to Zalopay payment page

## Integration Steps

1. Display Zalopay QR payment option at checkout
2. Send order creation request with parameters specifying VietQR preference
3. Initiate payment via: Zalopay Gateway redirect, QR code display, or bank app deeplink
4. Process payment results through callbacks or order status queries

The system handles transaction notifications automatically and supports active order status polling to ensure reliable payment confirmation.
