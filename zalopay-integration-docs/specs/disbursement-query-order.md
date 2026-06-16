# API Disbursement Query Order (Truy vấn trạng thái đơn chi hộ)

Nguồn: https://docs.zalopay.vn/docs/specs/disbursement-query-order

## Tổng quan

API Query Order cho phép partner truy vấn trạng thái hiện tại của một giao dịch chi hộ đã gửi qua [API Topup](./disbursement-topup.md).

- **Method:** POST
- **Endpoint:** `/disbursement-query-order`
- Hỗ trợ Content-Type: `application/json`, `application/xml`, `application/x-www-form-urlencoded`

## Request Parameters

| Tham số | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|
| `app_id` | int64 | Có | ID do Zalopay cấp cho partner |
| `partner_order_id` | string | Có | Mã đơn hàng do partner tự sinh khi gọi [API Topup](./disbursement-topup.md) |
| `time` | int64 | Có | Thời điểm gửi request, tính bằng Unix timestamp (milliseconds) |
| `mac` | string | Có | Chữ ký xác thực HMAC (xem [Tính toán mac](#tính-toán-mac)) |

## Tính toán mac

```
mac = HMAC_SHA256(key1, app_id|partner_order_id|time)
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
| `data.zp_trans_id` | string | Mã giao dịch của Zalopay |
| `data.result_url` | string | URL nhận thông báo kết quả chi hộ |

## Mã lỗi

| `sub_return_code` | Ý nghĩa |
|---|---|
| `-101` | Không tìm thấy đơn hàng |
| `-401` | Tham số request không hợp lệ |
| `-402` | Không có quyền truy cập (Unauthorized) |
| `-500` | Lỗi hệ thống Zalopay |
| `-503` | Hệ thống đang bảo trì |

## Lưu ý

- `data.status = 3` (PROCESSING) hoặc `4` (PENDING): partner nên gọi lại API này theo định kỳ cho đến khi nhận trạng thái cuối cùng.
