# API Query ZOD Order Status (Truy vấn trạng thái đơn hàng ZOD)

Nguồn: https://docs.zalopay.vn/docs/specs/query-zod-order-status

## Tổng quan

API QueryZODOrder cho phép merchant truy vấn trạng thái thanh toán của một đơn hàng ZOD đã tạo qua [API ZOD Create Invoice](./zod-create-invoice.md). Merchant nên chủ động gọi API này thay vì chỉ phụ thuộc vào callback (xem [ZOD Integration Guide](../integration-guides/payment-acceptance/zod.md#query-functionality)).

- **Method:** POST
- **Endpoint:** `/v2/query-order-status`

## Request Parameters

| Tham số | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|
| `appId` | string | Có | AppID do Zalopay cấp |
| `mcRefId` | string | Có | Mã tham chiếu đơn hàng của merchant |
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
| `status` | int64 | Trạng thái đơn hàng: `1`=SUCCESS, `2`=FAILURE, `3`=UNPAID |
| `amount` | string | Số tiền của đơn hàng |
| `zpTransId` | string | Mã giao dịch của Zalopay |

## Ví dụ response

```json
{
  "status": 1,
  "amount": "50000",
  "zpTransId": "220603000000123"
}
```

## Lưu ý

- HTTP status trả về `200 OK` khi thành công.
- `status = 3` (UNPAID): merchant nên gọi lại API này định kỳ cho đến khi `orderUrl` hết hạn (1 tháng) hoặc nhận được callback.
