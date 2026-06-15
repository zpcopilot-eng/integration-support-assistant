# Agent Flow

Tài liệu này mô tả luồng xử lý nội bộ của **Integration Support Assistant**
(`main.py`). Đây là tài liệu cho team phát triển — khác với
`zalopay-integration-docs/`, nội dung ở đây **không** được index vào
`search_docs` và không hiển thị cho merchant.

## 1. Kiến trúc tổng quan

```
                ┌─────────────────────────┐
HTTP POST       │                          │
/invocations ──▶│   handler()              │
                 │   (app.entrypoint)       │
Telegram ───────▶│   telegram_webhook()     │
webhook          │                          │
                 └────────────┬─────────────┘
                                │
                                ▼
                 ┌──────────────────────────┐
                 │  agent (LangGraph,        │
                 │  create_agent)            │
                 │  - SYSTEM_PROMPT          │
                 │  - tools: search_docs,    │
                 │    remember, recall       │
                 │  - checkpointer (memory)  │
                 └────────────┬───────────────┘
                                │
                                ▼
                 validate_citations() + is_doc_gap()
                                │
                                ▼
                       response trả về client
```

## 2. Luồng xử lý request HTTP (`handler`)

1. **Kiểm tra header**: yêu cầu `X-GreenNode-AgentBase-User-Id` và
   `X-GreenNode-AgentBase-Session-Id` (bắt buộc vì agent dùng memory). Thiếu
   1 trong 2 → trả `{"status": "error", ...}`.
2. **Map sang LangGraph config**:
   - `thread_id = session_id` → short-term memory (lịch sử hội thoại) theo
     từng session, persist qua `checkpointer` (`AgentBaseMemoryEvents`).
   - `actor_id = user_id` → namespace cho long-term memory (`remember`/`recall`).
3. **`agent.invoke(...)`**: LangGraph agent loop chạy với `SYSTEM_PROMPT`,
   có thể gọi tool nhiều lần (search_docs, remember, recall) trước khi trả
   lời cuối.
4. **Post-processing trên câu trả lời cuối** (`ai_message.content`):
   - `validate_citations()` — xem mục 5.
   - `is_doc_gap()` — nếu câu trả lời là "không tìm thấy thông tin", gọi
     `log_doc_gap()` (mục 6).
5. Trả về `{"status": "success", "response": ..., "timestamp": ...}`.

## 3. Luồng Telegram webhook (`/telegram-webhook`)

Tương tự `handler`, nhưng:
- `thread_id = actor_id = chat_id` (mỗi chat Telegram là 1 session/actor).
- Không yêu cầu header AgentBase (Telegram tự định danh qua `chat_id`).
- Kiểm tra `X-Telegram-Bot-Api-Secret-Token` nếu `TELEGRAM_WEBHOOK_SECRET`
  được cấu hình.
- Sau `validate_citations()` + `is_doc_gap()`, response được:
  - cắt ngắn nếu vượt `TELEGRAM_MAX_MESSAGE_LENGTH` (4096 ký tự),
  - convert markdown đơn giản (`**bold**`, `` `code` ``, bullet `- `/`* `)
    sang Telegram HTML qua `markdown_to_telegram_html()`,
  - gửi qua Telegram Bot API (`sendMessage`, `parse_mode=HTML`); nếu lỗi
    (ví dụ HTML không hợp lệ), fallback gửi lại bằng plain text.

## 4. Tools của agent

| Tool | Namespace memory | Mục đích |
|---|---|---|
| `search_docs(query)` | `/strategies/{DOCS_MEMORY_STRATEGY_ID}/actors/shared` (`DOCS_NAMESPACE`) | Tìm kiếm nội dung đã index từ `zalopay-integration-docs/` (xem mục 7). Trả về tối đa 5 record, mỗi record bắt đầu bằng `[Nguồn: <path>#<anchor>]`. |
| `remember(fact)` | `/strategies/{MEMORY_STRATEGY_ID}/actors/{user_id}` | Lưu fact dài hạn cho 1 user cụ thể (qua `_build_namespace`). |
| `recall(query)` | cùng namespace với `remember` | Tìm fact đã lưu cho user hiện tại. |

`SYSTEM_PROMPT` yêu cầu agent luôn gọi `search_docs` trước khi trả lời, và
nếu không có thông tin liên quan, trả lời đúng theo mẫu bắt đầu bằng
*"Tôi không tìm thấy thông tin..."* — câu này được `is_doc_gap()` dùng để
phát hiện doc gap.

## 5. Citation validation (`validate_citations`)

- `DOC_PATHS`: tập hợp tất cả đường dẫn `*.md` thật có trong
  `zalopay-integration-docs/` (tính 1 lần khi load module, dạng
  `zalopay-integration-docs/...`).
- `CITATION_RE`: regex bắt các đoạn `(Nguồn: <path>)` hoặc `(Nguon: <path>)`
  trong câu trả lời.
- Với mỗi citation tìm được, lấy phần trước `#` (bỏ anchor) và so với
  `DOC_PATHS`. Nếu path không tồn tại → xoá toàn bộ `(Nguồn: ...)` khỏi câu
  trả lời (loại bỏ citation bị hallucinate/sai đường dẫn), giữ nguyên phần
  nội dung.
- **Lưu ý**: chỉ validate phần file path, không validate `#anchor` — anchor
  sai (ví dụ do file đổi heading nhưng chưa reindex) sẽ không bị phát hiện.

## 6. Doc-gap logging (`log_doc_gap`, `is_doc_gap`)

- `DOC_GAPS_NAMESPACE = /strategies/{DOCS_MEMORY_STRATEGY_ID}/actors/doc-gaps`.
- `is_doc_gap(text)`: strip dấu tiếng Việt (`_strip_accents`, NFD +
  loại bỏ combining marks) rồi kiểm tra có chứa `"toi khong tim thay thong tin"`
  hay không — match accent-insensitive vì model không luôn trả lời đúng dấu.
- Khi match, `log_doc_gap(question)` ghi 1 record
  `[<ISO timestamp>] <câu hỏi gốc>` vào `DOC_GAPS_NAMESPACE`. Lỗi ghi memory
  bị bắt và bỏ qua (`except Exception: pass`) để không làm fail response
  của user.
- **Mục đích**: team docs có thể search/list namespace `doc-gaps` định kỳ để
  biết những câu hỏi merchant hỏi mà tài liệu chưa có, từ đó bổ sung
  `zalopay-integration-docs/`.

## 7. Indexing pipeline (`scripts/index_docs.py`)

Chạy thủ công (`python3 scripts/index_docs.py`) hoặc tự động qua
`.github/workflows/index-docs.yml` (trigger khi push vào `main` thay đổi
`zalopay-integration-docs/**` hoặc `scripts/index_docs.py`).

Các bước:
1. Đọc toàn bộ `*.md` dưới `zalopay-integration-docs/`.
2. `chunk_file()`: tách mỗi file theo heading `##`/`###` thành các chunk
   riêng, mỗi chunk được gắn `[Nguồn: <rel_path>#<slug>]` (slug dạng
   GitHub anchor, tự xử lý trùng tên bằng hậu tố `-1`, `-2`, ...). Nội dung
   trước heading đầu tiên được index riêng, citation chỉ có file path
   (không anchor).
3. `purge_namespace()`: xoá **toàn bộ** record hiện có trong `DOCS_NAMESPACE`
   trước khi insert — tránh tích lũy record trùng/cũ qua nhiều lần reindex
   (memory API không có upsert-by-key).
4. Insert lại theo batch `BATCH_SIZE = 20` (do API embed đồng bộ từng
   record, request quá lớn sẽ vượt timeout 30s mặc định của SDK).

Kết quả: `search_docs` luôn trả về chunk theo section cụ thể với citation
`zalopay-integration-docs/<path>#<anchor>` khớp với cấu trúc heading hiện
tại của tài liệu.
