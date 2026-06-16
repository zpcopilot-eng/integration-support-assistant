# API Tokenization Query (Truy vấn trạng thái liên kết)

Nguồn: https://docs.zalopay.vn/docs/specs/tokenization-query

## Tổng quan

API Tokenization Query dùng để truy vấn trạng thái và thông tin của một yêu cầu liên kết (binding) đã tạo qua [API Tokenization Bind](./tokenization-bind.md).

- **Method:** POST
- **Endpoint:** `/tokenization-query`

## Request Parameters

| Tham số | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|
| `app_id` | int64 | Có | ID do Zalopay cấp cho merchant/ứng dụng |
| `app_trans_id` | string(40) | Có | Mã giao dịch (`app_trans_id`) đã dùng khi gọi API Tokenization Bind, định dạng `yyMMddxxxxxxxxx` |
| `req_date` | int64 | Có | Thời điểm gửi request, tính bằng Unix timestamp (milliseconds) |
| `mac` | string | Có | Chữ ký xác thực HMAC (xem [Tính toán mac](#tính-toán-mac)) |

## Tính toán mac

```
mac = HMAC_SHA256(key1, app_id|app_trans_id|req_date)
```

- Thuật toán mặc định: `HmacSHA256`
- `key1` do Zalopay cấp khi đăng ký merchant

> Xem thêm chi tiết tại [Secure Data Transmission](../integration-guides/developer-tools/security-secure-data-transmission.md#hmac)

## Response Fields

| Field | Kiểu | Mô tả |
|---|---|---|
| `return_code` | int | `1`=SUCCESS, `2`=FAILED, `3`=PENDING |
| `return_message` | string | Mô tả trạng thái xử lý |
| `sub_return_code` | int | Mã trạng thái chi tiết |
| `sub_return_message` | string | Mô tả mã trạng thái chi tiết |
| `binding_token` | string | Token của giao dịch liên kết |
| `binding_qr_link` | string | URL QR code dùng cho liên kết |
| `deep_link` | string | Deep link mở app merchant |
| `short_link` | string | URL rút gọn |
| `order_no` | int | Số thứ tự đơn hàng |
| `order_token` | string | Token của đơn hàng (nếu `binding_mode = BIND_AND_PAY`) |
| `order_url` | string | URL đơn hàng |
| `zp_trans_id` | string | Mã giao dịch của Zalopay |
| `status` | int | Mã trạng thái giao dịch |

## Ví dụ response

```json
{
  "return_code": 1,
  "return_message": "SUCCESS",
  "sub_return_code": 1,
  "sub_return_message": "SUCCESS",
  "binding_token": "...",
  "status": 1
}
```

## Lưu ý

- HTTP status code có thể trả về `200` (thành công) hoặc `405` (input không hợp lệ).
- `return_code = 3` (PENDING) nghĩa là người dùng chưa hoàn tất quy trình liên kết; merchant nên gọi lại API này định kỳ để kiểm tra.
