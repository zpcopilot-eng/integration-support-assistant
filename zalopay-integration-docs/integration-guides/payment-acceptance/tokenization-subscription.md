# Subscription - Zalopay Docs

Nguồn: https://docs.zalopay.vn/docs/guides/payment-acceptance/tokenization/subscription

## Overview

According to the documentation, the Subscription feature operates without direct API integration with merchants. Instead, it functions by "listen[ing] kafka data from AgreementPay to subscribe User item and have schedule scanning the matched by Rule to notifitcation to User via ZMS / SMS."

For implementation details, the docs reference the Agreement-Pay Integration document.

## Key Use Cases

**2.1 Binding**
Users add Zalopay as a payment method for merchant services. The subscription system takes no action during this phase.

**2.2 Purchase/Payment**
When users purchase merchant services, the merchant requests payment through Zalopay or Agreement. The Agreement then notifies the Subscription system to enable reminder notifications.

**2.3 Notification/Reminder**
The Subscription system independently scans for matched items based on configured rules and sends reminder notifications to users via the Zalopay messaging system, operating independently from merchants and payment processors.

**2.4 Unbind**
Users discontinue Zalopay as their payment method by either removing it from the merchant application or unbinding the service within the Zalopay app.

## Resources

- Documentation: [Zalopay Docs](/docs/guides/intro)
- Support: hotline 1900 545 436 or op@zalopay.vn
