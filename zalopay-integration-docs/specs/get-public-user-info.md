# API Get Public User Info (Lấy thông tin công khai người dùng - OAuth)

Nguồn: https://docs.zalopay.vn/docs/specs/get-public-user-info

## Tổng quan

API trả về thông tin công khai cơ bản (tên hiển thị, avatar) của người dùng đã ủy quyền (OAuth), dựa trên `access_token` lấy từ [API Get Access Token](./get-access-token.md). Đây là phiên bản rút gọn của [API Get User Info](./get-user-info.md), thường dùng khi merchant chỉ cần hiển thị thông tin cơ bản.

- **Method:** GET
- **Endpoint:** `/oauth/user/public-info`

## Request Parameters

### Header

| Tham số | Bắt buộc | Mô tả |
|---|---|---|
| `x-secret-key` | Có | Secret key do team Zalopay cấp cho merchant |
| `Authorization` | Có | Định dạng `Bearer {access_token}` |

### Query Parameters

| Tham số | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|
| `fields` | string | Không | Danh sách scope field cần lấy, phân tách bằng dấu phẩy. Ví dụ: `fields=user.avatar,user.name` |

## Response Fields (200 OK)

| Field | Kiểu | Mô tả |
|---|---|---|
| `context_id` | string | ID context của request |
| `trace_id` | string | ID dùng để trace request |
| `data.avatar` | string | URL ảnh đại diện |
| `data.display_name` | string | Tên hiển thị |
| `data.muid` | string | Định danh người dùng trong hệ thống Zalopay |

## Ví dụ response

```json
{
  "context_id": "string",
  "trace_id": "string",
  "data": {
    "avatar": "string",
    "display_name": "string",
    "muid": "string"
  }
}
```

## Lưu ý

- Không có công thức tính `mac`/chữ ký cho API này; xác thực qua header `x-secret-key` và `Authorization: Bearer`.
