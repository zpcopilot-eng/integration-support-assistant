# API Callback (Thông báo kết quả thanh toán)

Nguồn: https://docs.zalopay.vn/docs/specs/callback-api

## Tổng quan

Sau khi đơn hàng được thanh toán thành công, Zalopay gửi callback (server-to-server) đến `callback_url` mà merchant đã đăng ký (truyền trong [API CreateOrder](./order-create.md)) để thông báo kết quả thanh toán.

- **Method:** POST
- **Endpoint:** URL do merchant đăng ký (callback URL), Content-Type: `application/json`

## Request từ Zalopay gửi đến Merchant

| Field | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|
| `data` | string | Có | Chuỗi JSON chứa thông tin chi tiết giao dịch (xem [Cấu trúc `data`](#cấu-trúc-data)) |
| `mac` | string | Có | Chữ ký xác thực HMAC của `data` (xem [Tính toán mac](#tính-toán-mac)) |
| `type` | int | Có | Loại callback: `1`=Order, `2`=Agreement |

### Cấu trúc `data`

| Field | Kiểu | Mô tả |
|---|---|---|
| `app_id` | int | ID ứng dụng của merchant |
| `app_trans_id` | string | Mã giao dịch của merchant |
| `app_time` | long | Thời gian tạo đơn hàng |
| `app_user` | string | Định danh người dùng từ merchant |
| `amount` | long | Số tiền thanh toán (VND) |
| `embed_data` | string | Chuỗi JSON dữ liệu mở rộng do merchant truyền khi tạo đơn |
| `item` | string | Chuỗi JSON array thông tin sản phẩm |
| `zp_trans_id` | long | Mã giao dịch của Zalopay |
| `server_time` | long | Thời gian xử lý tại Zalopay (Unix timestamp, milliseconds) |
| `channel` | int | Kênh thanh toán đã sử dụng |
| `merchant_user_id` | string | ID người dùng trong hệ thống Zalopay |
| `user_fee_amount` | long | Phí người dùng phải trả (VND) |
| `discount_amount` | long | Số tiền giảm giá (VND) |

## Tính toán mac

```
mac = HMAC_SHA256(key2, data)
```

- Thuật toán mặc định: `HmacSHA256`
- `key2` (callback key) do Zalopay cấp khi đăng ký merchant
- Input chính là giá trị chuỗi của field `data`

> Xem thêm chi tiết tại [Secure Data Transmission](../integration-guides/developer-tools/security-secure-data-transmission.md#hmac) và [Knowledge Base Callback](../integration-guides/developer-tools/knowledge-base-callback.md#security-validation)

## Response merchant cần trả về

| Field | Kiểu | Mô tả |
|---|---|---|
| `return_code` | int | `1`=Success (đã xác nhận callback hợp lệ), `2`=Invalid |
| `return_message` | string | `"Success"` hoặc `"Invalid"` |

## Ví dụ response

```json
{
  "return_code": 1,
  "return_message": "Success"
}
```

## Lưu ý

- Merchant **bắt buộc** phải verify `mac` bằng `key2` trước khi xử lý callback, để đảm bảo request thực sự đến từ Zalopay.
- Nếu merchant trả `return_code = 2` hoặc không phản hồi, Zalopay sẽ gửi lại callback theo cơ chế retry.
- Nên kết hợp dùng [API QueryOrder](./order-query.md) để xác nhận trạng thái đơn hàng, tránh trường hợp callback bị mất do lỗi mạng.
