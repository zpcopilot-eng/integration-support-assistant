# API Tokenization Bind (Liên kết phương thức thanh toán)

Nguồn: https://docs.zalopay.vn/docs/specs/tokenization-bind

## Tổng quan

API Tokenization Bind dùng để khởi tạo quy trình liên kết (binding) một phương thức thanh toán (ví Zalopay hoặc thẻ) của người dùng với ứng dụng của merchant, phục vụ cho các giao dịch thanh toán bằng token sau này.

- **Method:** POST
- **Endpoint:** `/tokenization-bind`

## Request Parameters

| Tham số | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|
| `app_id` | int64 | Có | ID do Zalopay cấp cho merchant/ứng dụng |
| `req_date` | int64 | Có | Thời điểm tạo request liên kết, tính bằng Unix timestamp (milliseconds); request có hiệu lực trong 15 phút |
| `app_trans_id` | string(40) | Có | Mã giao dịch duy nhất, định dạng `yyMMddxxxxxxxxx` |
| `identifier` | string | Có | Định danh người dùng trên hệ thống merchant (user ID, số điện thoại, email, ...) |
| `binding_type` | string | Có | Loại phương thức liên kết: `WALLET` hoặc `CARD` |
| `binding_mode` | string | Có | Chế độ liên kết: `BIND` (chỉ liên kết) hoặc `BIND_AND_PAY` (liên kết và thanh toán luôn) |
| `device_type` | string | Có | Loại thiết bị: `MOBILE` hoặc `DESKTOP` |
| `binding_data` | string | Có | Chuỗi JSON chứa `redirect_url` (web), `redirect_deep_link` (mobile), `callback_url`, `embed_data` |
| `payment_data` | string | Có | Chuỗi JSON chứa `amount` (int64), `description`, `callback_url`, `embed_data` — chỉ áp dụng khi `binding_mode = BIND_AND_PAY` |
| `mac` | string | Có | Chữ ký xác thực HMAC (xem [Tính toán mac](#tính-toán-mac)) |

## Tính toán mac

```
mac = HMAC_SHA256(key1, app_id|app_trans_id|identifier|binding_mode|binding_type|device_type|binding_data|payment_data|req_date)
```

- Thuật toán mặc định: `HmacSHA256`
- `key1` do Zalopay cấp khi đăng ký merchant

> Xem thêm chi tiết tại [Secure Data Transmission](../integration-guides/developer-tools/security-secure-data-transmission.md#hmac)

## Response Fields

| Field | Kiểu | Mô tả |
|---|---|---|
| `return_code` | int | Mã trạng thái xử lý (xem [Mã lỗi](#mã-lỗi)) |
| `return_message` | string | Mô tả trạng thái xử lý |
| `sub_return_code` | int | Mã trạng thái chi tiết |
| `sub_return_message` | string | Mô tả mã trạng thái chi tiết |
| `binding_token` | string | Token định danh phiên liên kết |
| `binding_url` | string | URL để người dùng hoàn tất quy trình liên kết |
| `reform_url` | string | URL dùng để định dạng lại tham số liên kết (nếu cần) |

## Mã lỗi

| `return_code` | Ý nghĩa |
|---|---|
| `1` | SUCCESS |
| `2` | FAIL |
| `3` | PROCESSING |
| `406` | ILLEGAL_STATUS |
| `-401` | ILLEGAL_DATA_REQUEST |
| `-402` | ILLEGAL_APP_REQUEST |
| `-403` | ILLEGAL_SIGNATURE_REQUEST |
| `-405` | ILLEGAL_CLIENT_REQUEST |
| `-429` | LIMIT_REQUEST_REACH |
| `-500` | SYSTEM_ERROR |

## Ví dụ response

```json
{
  "return_code": 1,
  "return_message": "SUCCESS",
  "sub_return_code": 1,
  "sub_return_message": "SUCCESS",
  "binding_token": "...",
  "binding_url": "https://...",
  "reform_url": "https://..."
}
```

## Lưu ý

- `req_date` chỉ có hiệu lực trong 15 phút kể từ thời điểm tạo, request quá hạn sẽ bị từ chối.
- Với `binding_mode = BIND_AND_PAY`, cần truyền đầy đủ `payment_data` để xử lý thanh toán ngay sau khi liên kết thành công.
- HTTP status trả về luôn là `200 OK`; trạng thái thực tế dựa vào `return_code`.
