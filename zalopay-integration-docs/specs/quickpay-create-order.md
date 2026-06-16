# API QuickPay Create Order (Thu tiền bằng quét mã QR người dùng)

Nguồn: https://docs.zalopay.vn/docs/specs/quickpay-create-order

## Tổng quan

API QuickPay dùng cho mô hình thu tiền tại điểm bán: thu ngân (merchant cashier) quét mã QR hiển thị trên app Zalopay của khách hàng để trừ tiền trực tiếp.

- **Method:** POST
- **Endpoint:** `/v2/quickpay/create`

## Request Parameters

### Tham số bắt buộc

| Tham số | Kiểu | Mô tả |
|---|---|---|
| `app_id` | int | ID do Zalopay cấp cho merchant/ứng dụng |
| `app_user` | string(50) | Định danh người dùng; dùng tên ứng dụng nếu không có |
| `app_time` | int64 | Thời điểm tạo đơn hàng, tính bằng Unix timestamp (milliseconds) |
| `amount` | int64 | Số tiền đơn hàng (VND) |
| `app_trans_id` | string(40) | Mã giao dịch, định dạng `yymmdd_OrderID` |
| `embed_data` | string(1024) | Chuỗi JSON dữ liệu mở rộng; dùng `"{}"` nếu trống. Hỗ trợ: `redirecturl`, `columninfo`, `promotioninfo`, `zlppaymentid` |
| `item` | string(1024) | Chuỗi JSON array thông tin sản phẩm; dùng `"[]"` nếu trống |
| `payment_code` | string | Mã QR quét từ app Zalopay của khách hàng, đã được mã hóa RSA bằng public key của merchant |
| `mac` | string | Chữ ký xác thực HMAC (xem [Tính toán mac](#tính-toán-mac)) |

### Tham số không bắt buộc

| Tham số | Kiểu | Mô tả |
|---|---|---|
| `description` | string(100) | Mô tả đơn hàng hiển thị khi thanh toán |
| `callback_url` | string | URL nhận callback kết quả thanh toán |
| `redirect_url` | string | URL điều hướng sau khi thanh toán |
| `device_info` | string(256) | Chuỗi JSON mô tả thiết bị |
| `currency` | string | Đơn vị tiền tệ, mặc định `VND` |
| `title` | string | Tiêu đề đơn hàng |
| `userIP` | string | Địa chỉ IP của người dùng |

## Tính toán mac

```
mac = HMAC_SHA256(key1, app_id|app_trans_id|app_user|amount|app_time|embed_data|item|paymentCodeRaw)
```

- Thuật toán mặc định: `HmacSHA256`
- `key1` do Zalopay cấp khi đăng ký merchant
- `paymentCodeRaw`: dữ liệu gốc của mã QR trước khi mã hóa RSA

> Xem thêm chi tiết tại [Secure Data Transmission](../integration-guides/developer-tools/security-secure-data-transmission.md#hmac)

## Response Fields

| Field | Kiểu | Mô tả |
|---|---|---|
| `return_code` | int | `1`=Success, `2`=Failure, `3`=Processing |
| `return_message` | string | Mô tả trạng thái xử lý |
| `sub_return_code` | int | Mã trạng thái chi tiết |
| `sub_return_message` | string | Mô tả chi tiết trạng thái đơn hàng |
| `is_processing` | boolean | `true`=đang xử lý, `false`=đã hoàn tất |
| `zp_trans_id` | int64 | Mã giao dịch của Zalopay |

## Lưu ý

- `return_code = 3` (Processing) hoặc `is_processing = true`: merchant nên dùng [API QueryOrder](./order-query.md) với `app_trans_id` để xác nhận kết quả cuối cùng.
- `payment_code` cần được mã hóa RSA bằng public key của merchant trước khi gửi lên Zalopay.
