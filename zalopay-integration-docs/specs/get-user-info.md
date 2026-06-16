# API Get User Info (Lấy thông tin người dùng - OAuth)

Nguồn: https://docs.zalopay.vn/docs/specs/get-user-info

## Tổng quan

API cho phép merchant lấy thông tin chi tiết của người dùng đã ủy quyền (OAuth), dựa trên `access_token` lấy từ [API Get Access Token](./get-access-token.md).

- **Method:** GET
- **Endpoint:** `/oauth/user/info`

## Request Parameters

### Header

| Tham số | Bắt buộc | Mô tả |
|---|---|---|
| `x-secret-key` | Có | Secret key do team Zalopay cấp cho merchant |
| `Authorization` | Có | Định dạng `Bearer {access_token}` |

### Query Parameters

| Tham số | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|
| `fields` | string | Không | Danh sách scope field cần lấy, phân tách bằng dấu phẩy. Ví dụ: `fields=user.phone,user.identity.info` |

## Response Fields (200 OK)

| Field | Kiểu | Mô tả |
|---|---|---|
| `context_id` | string | ID context của request |
| `trace_id` | string | ID dùng để trace request |
| `data.avatar` | string | URL ảnh đại diện |
| `data.display_name` | string | Tên hiển thị |
| `data.muid` | string | Định danh người dùng trong hệ thống Zalopay |
| `data.user_email` | string | Email người dùng |
| `data.user_phone` | int | Số điện thoại người dùng |
| `data.user_identity_image.id_number` | string | Số CMND/CCCD |
| `data.user_identity_image.id_type` | string | Loại giấy tờ định danh |
| `data.user_identity_image.expiration_date` | string | Ngày hết hạn giấy tờ |
| `data.user_identity_image.issue_date` | string | Ngày cấp |
| `data.user_identity_image.issue_place` | string | Nơi cấp |
| `data.user_identity_image.identity_image_front` | string | Ảnh mặt trước giấy tờ |
| `data.user_identity_image.identity_image_back` | string | Ảnh mặt sau giấy tờ |
| `data.user_identity_info.full_name` | string | Họ tên đầy đủ |
| `data.user_identity_info.permanent_address` | string | Địa chỉ thường trú |
| `data.user_identity_info.birthday` | int | Ngày sinh |
| `data.user_identity_info.gender` | int | Giới tính |

## Lưu ý

- Tham số `fields` cho phép merchant chỉ lấy các nhóm thông tin cần thiết (ví dụ chỉ `user.phone`), theo đúng scope đã được người dùng cấp quyền khi đăng nhập OAuth.
- Không có công thức tính `mac`/chữ ký cho API này; xác thực qua header `x-secret-key` và `Authorization: Bearer`.
