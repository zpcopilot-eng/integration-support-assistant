# Zalopay Payment Gateway Documentation

Nguồn: https://docs.zalopay.vn/docs/guides/payment-acceptance/payment-gateway/intro

## Overview
Zalopay Gateway is a Vietnamese payment platform offering multiple payment methods including Zalopay Wallet, ATM cards, internet banking, credit cards, VietQR, and Apple Pay. The system emphasizes security (PCI DSS and ISO 27001 certified) and streamlined business integration.

## Key Features

**Diverse Payment Options:** The gateway supports "payment methods, from Zalopay Wallet, ATM Card, Internet Banking, Visa Card, VietQR to Apple Pay."

**Security:** User payment information is encrypted with "high safety and reliability" and meets international security standards.

**Integration:** The API interface enables quick integration and optimization of online payment processes.

## How It Works

The payment flow involves eight steps:

1. Customer initiates payment
2. Merchant creates order via Zalopay
3. Zalopay verifies merchant and returns payment link (order_url)
4. Merchant redirects customer to gateway
5. Gateway displays order details
6. Customer selects payment method and completes transaction
7. Gateway processes payment and redirects to merchant
8. Merchant displays payment status to customer

## Integration Steps

**1. Display Payment Methods** - Show available Zalopay payment options at checkout

**2. Create Order** - Send order creation request with parameters like amount, description, and preferred payment method via the Create Order API

**3. Redirect to Gateway** - Use the returned order_url to direct customers, with configurable payment method displays (all methods, VietQR only, credit cards, ATM cards, or Zalopay wallet)

**4. Process Results** - Handle callbacks from Zalopay, query order status, and process redirect data with checksum validation

## Payment Methods Available

- Domestic ATM cards
- Credit/debit cards
- Bank transfer via VietQR
- Zalopay QR payment
- Buy now pay later options
