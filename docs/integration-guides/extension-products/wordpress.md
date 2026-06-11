# WordPress | Zalopay Docs

Nguồn: https://docs.zalopay.vn/docs/guides/extension-products/wordpress/intro

## Overview

WordPress is described as "an open source system used to publish blogs/websites written in the PHP programming language and MySQL database." Zalopay offers a plugin enabling merchants to integrate Zalopay payment methods into WordPress sites quickly and securely.

## Integration Workflow

The setup process involves two main phases:

1. **Plugin Installation**
   - Download the Zalopay plugin
   - Navigate to Plugins → Add New Plugin in WordPress admin
   - Upload and activate the plugin

2. **Payment Method Configuration**
   - Access plugin settings after activation
   - Configure individual payment methods by enabling them and entering credentials

## Required Configuration Information

Merchants need three key pieces of information from Zalopay (available in both sandbox and production environments):

- AppId
- Mac key (Key 1)
- Callback key (Key 2)

## Supported Payment Methods

The plugin supports multiple payment options:

- Zalopay QR code scanning
- Multi-function QR codes (compatible with banking apps)
- ATM card payments
- Credit cards (Visa, Mastercard, JCB)
- Apple Pay

## Configuration Settings

Each payment method requires:

- Enable/Disable toggle
- Sandbox mode indicator
- AppID, Mac key, and Callback key entry
- Custom description for user display
- Gateway description (preset)

After entering credentials and clicking "Save changes," the payment method becomes available during checkout.
