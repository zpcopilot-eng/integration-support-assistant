# API Agreement Pay (Thanh toán bằng token đã liên kết)

Nguồn: https://docs.zalopay.vn/docs/specs/agreement-pay

## Tổng quan

API Agreement Pay cho phép merchant thực hiện thanh toán (charge-on-file) cho người dùng đã liên kết, sử dụng `pay_token` từ [API Agreement Query](./agreement-query.md) kết hợp với `zp_trans_token` từ [API CreateOrder](./order-create.md).

- **Method:** POST
- **Endpoint:** `/agreement-pay`

## Request Parameters

| Tham số | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|
| `app_id` | int64 | Có | ID do Zalopay cấp cho merchant/ứng dụng |
| `identifier` | string | Có | Định danh người dùng trên hệ thống merchant (user ID, số điện thoại, email, ...) |
| `zp_trans_token` | string | Có | Token giao dịch được sinh ra từ [API CreateOrder](./order-create.md) (field `zp_trans_token`) |
| `pay_token` | string | Có | Token công khai của người dùng (lấy từ [API Agreement Query](./agreement-query.md)) |
| `req_date` | int64 | Có | Thời điểm gửi request, tính bằng Unix timestamp (milliseconds) |
| `mac` | string | Có | Chữ ký xác thực HMAC (xem [Tính toán mac](#tính-toán-mac)) |

## Tính toán mac

```
mac = HMAC_SHA256(key1, app_id|identifier|zp_trans_token|pay_token|req_date)
```

- Thuật toán mặc định: `HmacSHA256`
- `key1` do Zalopay cấp khi đăng ký merchant

> Xem thêm chi tiết tại [Secure Data Transmission](../integration-guides/developer-tools/security-secure-data-transmission.md#hmac)

## Response Fields

| Field | Kiểu | Mô tả |
|---|---|---|
| `return_code` | int | `1`=Success, `2`=Failed, `3`=Processing |
| `return_message` | string | Mô tả trạng thái xử lý |
| `sub_return_code` | int | Mã trạng thái chi tiết |
| `sub_return_message` | string | Mô tả mã trạng thái chi tiết |
| `app_trans_id` | string | Mã giao dịch (`app_trans_id`) của đơn hàng (TXID) |
| `zp_trans_id` | int | Mã giao dịch của Zalopay |

## Ví dụ response

```json
{
  "return_code": 1,
  "return_message": "SUCCESS",
  "sub_return_code": 1,
  "sub_return_message": "SUCCESS",
  "app_trans_id": "240101_OrderID",
  "zp_trans_id": 220603000000789
}
```

## Lưu ý

- Trước khi gọi API này, cần tạo đơn hàng qua [API CreateOrder](./order-create.md) để lấy `zp_trans_token`.
- `return_code = 3` (Processing): merchant nên dùng [API QueryOrder](./order-query.md) với `app_trans_id` để xác nhận kết quả cuối cùng.
- HTTP status trả về `200 OK` khi thành công, `405` khi dữ liệu request không hợp lệ.
