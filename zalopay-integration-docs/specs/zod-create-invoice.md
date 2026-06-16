# API ZOD Create Invoice (Tạo hóa đơn thanh toán khi giao hàng)

Nguồn: https://docs.zalopay.vn/docs/specs/zod-create-invoice

## Tổng quan

API CreateZODInvoice dùng để merchant tạo hóa đơn cho đơn hàng thanh toán khi nhận hàng (Zalopay On Delivery - ZOD). Response trả về `orderUrl` để merchant tạo QR code hiển thị cho shipper/người nhận hàng quét thanh toán. Xem thêm tổng quan tại [ZOD Integration Guide](../integration-guides/payment-acceptance/zod.md).

- **Method:** POST
- **Endpoint:** `/v2/create-invoice`

## Request Parameters

| Tham số | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|
| `appId` | string | Có | AppID do Zalopay cấp |
| `mcRefId` | string | Có | Mã tham chiếu đơn hàng của merchant |
| `hubId` | string | Không | ID của hub (kho/điểm giao hàng) của merchant |
| `driverId` | string | Không | ID của shipper/driver |
| `amount` | int64 | Có | Số tiền đơn hàng (VND) |
| `receiver` | object | Có | Thông tin người nhận |
| `receiver.contact` | string | Không | Tên người nhận |
| `orderInfo` | array | Có | Danh sách thông tin chi tiết đơn hàng |
| `orderInfo[].trackingNumber` | string | Không | Mã vận đơn |
| `orderInfo[].description` | string | Không | Mô tả đơn hàng |
| `orderInfo[].amount` | int64 | Không | Số tiền của từng đơn hàng con |
| `mcExtInfo` | string | Có | Chuỗi JSON chứa `merchandiseSubtotal`, `shippingSubtotal` |
| `mac` | string | Có | Chữ ký xác thực HMAC (xem [Tính toán mac](#tính-toán-mac)) |

## Tính toán mac

```
mac = HMAC_SHA256(key1, appId|mcRefId|amount|mcExtInfo)
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
- `orderUrl` sẽ hết hạn và bị đánh dấu `INVALID` sau 1 tháng kể từ thời điểm tạo.
- Dùng [API Query ZOD Invoice](./query-zod-invoice.md) hoặc [API Query ZOD Order Status](./query-zod-order-status.md) để kiểm tra trạng thái thanh toán.
