# API Query Order (Truy vấn trạng thái đơn hàng)

Nguồn: https://docs.zalopay.vn/docs/specs/order-query

## Tổng quan

API QueryOrder dùng để merchant truy vấn trạng thái thanh toán của một đơn hàng đã tạo qua [API CreateOrder](./order-create.md), đặc biệt trong trường hợp không nhận được callback từ Zalopay.

- **Method:** POST
- **Endpoint:** `/v2/query`

## Request Parameters

| Tham số | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|
| `app_id` | int32 | Có | ID do Zalopay cấp cho merchant/ứng dụng |
| `app_trans_id` | string | Có | Mã giao dịch (`app_trans_id`) của đơn hàng cần truy vấn, định dạng `yymmdd_OrderID` |
| `mac` | string | Có | Chữ ký xác thực HMAC (xem [Tính toán mac](#tính-toán-mac)) |

## Tính toán mac

```
mac = HMAC_SHA256(key1, app_id|app_trans_id)
```

- Thuật toán mặc định: `HmacSHA256`
- `key1` do Zalopay cấp khi đăng ký merchant

> Xem thêm chi tiết tại [Secure Data Transmission](../integration-guides/developer-tools/security-secure-data-transmission.md#hmac)

## Response Fields

| Field | Kiểu | Mô tả |
|---|---|---|
| `return_code` | int | Mã trạng thái xử lý (xem [Bảng mã lỗi](../integration-guides/developer-tools/knowledge-base-status-codes.md)) |
| `return_message` | string | Mô tả trạng thái xử lý |
| `sub_return_code` | int | Mã trạng thái chi tiết |
| `sub_return_message` | string | Mô tả mã trạng thái chi tiết |
| `is_processing` | boolean | Đơn hàng đang được xử lý tại Zalopay (chỉ dùng nội bộ Zalopay) |
| `amount` | int64 | Số tiền thực nhận (chỉ có giá trị khi thanh toán thành công) |
| `discount_amount` | int64 | Số tiền giảm giá (nếu có) |
| `zp_trans_id` | int64 | Mã giao dịch của Zalopay, dùng để đối soát/hoàn tiền |
| `server_time` | int64 | Thời gian xử lý tại server Zalopay, tính bằng Unix timestamp (milliseconds) |

## Ví dụ response

```json
{
  "return_code": 1,
  "return_message": "Giao dịch thành công",
  "sub_return_code": 1,
  "sub_return_message": "Giao dịch thành công",
  "is_processing": false,
  "amount": 50000,
  "discount_amount": 0,
  "zp_trans_id": 220603000000123,
  "server_time": 1654234567000
}
```

## Lưu ý

- `return_code = 1`: giao dịch thành công; `return_code = 2`: giao dịch thất bại; `return_code = 3`: giao dịch đang xử lý.
- Merchant nên gọi QueryOrder định kỳ (ví dụ qua cron job) để xác nhận trạng thái đơn hàng cho đến khi nhận được callback hoặc hết thời gian hết hạn của đơn hàng (mặc định 15 phút).
- HTTP status trả về luôn là `200 OK`; trạng thái thực tế của giao dịch dựa vào `return_code`.
