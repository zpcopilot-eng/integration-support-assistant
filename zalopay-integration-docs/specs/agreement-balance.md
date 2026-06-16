# API Agreement Balance (Truy vấn khả năng thanh toán)

Nguồn: https://docs.zalopay.vn/docs/specs/agreement-balance

## Tổng quan

API Agreement Balance cho phép merchant kiểm tra số dư và khả năng thanh toán của người dùng (dựa trên `pay_token` đã liên kết) trước khi thực hiện thanh toán qua [API Agreement Pay](./agreement-pay.md).

- **Method:** POST
- **Endpoint:** `/agreement-balance`

## Request Parameters

| Tham số | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|
| `app_id` | int64 | Có | ID do Zalopay cấp cho merchant/ứng dụng |
| `identifier` | string | Có | Định danh người dùng trên hệ thống merchant (user ID, số điện thoại, email, ...) |
| `pay_token` | string | Có | Token công khai của người dùng (lấy từ [API Agreement Query](./agreement-query.md)) |
| `amount` | int64 | Có | Số tiền dự kiến thanh toán (VND) |
| `req_date` | int64 | Có | Thời điểm gửi request, tính bằng Unix timestamp (milliseconds) |
| `mac` | string | Có | Chữ ký xác thực HMAC (xem [Tính toán mac](#tính-toán-mac)) |

## Tính toán mac

```
mac = HMAC_SHA256(key1, app_id|pay_token|identifier|amount|req_date)
```

- Thuật toán mặc định: `HmacSHA256`
- `key1` do Zalopay cấp khi đăng ký merchant

> Xem thêm chi tiết tại [Secure Data Transmission](../integration-guides/developer-tools/security-secure-data-transmission.md#hmac)

## Response Fields

| Field | Kiểu | Mô tả |
|---|---|---|
| `return_code` | int | `1`=Success, các giá trị khác=Failed |
| `return_message` | string | Mô tả trạng thái xử lý |
| `sub_return_code` | int | Mã trạng thái chi tiết |
| `sub_return_message` | string | Mô tả mã trạng thái chi tiết |
| `data` | array | Danh sách kênh thanh toán, mỗi item gồm: `channel` (int64), `payable` (boolean), `bank_code` (string) |
| `discount_amount` | int64 | Số tiền giảm giá tốt nhất từ voucher hiện có; `0` nếu không có |

## Ví dụ response

```json
{
  "return_code": 1,
  "return_message": "SUCCESS",
  "sub_return_code": 1,
  "sub_return_message": "SUCCESS",
  "data": [
    { "channel": 38, "payable": true, "bank_code": "" }
  ],
  "discount_amount": 0
}
```

## Lưu ý

- HTTP status trả về `200 OK` khi thành công, `405` khi dữ liệu request không hợp lệ.
- Nên gọi API này trước khi gọi [API Agreement Pay](./agreement-pay.md) để đảm bảo người dùng có đủ khả năng thanh toán cho `amount` dự kiến.
