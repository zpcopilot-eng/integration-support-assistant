# Zalopay Status Codes Documentation

Nguồn: https://docs.zalopay.vn/docs/developer-tools/knowledge-base/status-codes

## Overview

The Zalopay API returns responses containing standard fields:

- **return_code**: General status indicator (1=SUCCESS, 2=FAIL, 3=PROCESSING)
- **return_message**: Status description
- **sub_return_code**: Detailed status code
- **sub_return_message**: Detailed status explanation

When `return_code` equals 2, consult the `sub_return_code` for specific error details.

## Key Status Categories

### Create Order Errors
Common issues include duplicate transaction IDs (-68), malformed requests (-401), invalid authentication (-402), rate limiting (-429), and system errors (-500/-999).

### Query Order Status Errors
Possible failures involve expired transactions (-54), insufficient user balance (-63), invalid app transaction IDs (-92), non-existent orders (-101), and bank-related issues (-217).

### Refund Operations
Refund-specific codes address expired requests (-13), missing transactions (-101), unsupported partial refunds (-32), and timing violations.

### Wallet Management
Wallet operations track binding creation, token queries, balance inquiries, and unbinding actions with codes addressing token expiration (-1007), locked accounts (-1009), and permission issues (-1011).

### Card Operations
Card binding and payment processes include token validation errors (-7202), missing tokens (-7041), and invalid statuses (-7217).

## Common Resolution Patterns

For parameter validation errors, merchants should verify formatting and completeness. Authentication failures require credential verification against Zalopay's records. Rate limiting necessitates retry delays. System maintenance errors resolve after service restoration.
