# API Agreement Query (Truy vấn token thanh toán định kỳ)

Nguồn: https://docs.zalopay.vn/docs/specs/agreement-query

## Tổng quan

API Agreement Query dùng để truy vấn `pay_token` (token thanh toán công khai) của một liên kết (binding) đã được người dùng xác nhận, dùng cho các giao dịch thanh toán tự động (auto-debit) sau này qua [API Agreement Pay](./agreement-pay.md).

- **Method:** POST
- **Endpoint:** `/agreement-query`

## Request Parameters

| Tham số | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|
| `app_id` | int64 | Có | ID do Zalopay cấp cho merchant/ứng dụng |
| `app_trans_id` | string(40) | Có | Mã giao dịch (`app_trans_id`) đã dùng khi gọi [API Agreement Bind](./agreement-bind.md), định dạng `yyMMddxxxxxxxxx` |
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
| `data.app_id` | int64 | ID ứng dụng merchant |
| `data.app_trans_id` | string | Mã giao dịch liên kết của merchant |
| `data.binding_id` | string | ID liên kết do Zalopay xác nhận |
| `data.pay_token` | string | Token công khai dùng cho thanh toán tự động (auto-debit) |
| `data.server_time` | int64 | Thời gian server Zalopay (Unix timestamp, giây) |
| `data.merchant_user_id` | string | Định danh người dùng từ request Bind ban đầu |
| `data.status` | int | `1`=Confirmed, `3`=Cancelled, `4`=Disabled |
| `data.msg_type` | int | `1`=Người dùng xác nhận liên kết, `2`=Người dùng cập nhật agreement |
| `data.zp_user_id` | string | Định danh người dùng trong hệ thống Zalopay theo từng app |
| `data.masked_user_phone` | string | Số điện thoại đã ẩn một phần (ví dụ: `****6938`) |

## Ví dụ response

```json
{
  "return_code": 1,
  "return_message": "SUCCESS",
  "sub_return_code": 1,
  "sub_return_message": "SUCCESS",
  "data": {
    "app_id": 123,
    "app_trans_id": "240101_OrderID",
    "binding_id": "...",
    "pay_token": "...",
    "server_time": 1654234567,
    "merchant_user_id": "user123",
    "status": 1,
    "msg_type": 1,
    "zp_user_id": "...",
    "masked_user_phone": "****6938"
  }
}
```

## Lưu ý

- HTTP status trả về `200 OK` khi thành công, `405` khi dữ liệu request không hợp lệ.
- `data.status = 1` (Confirmed) là điều kiện cần để sử dụng `pay_token` cho [API Agreement Pay](./agreement-pay.md) hoặc [API Agreement Balance](./agreement-balance.md).
