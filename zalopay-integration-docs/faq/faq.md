# FAQs | Zalopay Docs

Nguồn: https://docs.zalopay.vn/docs/faq

## FAQs

This document lists the Most Frequently Asked Questions about Zalopay Integration.

### 1. Registration information for the integrated application (AppID, Keys) with Zalopay?

The required information to establish integrated AppID, Keys:

- **App name**: display on the payment pages on Zalopay and help identify when using the tool in case of Partner has many products or services.
- **Callback URL**: merchant webhook for obtaining transaction results from Zalopay. The callback URL must be HTTPS (Production environment) and support TLS 1.2 or higher. Check if your domain supports TLS 1.2 or higher at [https://www.ssllabs.com/ssltest/](https://www.ssllabs.com/ssltest/)
- **Redirect URL**: link to merchant's transaction result page.

### 2. How many payment/refund methods are there in Zalopay?

| PAYMENT METHOD | WALLET | REFUND TO | REFUND TIME | SUPPORTED BANKS |
|---|---|---|---|---|
| Zalopay App | Zalopay Wallet | Zalopay Wallet | Immediately | Vietcombank, Vietinbank, BIDV, Sacombank, Eximbank, SCB, Viet Capital Bank, JCB |
| ATM / Bank Account | Zalopay Wallet | Immediately | Visa / Master / JCB | |
| Card | | 5 - 7 working days | Card payment / Bank Account via Zalopay Gateway | |
| ATM / Bank Account | Bank Account | 3 - 5 working days (depending on the bank) | ABBank, ACB, Agribank, Bac A Bank, Bao Viet Bank, BIDV, DongA Bank, Eximbank, GP Bank, HD Bank, Lien Viet Post Bank, Maritime Bank, MB Bank, NamA Bank, NCB, Viet Capital Bank, OCB, Ocean Bank, PG Bank, Sacombank, Saigon Bank, SCB, SeA Bank, SHB, Techcombank, TP Bank, VIB | |
| Visa / Master / JCB | Card | 5 - 7 working days (depending on the bank) | | |

> For transactions with promotions from Zalopay's program or implementing partners, the required refund amount must be a full refund. Refund time will vary from bank to bank.

### 3. Does Zalopay support Sandbox for Developers?

Sure! Information about the sandbox environment can be found [here](/docs/developer-tools/test-instructions/testing).

### 4. What is a valid Callback URL?

"Zalopay Callback URL only support URL = domain + port 443, does NOT support IP and other port, and TLS version 1.2 or higher is a necessity."

- Partners can use online services like [https://www.ssllabs.com/ssltest](https://www.ssllabs.com/ssltest) to check TLS.

An example valid Callback URL: [https://abc.com/zalopaycallback](https://abc.com/zalopaycallback).

The Sandbox environment supports port 80.

### 5. Does Zalopay support Credit Cards, ATMs, accounts for testing in a real environment? If not, how long will it take to process the refund?

"Zalopay does not support real money for testing, partners use their cards, bank accounts, ... for testing and then use merchant's tools to refund."

Please refer to FAQ #2 for information regarding the refund time.

### 6. Does Zalopay have a built-in merchant support technical team?

Certainly, Zalopay will provide the Merchant with comprehensive technical support information, as well as assistance in testing and gathering data, until full integration is done.

For more information, please contact:

- Hotline: [1900 54 54 36](tel:1900545436)
- Email: [hotro@zalopay.vn](mailto:hotro@zalopay.vn)

---

**Last updated on Jul 31, 2024**
