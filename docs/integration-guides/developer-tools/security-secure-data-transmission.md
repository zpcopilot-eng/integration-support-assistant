# Secure Data Transmission | Zalopay Docs

Nguồn: https://docs.zalopay.vn/docs/developer-tools/security/secure-data-transmission

## Overview

Zalopay implements two security techniques to protect data integrity and authenticity: "HMAC and Digital signature to ensure the integrity and authenticity of its data."

## HMAC

The HMAC technique secures data in three contexts:
- API requests via the `mac` field
- Callbacks from Zalopay via the `mac` field
- Redirects via the `checksum` field

**Three key components:**

1. **Algorithm**: SHA-256 by default (merchant-configurable)
2. **Data**: Created by joining necessary data with the `|` character
3. **Keys**: Two keys provided upon registration:
   - `key1`: Used for requests to Zalopay
   - `key2`: Used for callbacks and redirects from Zalopay

**CreateOrderAPI Example:**
```javascript
import CryptoJS from "crypto-js";
const order = { // request data };
const data = [
  order.app_id,
  order.app_trans_id,
  order.app_user,
  order.amount,
  order.app_time,
  order.embed_data,
  order.item
].join("|");
order.mac = CryptoJS.HmacSHA256(data, configZLP.key1).toString();
```

## Digital Signature

Unlike HMAC's shared secret key approach, "digital signature uses a pair of public-private keys." The client maintains the private key for signing; Zalopay stores the public key for verification.

**Used in**: The `sig` field for requests like TopUpAPI

**Three key components:**

1. **Algorithm**: RSA
2. **Data**: API-specific (refer to specifications)
3. **Key**: Private key from merchant registration

**TopUpAPI Example:**
```javascript
import CryptoJS from "crypto-js";
import rsa from "node-rsa";

const request = { // request data };
const message = [
  request.appId,
  request.paymentId,
  request.partnerOrderId,
  request.mUId,
  request.amount,
  request.description,
  request.partnerEmbedData,
  request.extraInfo,
  request.time
].join("|");

const mac = crypto.HmacSHA256(message, configZLP.key1).toString();
const msg = Buffer.from(mac);
const privateKey = Buffer.from(configZLP.secretKey);
const rsaInstance = new rsa(privateKey, 'pkcs8');
const signature = rsaInstance.sign(msg, 'base64', 'utf8');
request.sig = signature;
```
