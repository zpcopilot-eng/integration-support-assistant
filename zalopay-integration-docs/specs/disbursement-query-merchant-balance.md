# API Disbursement Query Merchant Balance (Truy vấn số dư tài khoản đối tác)

Nguồn: https://docs.zalopay.vn/docs/specs/disbursement-query-merchant-balance

## Tổng quan

API Query Merchant Balance cho phép partner truy vấn số dư hiện tại trong tài khoản chi hộ của mình tại Zalopay.

- **Method:** POST
- **Endpoint:** `/disbursement-query-merchant-balance`

## Request Parameters

| Tham số | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|
| `request_id` | string | Không | ID request của client, dùng để tracing |
| `app_id` | int64 | Có | ID do Zalopay cấp cho partner |
| `payment_id` | string | Có | ID thanh toán do Zalopay cấp cho partner khi đăng ký |
| `time` | int64 | Có | Thời điểm gửi request, tính bằng Unix timestamp (milliseconds) |
| `mac` | string | Có | Chữ ký xác thực HMAC (xem [Tính toán mac](#tính-toán-mac)) |

## Tính toán mac

```
mac = HMAC_SHA256(key1, app_id|payment_id|time)
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
| `data.balance` | int64 | Số dư hiện tại của tài khoản partner |

## Mã lỗi

| `sub_return_code` | Ý nghĩa |
|---|---|
| `-401` | Tham số request không hợp lệ |
| `-402` | Không có quyền truy cập (Unauthorized) |
| `-500` | Lỗi hệ thống Zalopay |
| `-503` | Hệ thống đang bảo trì |

## Lưu ý

- Nên kiểm tra `data.balance` trước khi gọi [API Topup](./disbursement-topup.md) với số tiền lớn để tránh lỗi do số dư không đủ.
