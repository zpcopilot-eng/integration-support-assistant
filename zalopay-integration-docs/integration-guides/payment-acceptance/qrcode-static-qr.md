# Static QR Code Documentation

Nguồn: https://docs.zalopay.vn/docs/guides/payment-acceptance/qrcode/static-qr

## Overview
The Static QR Code is a straightforward payment solution requiring no coding. Customers open the Zalopay App, scan a merchant's QR code (either printed or displayed), enter the transaction amount, and complete payment. The merchant then receives and confirms the funds.

## Key Features

**Access Requirements:**
- Login capability to Merchant Portal
- Sandbox environment: https://sbmc.zalopay.vn/home
- Production environment: https://mc.zalopay.vn/home
- Pre-configured branch/shop/counter structure

## Implementation Process

### Steps to Generate a QR Code

1. Navigate to the Counter Management section in your Merchant Portal
2. Select the desired counter location
3. Generate the QR code through the interface
4. Print or display the code at your business location

## Payment Flow

The transaction sequence involves:
- Customer scans merchant's QR code via Zalopay App
- Customer inputs payment amount
- Payment is processed
- Merchant receives confirmation of successful transaction

## Navigation Structure

The documentation includes related sections:
- Dynamic QR Code (alternative implementation)
- Payment Gateway options
- Tokenization Payments
- Additional payment methods (ApplePay, GooglePay, QuickPay)

**Last Updated:** July 31, 2024
