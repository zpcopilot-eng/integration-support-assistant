# API Get Access Token (Lấy access token người dùng - OAuth)

Nguồn: https://docs.zalopay.vn/docs/specs/get-access-token

## Tổng quan

API này dùng trong luồng OAuth của Zalopay, để đổi `authorization code` (lấy được từ bước `zlpSdk.User.getOauthV1Code` trên SDK) hoặc `refresh_token` thành `access_token`, phục vụ cho việc gọi các API ủy quyền của người dùng như [Get User Info](./get-user-info.md) và [Get Public User Info](./get-public-user-info.md).

- **Method:** POST
- **Endpoint:** `/oauth/token`

## Request Parameters

### Header

| Tham số | Bắt buộc | Mô tả |
|---|---|---|
| `x-secret-key` | Có | Secret key do team Zalopay cấp cho merchant |

### Body

| Tham số | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|
| `code` | string | Tùy chọn* | Authorization code lấy từ `zlpSdk.User.getOauthV1Code` |
| `code_verifier` | string | Tùy chọn* | Code verifier được sinh ra ở cùng bước với `code` |
| `refresh_token` | string | Tùy chọn* | Dùng để lấy `access_token` mới khi token cũ hết hạn |

\* Cần cung cấp **một trong hai**: (`code` + `code_verifier`) hoặc `refresh_token`.

## Response Fields (Thành công - 200)

| Field | Kiểu | Mô tả |
|---|---|---|
| `data.access_token` | string | Token dùng để gọi các API ủy quyền của Zalopay |
| `data.refresh_token` | string | Refresh token, có hiệu lực 30 ngày |
| `data.expires_in` | int | Thời gian hết hạn của `access_token` (milliseconds) |
| `data.refresh_expires_in` | int | Thời gian hết hạn của `refresh_token` (milliseconds) |
| `data.permissions` | string[] | Danh sách scope/quyền được người dùng cấp |

## Response lỗi

| Field | Kiểu | Mô tả |
|---|---|---|
| `error.error` | string | Mã định danh lỗi |
| `error.code` | int | Mã lỗi |
| `error.details` | object | Thông tin chi tiết lỗi: `reason`, `domain`, message hiển thị |

## Lưu ý

- Khi `access_token` hết hạn, dùng `refresh_token` để lấy `access_token` mới mà không cần người dùng đăng nhập lại.
- Không có công thức tính `mac`/chữ ký cho API này; xác thực thực hiện qua header `x-secret-key`.
