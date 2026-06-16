# API Query ZOD Invoice (Truy vấn hóa đơn ZOD)

Nguồn: https://docs.zalopay.vn/docs/specs/query-zod-invoice

## Tổng quan

API QueryZODInvoice cho phép merchant truy vấn lại thông tin hóa đơn (`orderUrl`) đã tạo qua [API ZOD Create Invoice](./zod-create-invoice.md), theo `mcRefId`.

- **Method:** POST
- **Endpoint:** `/v2/query-invoice`

## Request Parameters

| Tham số | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|
| `appId` | string | Có | AppID do Zalopay cấp |
| `mcRefId` | string | Có | Mã tham chiếu đơn hàng của merchant (đã dùng khi tạo hóa đơn) |
| `mac` | string | Có | Chữ ký xác thực HMAC (xem [Tính toán mac](#tính-toán-mac)) |

## Tính toán mac

```
mac = HMAC_SHA256(key1, appId|mcRefId)
```

- Thuật toán mặc định: `HmacSHA256`
- `key1` do Zalopay cấp khi đăng ký merchant

> Xem thêm chi tiết tại [Secure Data Transmission](../integration-guides/developer-tools/security-secure-data-transmission.md#hmac)

## Response Fields

| Field | Kiểu | Mô tả |
|---|---|---|
| `orderUrl` | string | URL dùng để tạo QR code hiển thị trên app shipper |

## Ví dụ response

```json
{
  "orderUrl": "string"
}
```

## Lưu ý

- HTTP status trả về `200 OK` khi thành công.
- Để kiểm tra trạng thái thanh toán (đã thanh toán hay chưa), dùng [API Query ZOD Order Status](./query-zod-order-status.md).
