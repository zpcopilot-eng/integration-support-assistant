# Wallet Token - Zalopay Payment Integration

Nguồn: https://docs.zalopay.vn/docs/guides/payment-acceptance/tokenization/wallet-token

## Overview

Wallet Token enables merchants to implement auto-debit functionality, allowing automatic payment processing from user Zalopay balances after agreement confirmation.

## Key Prerequisites

Before integration, merchants must:

- Register and obtain `app_id`, `key1`, and `key2` credentials
- Understand multiple tokenization APIs including binding, querying, and payment APIs
- Comprehend callback mechanisms and secure data transmission protocols

## Core Integration Steps

### Step 1: Binding Initiation

Merchants call the CreateBinding API to establish a connection between user Zalopay accounts and the merchant application. The system generates multiple confirmation options:

- **Deep link** for mobile app scenarios
- **QR code link** for web-based confirmation
- **Short link** for merchant-generated QR codes

"The callback data includes the `pay_token` field, which the merchant will store in the system, for later payments using this token."

Bindings expire after 15 minutes without user confirmation.

### Step 2: Payment Processing

Before payment, merchants:

1. Verify user can pay via QueryBalance API
2. Create an order using CreateOrder API
3. Execute payment through PayByToken API
4. Receive payment confirmation callbacks

### Step 3: Agreement Termination

Merchants can terminate agreements using the Unbind API, though users may also initiate unbinding through the Zalopay app.

### Step 4: User Information Retrieval

The QueryUser API provides basic user details, currently limited to masked phone numbers.

## Security Requirements

"It's **important** to verify that the request actually came from Zalopay by using `key2` to validate the callback's data" (see [Secure Data Transmission](../developer-tools/security-secure-data-transmission.md#hmac)).

Callback URLs must be publicly accessible with matching server domains.

## Resources

- [Live demonstration application](https://zalopay-tokenized-payment.vercel.app)
- [GitHub implementation example](https://github.com/zalopay-samples/quickstart-nextjs-tokenized-payment)
- API Explorer and comprehensive documentation available
