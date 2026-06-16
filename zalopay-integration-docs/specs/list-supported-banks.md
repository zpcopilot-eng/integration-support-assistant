# API List Supported Banks (Danh sách ngân hàng hỗ trợ)

Nguồn: https://docs.zalopay.vn/docs/specs/list-supported-banks

## Tổng quan

API List Supported Banks trả về danh sách các ngân hàng/phương thức thanh toán mà merchant có thể sử dụng, theo từng nhóm phương thức thanh toán (`pcmid`). Thường dùng để hiển thị tùy chọn ngân hàng khi merchant tự xây dựng giao diện thanh toán (tham số `bank_code` trong [API CreateOrder](./order-create.md)).

- **Method:** POST
- **Content-Type:** `application/x-www-form-urlencoded`
- **Endpoint:** `/v2/getbanklist`

## Request Parameters

| Tham số | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|
| `appid` | string | Có | ID do Zalopay cấp cho merchant/ứng dụng |
| `reqtime` | string | Có | Thời điểm gửi request, tính bằng Unix timestamp (milliseconds) |
| `mac` | string | Có | Chữ ký xác thực HMAC (xem [Tính toán mac](#tính-toán-mac)) |

## Tính toán mac

```
mac = HMAC_SHA256(key1, appid|reqtime)
```

- Thuật toán mặc định: `HmacSHA256`
- `key1` do Zalopay cấp khi đăng ký merchant

## Response Fields

| Field | Kiểu | Mô tả |
|---|---|---|
| `returncode` | int | `1`=SUCCESS, `2`=FAIL |
| `returnmessage` | string | Mô tả trạng thái xử lý |
| `banks` | object | Map từ `pcmid` (nhóm phương thức thanh toán) sang danh sách ngân hàng tương ứng |

### Cấu trúc một bank object

| Field | Mô tả |
|---|---|
| `bankcode` | Mã ngân hàng |
| `name` | Tên ngân hàng |
| `displayorder` | Thứ tự hiển thị |
| `pcmid` | Nhóm phương thức thanh toán |
| `minamount` | Số tiền tối thiểu hỗ trợ |
| `maxamount` | Số tiền tối đa hỗ trợ |

## Nhóm phương thức thanh toán (`pcmid`)

| `pcmid` | Phương thức |
|---|---|
| `36` | Visa/Master/JCB (thẻ tín dụng/ghi nợ quốc tế) |
| `37` | Tài khoản ngân hàng (Internet Banking) |
| `38` | Ví Zalopay |
| `39` | Thẻ ATM nội địa |
| `41` | Visa/Master Debit |

## Lưu ý

- Danh sách ngân hàng trả về thường được merchant dùng để map sang giá trị `bank_code` truyền vào [API CreateOrder](./order-create.md).
