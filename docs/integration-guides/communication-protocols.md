# Communication Protocols

Nguồn: https://docs.zalopay.vn/docs/guides/integration-guide/communication-protocols/intro

## Overview

The Zalopay documentation outlines specific requirements for merchants integrating with their API services. These guidelines establish technical standards for secure and consistent communication.

## Key Requirements

According to the documentation, merchants must adhere to the following specifications:

| Aspect | Requirement |
|--------|-------------|
| **Transmission Method** | "HTTPS transmission is adopted" for security |
| **Submission Method** | POST method required |
| **Data Format** | JSON or form-urlencoded formats accepted |
| **Character Encoding** | UTF-8 standard |
| **Authentication** | HmacSHA256 algorithm used |
| **Verification** | Authentication validation needed for both requests and responses |

## Processing Guidelines

The documentation specifies a particular sequence for handling responses: "First refer to the return of the protocol field, then refer to the code in the response message, and finally refer to the transaction status."

## Related Resources

- [Authentication Rules](/docs/guides/integration-guide/authentication-rules/intro)
- [Integration Guide](/docs/guides/integration-guide/intro)
- [API Explorer](/docs/openapi)

**Contact:** Hotline 1900 545 436 or op@zalopay.vn for support
