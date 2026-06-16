# API Disbursement Query User (Truy vấn tài khoản người dùng)

Nguồn: https://docs.zalopay.vn/docs/specs/disbursement-query-user

## Tổng quan

API Query User dùng trong nghiệp vụ chi hộ/giải ngân (disbursement), cho phép partner truy vấn thông tin tài khoản Zalopay của người dùng theo số điện thoại trước khi thực hiện [API Topup](./disbursement-topup.md).

- **Method:** POST
- **Endpoint:** `/disbursement-query-user`

## Request Parameters

| Tham số | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|
| `request_id` | string | Không | ID request của client, dùng để tracing |
| `app_id` | int64 | Có | ID do Zalopay cấp cho partner |
| `phone` | string | Có | Số điện thoại của người dùng cần truy vấn |
| `time` | int64 | Có | Thời điểm gửi request, tính bằng Unix timestamp (milliseconds) |
| `mac` | string | Có | Chữ ký xác thực HMAC (xem [Tính toán mac](#tính-toán-mac)) |

## Tính toán mac

```
mac = HMAC_SHA256(key1, app_id|phone|time)
```

- Thuật toán mặc định: `HmacSHA256`
- `key1` do Zalopay cấp khi đăng ký partner

> Xem thêm chi tiết tại [Secure Data Transmission](../integration-guides/developer-tools/security-secure-data-transmission.md#hmac)

## Response Fields

| Field | Kiểu | Mô tả |
|---|---|---|
| `return_code` | int | `1`=SUCCESS, `2`=FAIL |
| `return_message` | string | Mô tả trạng thái xử lý |
| `sub_return_code` | int | Mã trạng thái chi tiết (xem [Mã lỗi](#mã-lỗi)) |
| `sub_return_message` | string | Mô tả mã trạng thái chi tiết |
| `data.reference_id` | string | Reference ID của Zalopay |
| `data.m_u_id` | string | Định danh người dùng trong hệ thống Zalopay |
| `data.name` | string | Họ tên người dùng |
| `data.phone` | string | Số điện thoại người dùng |
| `data.onboarding_url` | string | URL onboarding (dành cho người dùng chưa có tài khoản Zalopay) |

## Mã lỗi

| `sub_return_code` | Ý nghĩa |
|---|---|
| `-101` | Tài khoản ví người dùng không tồn tại |
| `-401` | Tham số request không hợp lệ |
| `-402` | Không có quyền truy cập (Unauthorized) |
| `-500` | Lỗi hệ thống Zalopay |
| `-503` | Hệ thống đang bảo trì |
| `-1011` | Tài khoản ví người dùng đã bị khóa |

## Lưu ý

- Kết quả `data.m_u_id` và `data.reference_id` được dùng làm tham số đầu vào cho [API Topup](./disbursement-topup.md).
- Nếu người dùng chưa có tài khoản Zalopay, dùng `data.onboarding_url` để hướng dẫn đăng ký.
