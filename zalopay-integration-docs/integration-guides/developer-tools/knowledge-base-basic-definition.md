# Base Definition - Zalopay Docs

Nguồn: https://docs.zalopay.vn/docs/developer-tools/knowledge-base/basic-definition

## Overview

This documentation page outlines key terminology used throughout Zalopay's integration documentation.

## Definition

### app_id
"This is a Zalopay-provided identifier specific to the merchant's service or application, established during the integration agreement for payment methods." Example: App ID 123 for Merchant Web, App ID 124 for Merchant App.

### app_user
Represents "Information of the user making the payment for the order: id/username/name/phone number/email." If unavailable, default information like application name may be substituted. Examples include user names, phone numbers, or email addresses.

### app_trans_id
"The merchant transaction code sent through the Zalopay system for the user to proceed with payment." Format example: 20121225_123456789

### sub_app_id
Serves as "the service identifier/group of services used for payment within the merchant's application." This parameter is required for certain merchants offering multiple services like mobile cards or game cards.

### callback_url
"This is the URL of the merchant. After Zalopay successfully deducts the money, it will notify the merchant of the payment result for the order via the callback method (server-to-server)." Can be dynamically set per order or configured as default. Example: https://pay.abc.com/payment/ipn/zalopay

### redirecturl
"This is the URL of the merchant. This URL is used to redirect from Zalopay back to the partner's shopping page after the customer completes the payment." Supports both AppLink (mobile app) and WebLink (website) formats.
