# ApplePay Integration Documentation

Nguồn: https://docs.zalopay.vn/docs/guides/payment-acceptance/applepay/intro

## Overview

Zalopay offers Apple Pay as a payment method, enabling businesses to enhance sales through a secure checkout experience. Key benefits include:

- **Fast checkout**: Customers complete purchases with a single tap
- **Enhanced security**: Transactions require Face ID, Touch ID, or password authentication
- **Wide device support**: Works on iPhone, Apple Watch, Mac, and iPad
- **Browser compatibility**: Safari, Chrome, Firefox, Edge on iOS; Safari on macOS

## Integration Methods

### Merchant-Hosted Approach
Merchants configure their system by passing specific parameters when creating orders:
```json
{
  "bank_code": "",
  "embed_data": {
    "preferred_payment_method": ["applepay"]
  }
}
```

### Zalopay-Hosted Portal
Merchants direct users to the Zalopay Portal via the `order_url`, where Apple Pay appears as an available payment option.

## Testing Requirements

**Account Setup**: Use Zalopay's test credentials to sign in on your Apple device.

**Device Configuration**:
- Compatible device running latest iOS, iPadOS, watchOS, or macOS
- Active Apple ID
- Test card added to Wallet (Visa/Mastercard available)

**Payment Flow**: Create test orders, access the payment gateway, and follow on-screen instructions to complete transactions.
