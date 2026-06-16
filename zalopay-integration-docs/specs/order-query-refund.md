# API Query Refund (Truy vấn trạng thái hoàn tiền)

Nguồn: https://docs.zalopay.vn/docs/specs/order-query-refund

## Tổng quan

API QueryRefund cho phép merchant truy vấn trạng thái xử lý của một giao dịch hoàn tiền đã gửi qua [API Refund](./order-refund.md).

- **Method:** POST
- **Endpoint:** `/v2/query_refund`

## Request Parameters

| Tham số | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|
| `app_id` | int32 | Có | ID do Zalopay cấp cho merchant/ứng dụng |
| `m_refund_id` | string | Có | Mã giao dịch hoàn tiền (`m_refund_id`) do merchant sinh ra khi gọi API Refund |
| `timestamp` | int64 | Có | Thời điểm gửi request, tính bằng Unix timestamp (milliseconds) |
| `mac` | string | Có | Chữ ký xác thực HMAC (xem [Tính toán mac](#tính-toán-mac)) |

## Tính toán mac

```
mac = HMAC_SHA256(key1, app_id|m_refund_id|timestamp)
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

## Ví dụ response

```json
{
  "return_code": 1,
  "return_message": "success",
  "sub_return_code": 1,
  "sub_return_message": "success"
}
```

## Lưu ý

- `return_code = 1`: hoàn tiền thành công; `return_code = 2`: hoàn tiền thất bại; `return_code = 3`: đang xử lý.
- Nếu `return_code = 3` (đang xử lý), merchant nên gọi lại API này theo định kỳ để xác nhận kết quả cuối cùng.
- HTTP status trả về luôn là `200 OK`; trạng thái thực tế dựa vào `return_code`.
