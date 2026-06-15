# Zalopay All-in-One Disbursement Integration Guide

Nguồn: https://docs.zalopay.vn/docs/guides/business-operation/disbursement-all-in-one/intro

## Overview

Zalopay's All-in-One Disbursement feature enables businesses to transfer funds efficiently from their Business Wallet to recipient accounts through a unified platform. The service emphasizes "fast and easy transfer fund" capabilities alongside automated processes and robust security measures.

## Key Features

The platform offers several core advantages:

- **Unified transfer capability** to Zalopay Wallets, Bank Accounts, and ATM Cards
- **Automated payment processes** reducing manual errors
- **State-of-the-art security measures** protecting transactions
- **Expenditure tracking** and reporting functionality
- **Cross-platform accessibility** via mobile and web interfaces

## Integration Prerequisites

Before implementation, merchants must:

1. Register and obtain credentials (`app_id`, `mac_key`, `private_key`) from Merchant Portal
2. Understand relevant APIs: Verify Account, Transfer Fund, Query Transaction, Balance, and Bank Code List
3. Familiarize themselves with secure data transmission protocols

## Four-Step Integration Workflow

**Step 1:** Query merchant wallet balance using the Balance API

**Step 2:** Verify recipient account details through the Verify Account API, supporting three account types (Zalopay, Bank Account, ATM Card)

**Step 3:** Initiate transfers via Transfer Fund API with encrypted receiver information

**Step 4:** Monitor transaction completion using Query Transaction API

## Response Structure

All API responses follow a consistent format with `return_code`, `return_message`, and transaction-specific data fields. Successful transfers return status code 3, with masked sensitive information (account numbers, phone numbers) in responses.
