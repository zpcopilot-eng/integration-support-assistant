# QuickPay Documentation - Zalopay

Nguồn: https://docs.zalopay.vn/docs/guides/payment-acceptance/quick-pay/intro

## Overview

QuickPay enables a streamlined payment process where customers select products at a merchant's store, open the Zalopay app to generate a payment code, and the merchant scans this code to complete the transaction.

**Key participants:**
- **End-user**: Zalopay account holders making purchases
- **Merchant**: Sellers offering products or services
- **Zalopay**: Payment platform facilitating integration

## How It Works

The flow involves five essential steps:

1. End-users open Zalopay and select "Payment code"
2. Merchants scan the payment code using integrated software to deduct funds
3. Merchants receive success notifications in their system
4. Merchants query order status if they haven't received Zalopay's IPN notification yet
5. Merchants handle IPN callbacks when payment succeeds

## Integration Requirements

To implement QuickPay, merchants must:

- Integrate Zalopay's API (subject to Zalopay verification on production transactions)
- Set up systems to receive and process IPN callbacks
- Query order status as a fallback mechanism
- Handle the scanning and payment deduction workflow

## API Reference

The primary API endpoint for QuickPay implementation is the Create Order QuickPay specification, available in the documentation's API specs section.

**Last Updated**: July 31, 2024
