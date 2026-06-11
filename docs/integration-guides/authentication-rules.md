# Authentication Rules - Zalopay Documentation

Nguồn: https://docs.zalopay.vn/docs/guides/integration-guide/authentication-rules/intro

## Overview
This page explains the authentication mechanism for Zalopay API integration.

## Authentication Details

| Aspect | Information |
|--------|-------------|
| **Algorithm** | HmacSHA256 |
| **Default Method** | HmacSHA256 (registered during merchant setup) |

## Authentication Formula

The authentication process uses the following calculation:

**mac = HMAC(hmac_algorithm, key, hmacinput)**

Where:
- **hmac_algorithm**: The security method registered by the merchant with Zalopay (defaults to HmacSHA256)
- **key**: A unique value provided by Zalopay during merchant registration
- **hmacinput**: Varies depending on the specific API being called

## Navigation
- **Previous**: Communication Protocols
- **Next**: Payment Acceptance

## Resources
- [Merchant Portal](https://mc.zalopay.vn)
- [API Explorer](/docs/openapi)
- [SDK Documentation](/docs/sdk/intro)
- [Example Integrations](https://github.com/zalopay-samples)

**Last Updated**: July 31, 2024
