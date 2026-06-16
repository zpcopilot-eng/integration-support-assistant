# API Agreement Unbind (Hủy liên kết thanh toán định kỳ)

Nguồn: https://docs.zalopay.vn/docs/specs/agreement-unbind

## Tổng quan

API Agreement Unbind dùng để hủy một liên kết (binding) đã được tạo trước đó qua [API Agreement Bind](./agreement-bind.md).

- **Method:** POST
- **Endpoint:** `/agreement-unbind`

## Request Parameters

| Tham số | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|
| `app_id` | int64 | Có | ID do Zalopay cấp cho merchant/ứng dụng |
| `identifier` | string | Có | Định danh người dùng trên hệ thống merchant (user ID, số điện thoại, email, ...) |
| `binding_id` | string | Có | ID của liên kết cần hủy (nhận từ API Agreement Bind/Query) |
| `req_date` | int64 | Có | Thời điểm tạo request, tính bằng Unix timestamp (milliseconds); chênh lệch tối đa 15 phút |
| `mac` | string | Có | Chữ ký xác thực HMAC (xem [Tính toán mac](#tính-toán-mac)) |

## Tính toán mac

```
mac = HMAC_SHA256(key1, app_id|identifier|binding_id|req_date)
```

- Thuật toán mặc định: `HmacSHA256`
- `key1` do Zalopay cấp khi đăng ký merchant

> Xem thêm chi tiết tại [Secure Data Transmission](../integration-guides/developer-tools/security-secure-data-transmission.md#hmac)

## Response Fields

| Field | Kiểu | Mô tả |
|---|---|---|
| `return_code` | int | `1`=Success, `2`=Failed |
| `return_message` | string | Mô tả trạng thái xử lý |
| `sub_return_code` | int | Mã trạng thái chi tiết |
| `sub_return_message` | string | Mô tả mã trạng thái chi tiết |

## Lưu ý

- HTTP status trả về `200 OK` khi xử lý thành công, `405` khi dữ liệu request không hợp lệ.
- Sau khi unbind, `pay_token` tương ứng với `binding_id` sẽ không còn hiệu lực cho [API Agreement Pay](./agreement-pay.md).
