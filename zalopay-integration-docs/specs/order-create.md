# API Create Order (Tạo đơn hàng)

Nguồn: https://docs.zalopay.vn/docs/specs/order-create

## Tổng quan

API CreateOrder được merchant gọi từ server để khởi tạo thông tin đơn hàng và gửi lên server của Zalopay.

- **Method:** POST
- **Endpoint:** `/v2/create`

## Request Parameters

| Tham số | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|
| `app_id` | int32 | Có | ID do Zalopay cấp cho merchant/ứng dụng |
| `app_user` | string(50) | Có | ID/username của người dùng thực hiện thanh toán; không được để trống |
| `app_trans_id` | string(40) | Có | Mã giao dịch theo định dạng `yymmdd_OrderID` (ví dụ: `250210_OrderID`), tính theo timezone Việt Nam (GMT+7) |
| `app_time` | int64 | Có | Thời điểm tạo đơn hàng, tính bằng Unix timestamp (milliseconds) |
| `expire_duration_seconds` | long | Không | Thời gian hết hạn của đơn hàng, tính bằng giây (giá trị từ 300 đến 2.592.000) |
| `amount` | int64 | Có | Số tiền đơn hàng (VND) |
| `description` | string(256) | Có | Mô tả đơn hàng, hiển thị trên app Zalopay |
| `callback_url` | string | Không | URL của merchant để Zalopay gửi callback kết quả thanh toán (server-to-server) |
| `sub_app_id` | string(50) | Không | ID nhóm/dịch vụ con trong ứng dụng của merchant |
| `item` | string(2048) | Có | Chuỗi JSON array chứa thông tin sản phẩm do merchant định nghĩa; nếu không có dữ liệu, truyền `"[]"` |
| `embed_data` | string | Có | Chuỗi JSON object chứa thông tin đặc biệt của đơn hàng; nếu không có dữ liệu, truyền `"{}"` |
| `bank_code` | string | Không | Mã ngân hàng/phương thức thanh toán mong muốn |
| `mac` | string | Có | Chữ ký xác thực HMAC (xem [Tính toán mac](#tính-toán-mac)) |

### Một số field thường dùng trong `embed_data`

- `preferred_payment_method`: array chỉ định phương thức thanh toán ưu tiên (ví dụ: `["vietqr"]`)
- `redirecturl`: URL để redirect người dùng sau khi thanh toán
- `columninfo`: JSON object chứa thông tin hiển thị trên Merchant Portal
- `zlppaymentid`: ID thanh toán dùng cho multi-account payment

## Tính toán mac

```
mac = HMAC_SHA256(key1, app_id|app_trans_id|app_user|amount|app_time|embed_data|item)
```

- Thuật toán mặc định: `HmacSHA256`
- `key1` do Zalopay cấp khi đăng ký merchant

> Xem thêm chi tiết tại [Secure Data Transmission](../integration-guides/developer-tools/security-secure-data-transmission.md#hmac)

## Response Fields

| Field | Kiểu | Mô tả |
|---|---|---|
| `return_code` | int | Mã trạng thái xử lý (xem [Bảng mã lỗi](../integration-guides/developer-tools/knowledge-base-status-codes.md)) |
| `return_message` | string | Mô tả trạng thái xử lý |
| `sub_return_code` | int | Mã trạng thái chi tiết riêng của API CreateOrder |
| `sub_return_message` | string | Mô tả mã trạng thái chi tiết |
| `zp_trans_token` | string | Token giao dịch, dùng cho tích hợp app-to-app hoặc thanh toán bằng token |
| `order_url` | string | URL để chuyển người dùng đến Zalopay Gateway (dùng để hiển thị QR hoặc redirect) |
| `order_token` | string | Token của đơn hàng |
| `qr_code` | string | Chuỗi QR code đa năng (tương thích NAPAS) |

## Ví dụ response

```json
{
  "return_code": 1,
  "return_message": "Giao dịch thành công",
  "sub_return_code": 1,
  "sub_return_message": "Giao dịch thành công",
  "zp_trans_token": "...",
  "order_url": "https://qcgateway.zalopay.vn/openinapp?order=...",
  "order_token": "...",
  "qr_code": "..."
}
```

## Lưu ý

- HTTP status trả về luôn là `200 OK`; trạng thái thực tế của giao dịch dựa vào `return_code`.
- Sau khi tạo đơn hàng, nên gọi API QueryOrder để kiểm tra trạng thái thanh toán thay vì chỉ phụ thuộc vào callback.
