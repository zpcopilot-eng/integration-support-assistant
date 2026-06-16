# API Agreement Bind (Tạo liên kết thanh toán định kỳ)

Nguồn: https://docs.zalopay.vn/docs/specs/agreement-bind

## Tổng quan

API Agreement Bind dùng để tạo một liên kết (binding) mới giữa người dùng và merchant, phục vụ cho các giao dịch thanh toán tự động/định kỳ (agreement) sau này.

- **Method:** POST
- **Endpoint:** `/agreement-bind`

## Request Parameters

| Tham số | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|
| `app_id` | int64 | Có | ID do Zalopay cấp cho merchant/ứng dụng |
| `app_trans_id` | string(40) | Có | Mã giao dịch duy nhất, định dạng `yyMMddxxxxxxxxx` |
| `req_date` | int64 | Có | Thời điểm tạo request, tính bằng Unix timestamp (milliseconds); chênh lệch tối đa 15 phút |
| `identifier` | string | Có | Định danh người dùng trên hệ thống merchant (user ID, số điện thoại, email, ...) |
| `max_amount` | int64 | Không | Số tiền tối đa được phép thanh toán tự động; mặc định là số dư thực tế của người dùng |
| `redirect_url` | string | Không | URL redirect sau khi liên kết hoàn tất (cho web/desktop) |
| `redirect_deep_link` | string | Không | Deep link mở app merchant sau khi liên kết hoàn tất (cho mobile) |
| `binding_data` | string | Không | Chuỗi JSON chứa thông tin bổ sung cho liên kết |
| `binding_type` | string | Không | Loại liên kết, mặc định là `WALLET` nếu không truyền |
| `callback_url` | string | Không | URL nhận callback kết quả liên kết (TBD) |
| `mac` | string | Có | Chữ ký xác thực HMAC (xem [Tính toán mac](#tính-toán-mac)) |

## Tính toán mac

```
mac = HMAC_SHA256(key1, app_id|app_trans_id|binding_data|binding_type|identifier|max_amount|req_date)
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
| `binding_id` | string | ID của liên kết được tạo |
| `binding_url` | string | URL để người dùng hoàn tất liên kết |

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

## Lưu ý

- Cần cung cấp một trong hai: `redirect_url` (web/desktop) hoặc `redirect_deep_link` (mobile) để điều hướng người dùng sau khi liên kết.
- Sau khi liên kết thành công, dùng [API Agreement Query](./agreement-query.md) để lấy `pay_token` phục vụ thanh toán qua [API Agreement Pay](./agreement-pay.md).
