# API Hybrid Payment (Thanh toán linh hoạt token + cổng thanh toán)

Nguồn: https://docs.zalopay.vn/docs/specs/hybrid-payment

## Tổng quan

API Hybrid Payment cho phép merchant thực hiện thanh toán bằng `pay_token` đã liên kết, đồng thời cung cấp phương án dự phòng (fallback) chuyển hướng người dùng sang cổng thanh toán Zalopay Gateway nếu thanh toán bằng token không thực hiện được.

- **Method:** POST
- **Endpoint:** `/hybrid-payment`

## Request Parameters

| Tham số | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|
| `app_id` | int64 | Có | ID do Zalopay cấp cho merchant/ứng dụng |
| `identifier` | string | Có | Định danh người dùng trên hệ thống merchant (user ID, số điện thoại, email, ...) |
| `pay_token` | string | Có | Token công khai của người dùng (lấy từ [API Agreement Query](./agreement-query.md)) |
| `app_user` | string | Có | ID của merchant |
| `app_trans_id` | string(40) | Có | Mã giao dịch duy nhất, định dạng `yyMMddxxxxxxxxx` |
| `app_time` | int64 | Có | Thời điểm tạo đơn hàng, tính bằng Unix timestamp (milliseconds); chênh lệch tối đa 15 phút |
| `amount` | int64 | Có | Số tiền đơn hàng (VND) |
| `description` | string | Có | Mô tả hiển thị trên màn hình xác nhận thanh toán |
| `item` | string | Có | Chuỗi JSON array mô tả sản phẩm trong đơn hàng |
| `embed_data` | string | Có | Chuỗi JSON object chứa thông tin đơn hàng: `preferred_payment_method`, `redirecturl`, `columninfo`, `promotioninfo`, `zlppaymentid` |
| `mac` | string | Có | Chữ ký xác thực HMAC (xem [Tính toán mac](#tính-toán-mac)) |

## Tính toán mac

```
mac = HMAC_SHA256(key1, app_id|app_trans_id|app_user|amount|app_time|embed_data|item)
```

- Thuật toán mặc định: `HmacSHA256`
- `key1` do Zalopay cấp khi đăng ký merchant
- Công thức tương tự [API CreateOrder](./order-create.md#tính-toán-mac)

> Xem thêm chi tiết tại [Secure Data Transmission](../integration-guides/developer-tools/security-secure-data-transmission.md#hmac)

## Response Fields

| Field | Kiểu | Mô tả |
|---|---|---|
| `return_code` | int | `1`=Success, `2`=Failed, `3`=Processing |
| `return_message` | string | Mô tả trạng thái xử lý |
| `sub_return_code` | int | Mã trạng thái chi tiết |
| `sub_return_message` | string | Mô tả mã trạng thái chi tiết |
| `app_trans_id` | string | Mã giao dịch của đơn hàng |
| `zp_trans_id` | int | Mã giao dịch của Zalopay |
| `solution_url` | string | URL redirect đến trang thanh toán Zalopay Gateway (trường hợp fallback) |

## Lưu ý

- Nếu thanh toán bằng `pay_token` không khả dụng, merchant nên dùng `solution_url` để chuyển người dùng sang luồng thanh toán qua Zalopay Gateway.
- HTTP status trả về `200 OK` khi thành công, `405` khi dữ liệu request không hợp lệ.
