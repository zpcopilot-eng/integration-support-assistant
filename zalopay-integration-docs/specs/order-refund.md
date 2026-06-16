# API Refund Order (Hoàn tiền đơn hàng)

Nguồn: https://docs.zalopay.vn/docs/specs/order-refund

## Tổng quan

API Refund dùng để merchant yêu cầu hoàn tiền cho một giao dịch đã thanh toán thành công. Đây là API xử lý bất đồng bộ — sau khi gọi, merchant cần dùng [API QueryRefund](./order-query-refund.md) để kiểm tra kết quả hoàn tiền.

- **Method:** POST
- **Endpoint:** `/v2/refund`

## Request Parameters

| Tham số | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|
| `app_id` | int32 | Có | ID do Zalopay cấp cho merchant/ứng dụng |
| `m_refund_id` | string | Có | Mã giao dịch hoàn tiền do merchant tự sinh, định dạng `yymmdd_appid_xxxxxxxxx` |
| `zp_trans_id` | string | Có | Mã giao dịch gốc cần hoàn tiền (`zp_trans_id` lấy từ callback hoặc API QueryOrder) |
| `amount` | int64 | Có | Số tiền hoàn lại (VND) |
| `refund_fee_amount` | int64 | Không | Phí trừ vào số tiền hoàn lại của người dùng (nếu có) |
| `timestamp` | int64 | Có | Thời điểm gửi request, tính bằng Unix timestamp (milliseconds) |
| `description` | string | Có | Lý do/mô tả hoàn tiền |
| `mac` | string | Có | Chữ ký xác thực HMAC (xem [Tính toán mac](#tính-toán-mac)) |

## Tính toán mac

```
# Không có refund_fee_amount
mac = HMAC_SHA256(key1, app_id|zp_trans_id|amount|description|timestamp)

# Có refund_fee_amount
mac = HMAC_SHA256(key1, app_id|zp_trans_id|amount|refund_fee_amount|description|timestamp)
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
| `refund_id` | int64 | Mã giao dịch hoàn tiền do Zalopay cấp |

## Ví dụ response

```json
{
  "return_code": 1,
  "return_message": "success",
  "sub_return_code": 1,
  "sub_return_message": "success",
  "refund_id": 220603000000456
}
```

## Lưu ý

- Đây là API bất đồng bộ: `return_code = 1` chỉ xác nhận yêu cầu đã được tiếp nhận, chưa chắc hoàn tiền đã hoàn tất.
- Để biết kết quả hoàn tiền cuối cùng, merchant cần gọi [API QueryRefund](./order-query-refund.md) với `m_refund_id` đã dùng ở bước này.
- HTTP status trả về luôn là `200 OK`; trạng thái thực tế dựa vào `return_code`.
