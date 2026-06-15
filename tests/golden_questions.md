# Golden Questions

Regression set for the search_docs / citation pipeline. After changing
SYSTEM_PROMPT, the chunking in `scripts/index_docs.py`, or
`validate_citations`, re-run these questions through the agent and check:

1. The answer references the **expected source(s)** below (file + anchor).
2. Every `(Nguồn: ...)` in the answer points at a real file under `zalopay-integration-docs/`
   (i.e. `validate_citations` left it untouched).
3. The answer does not invent facts not present in the cited section.

| # | Question | Expected source(s) |
|---|----------|---------------------|
| 1 | Cong thuc tinh chu ky xac thuc (mac) cua Zalopay la gi? | `zalopay-integration-docs/integration-guides/authentication-rules.md#authentication-formula` |
| 2 | API call den Zalopay phai dung phuong thuc HTTP nao va format du lieu gi? | `zalopay-integration-docs/integration-guides/communication-protocols.md#key-requirements` |
| 3 | Callback tu Zalopay gui ve merchant server gom nhung field nao? | `zalopay-integration-docs/integration-guides/developer-tools/knowledge-base-callback.md#request-structure` |
| 4 | Zalopay co ho tro Sandbox cho developer khong? | `zalopay-integration-docs/faq/faq.md` (section "Does Zalopay support Sandbox for Developers?") |
| 5 | Lam sao de tich hop Shopify voi Zalopay VietQR? | `zalopay-integration-docs/integration-guides/extension-products/shopify-vietqr.md` |
| 6 | Cau hoi ngoai pham vi, vi du: "Gia co phieu Zalopay hom nay la bao nhieu?" | Khong co trong tai lieu — agent phai tra loi "Toi khong tim thay thong tin nay trong tai lieu hien co." va khong tu bia nguon |

## How to run

Until an automated harness exists, run each question manually against the
deployed agent (or via `agent.invoke` locally) and compare the output's
citations against the table above.
