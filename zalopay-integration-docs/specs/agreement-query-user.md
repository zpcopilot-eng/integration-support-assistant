# API Agreement Query User (Truy vấn thông tin cơ bản người dùng)

Nguồn: https://docs.zalopay.vn/docs/specs/agreement-query-user

## Tổng quan

API Agreement Query User cho phép merchant truy vấn thông tin cơ bản (số điện thoại đã ẩn) của người dùng đã có liên kết thanh toán đang hoạt động.

- **Method:** POST
- **Endpoint:** `/agreement-query-user`

## Request Parameters

| Tham số | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|
| `app_id` | int64 | Có | ID do Zalopay cấp cho merchant/ứng dụng |
| `access_token` | string | Không | Access token của người dùng sau khi liên kết, tương đương giá trị `pay_token` |
| `req_date` | int64 | Có | Thời điểm gửi request, tính bằng Unix timestamp (milliseconds) |
| `mac` | string | Có | Chữ ký xác thực HMAC (xem [Tính toán mac](#tính-toán-mac)) |

## Tính toán mac

```
mac = HMAC_SHA256(key1, app_id|access_token|req_date)
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
| `phone` | string | Số điện thoại người dùng đã ẩn một phần (ví dụ: `****1234`) |

## Ví dụ response

```json
{
  "return_code": 1,
  "return_message": "SUCCESS",
  "sub_return_code": 1,
  "sub_return_message": "SUCCESS",
  "phone": "****1234"
}
```

## Lưu ý

- HTTP status trả về `200 OK` khi thành công, `405` khi dữ liệu request không hợp lệ.
