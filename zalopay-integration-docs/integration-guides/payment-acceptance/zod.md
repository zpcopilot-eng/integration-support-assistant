# Zalopay On Delivery Integration Documentation

Nguồn: https://docs.zalopay.vn/docs/guides/payment-acceptance/zod/intro

## Overview

Zalopay On Delivery (ZOD) represents "a payment solution that enables users to pay for their goods on delivery by scanning QR codes using Zalopay." This service allows merchants to accept payments through QR code scanning at the point of delivery.

## Key Prerequisites

Before implementing ZOD, merchants must:

- Register a merchant account and obtain `app_id` and `mac_key` credentials from the Merchant Portal
- Understand three critical APIs: CreateZODInvoice, QueryZODInvoice, and QueryZODOrder
- Comprehend callback mechanisms and secure data transmission protocols

## Integration Workflow

The implementation consists of two primary steps:

**Step 1: Initiate ZOD Order**
Merchants call the CreateZODInvoice API after customers select on-delivery payment. The response includes an `orderUrl` that merchants encode into a QR code for display. Notably, "This url is used to generate QR code will be displayed on shipper app and will be expired and mark as INVALID after 1 month since its creation."

**Step 2: Process Payment Results**
Upon payment completion, Zalopay sends callback notifications containing transaction details including appId, mcRefId, amount, zpTransId, and other payment metadata. Merchants must validate callbacks using callback keys for security purposes.

## Critical Security Requirements

Documentation emphasizes merchants must:
- Verify callbacks originated from Zalopay using callback key validation
- Ensure callback URLs use identical domains as their servers
- Maintain publicly accessible callback endpoints

## Query Functionality

Merchants should proactively query order status via the QueryZODOrder API rather than relying solely on callbacks, as network issues may prevent callback delivery.
