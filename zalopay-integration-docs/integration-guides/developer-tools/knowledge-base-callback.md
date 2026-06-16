# Zalopay Callback Documentation

Nguồn: https://docs.zalopay.vn/docs/developer-tools/knowledge-base/callback

## Overview
Zalopay's callback mechanism automatically notifies merchants about transaction events. These webhooks enable communication between Zalopay and merchant servers, allowing merchants to stay informed about payment outcomes.

## How It Works
When transactions succeed, "Zalopay Server will notify to Merchant Server via Callback URL" that was registered during order creation. Merchants then use a provided security key to validate the incoming data.

## Request Structure
Callbacks arrive as POST requests with JSON content containing three main fields:
- **data**: Transaction details as a JSON string
- **mac**: HMAC signature for verification
- **type**: Indicates callback category (1 for orders, 2 for agreements)

## Callback Data Types

**Order callbacks** include transaction ID, amount, timestamp, items, payment channel, and user information.

**Agreement/Tokenization callbacks** contain binding details, payment tokens, and user phone masks.

**ZOD callbacks** provide alternative fields like `appId`, `mcRefId`, and `userChargeAmount`.

## Response Format
Merchants must return:
```json
{
  "return_code": 1,
  "return_message": "success"
}
```

Return code 1 indicates success; 2 indicates failure.

## Security Validation
Recipients must verify callbacks using HMAC-SHA256 (default) with `key2` (the callback/redirect key issued at registration — see [Secure Data Transmission](../developer-tools/security-secure-data-transmission.md#hmac)). The validation ensures authenticity: "if (reqmac == callback_data.mac)" indicates a legitimate notification.

## Best Practices
- Implement HTTPS for encrypted communication
- Make callback processing idempotent to handle duplicates safely
- Exclude callback routes from CSRF protection frameworks
- Proactively query orders after 15 minutes without callback notification
- Log all callback events for audit purposes
