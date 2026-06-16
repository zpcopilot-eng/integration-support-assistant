# API Disbursement Topup (Chi hộ vào ví người dùng)

Nguồn: https://docs.zalopay.vn/docs/specs/disbursement-topup

## Tổng quan

API Topup cho phép partner chuyển tiền (nạp tiền) vào ví Zalopay của người dùng, dùng trong nghiệp vụ chi hộ/giải ngân. Trước khi gọi API này cần dùng [API Query User](./disbursement-query-user.md) để lấy `m_u_id`.

- **Method:** POST
- **Endpoint:** `/disbursement-topup`

## Request Parameters

| Tham số | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|
| `app_id` | int64 | Có | ID do Zalopay cấp cho partner |
| `payment_id` | string | Có | ID thanh toán do Zalopay cấp cho partner khi đăng ký |
| `partner_order_id` | string | Có | Mã đơn hàng duy nhất do partner tự sinh, dùng để đối soát |
| `m_u_id` | string | Có | Định danh người dùng (lấy từ response của [API Query User](./disbursement-query-user.md)) |
| `amount` | int64 | Có | Số tiền chuyển vào ví người nhận (VND) |
| `description` | string | Có | Thông tin mô tả giao dịch |
| `partner_embed_data` | string | Có | Chuỗi JSON chứa thông tin bổ sung của partner (ví dụ: `store_id`, `store_name`) |
| `reference_id` | string | Không | Reference ID của Zalopay (lấy từ response của API Query User) |
| `extra_info` | string | Có | Chuỗi JSON cho các thông tin mở rộng khác |
| `time` | int64 | Có | Thời điểm gửi request, tính bằng Unix timestamp (milliseconds) |
| `sig` | string | Có | Chữ ký xác thực (xem [Tính toán sig](#tính-toán-sig)) |

## Tính toán sig

```
hmacinput = app_id|payment_id|partner_order_id|m_u_id|amount|description|partner_embed_data|extra_info|time
sig = RSA_Sign(private_key, HMAC_SHA256(key1, hmacinput))
```

- Bước 1: Tính `HmacSHA256` của `hmacinput` với `key1` (hmac key của app)
- Bước 2: Ký kết quả ở bước 1 bằng RSA với private key của app

> Xem thêm chi tiết tại [Secure Data Transmission](../integration-guides/developer-tools/security-secure-data-transmission.md#hmac)

## Response Fields

| Field | Kiểu | Mô tả |
|---|---|---|
| `return_code` | int | `1`=SUCCESS, `2`=FAIL |
| `return_message` | string | Mô tả trạng thái xử lý |
| `sub_return_code` | int | Mã trạng thái chi tiết (xem [Mã lỗi](#mã-lỗi)) |
| `sub_return_message` | string | Mô tả mã trạng thái chi tiết |
| `data.order_id` | string | Mã giao dịch của partner |
| `data.status` | int | `1`=SUCCESS, `2`=FAIL, `3`=PROCESSING, `4`=PENDING |
| `data.m_u_id` | string | Định danh người dùng |
| `data.phone` | string | Số điện thoại người dùng |
| `data.amount` | int64 | Số tiền giao dịch |
| `data.description` | string | Mô tả giao dịch |
| `data.partner_fee` | int64 | Phí của partner |
| `data.zlp_fee` | int64 | Phí của Zalopay |
| `data.extra_info` | string | Chuỗi JSON thông tin mở rộng |
| `data.time` | int64 | Thời gian giao dịch (Unix timestamp, milliseconds) |
| `data.upgrade_url` | string | URL nâng hạn mức nạp tiền (khi cần) |

## Mã lỗi

| `sub_return_code` | Ý nghĩa |
|---|---|
| `-68` | Trùng resource (duplicate) |
| `-101` | Tài khoản ví người dùng không tồn tại |
| `-401` | Tham số request không hợp lệ |
| `-402` | Không có quyền truy cập (Unauthorized) |
| `-406` | Tài khoản ví người dùng đã đạt hạn mức nạp tiền |
| `-500` | Lỗi hệ thống Zalopay |
| `-503` | Hệ thống đang bảo trì |

## Lưu ý

- `data.status = 3` (PROCESSING) hoặc `4` (PENDING): partner nên dùng [API Query Order](./disbursement-query-order.md) với `partner_order_id` để theo dõi kết quả cuối cùng.
- `sub_return_code = -406`: hướng dẫn người dùng dùng `data.upgrade_url` để nâng hạn mức nạp tiền.
