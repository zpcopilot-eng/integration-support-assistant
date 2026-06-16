# Card Token - Zalopay Documentation

Nguồn: https://docs.zalopay.vn/docs/guides/payment-acceptance/tokenization/card-token

## Overview

Card tokenization enables merchants to store customer payment card information with consent for streamlined future transactions. The feature supports:

- Credit cards
- ATM cards via 40+ NAPAS-affiliated banks

**Common use cases** include subscriptions, e-commerce repeat purchases, and travel industry transactions.

## Prerequisites

Before integration, ensure:

- Active merchant account with `app_id`, `key1`, and `key2` credentials from Merchant Portal
- Familiarity with required APIs: CreateOrder, QueryOrder, CreateBinding, Unbind, PayByToken, and QueryPaymentToken
- Understanding of callback mechanisms and secure data transmission protocols

## How It Works

**Flow 1: Card Binding** - User initiates card storage with merchant consent

**Flow 2: Payment & Token Return** - System processes payment while confirming tokenization preferences via Zalopay Gateway

## Integration Steps

### Step 1: Initiate Card Binding

Call the Create Binding API from your server. The response provides `binding_qr_link` for user confirmation. After completion, Zalopay sends callback data including `pay_token` (required for future transactions) and `binding_id` (needed for unbinding).

Key callback parameters include masked card number, issuing bank details, and binding status.

### Step 2: Pay Using Token

1. Create an order via Create Order API
2. Call Pay By Token API with the stored `pay_token` and `zp_trans_token`
3. User confirms payment via OTP at provided `verification_url`
4. Merchant receives payment confirmation callback

### Step 3: Unbind Agreement

Call Unbind API with the `binding_id` when users opt out of auto-debit features.

---

**Resources:** [Live demo](https://zalopay-tokenized-payment.vercel.app/) | [GitHub example](https://github.com/zalopay-samples/quickstart-nextjs-tokenized-payment)
