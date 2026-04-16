# Hướng dẫn sử dụng tính năng Đăng nhập - Quản lý Đảng viên

## Tính năng mới

Hệ thống quản lý Đảng viên giờ đây đã có tính năng xác thực người dùng và đăng nhập bằng email. Dưới đây là hướng dẫn chi tiết:

## URL cho Đăng nhập / Đăng ký

- **Đăng nhập**: `/login/`
- **Đăng ký tài khoản mới**: `/signup/`
- **Đăng xuất**: `/logout/` (tự động chuyển hướng về trang chủ)

## Hướng dẫn sử dụng

### 1. Đăng ký tài khoản mới

1. Truy cập trang `/signup/`
2. Điền thông tin:
   - **Tên**: Tên của bạn
   - **Họ**: Họ của bạn
   - **Email**: Địa chỉ email (sẽ được sử dụng để đăng nhập)
   - **Mật khẩu**: Tối thiểu 8 ký tự
   - **Xác nhận mật khẩu**: Nhập lại mật khẩu
3. Nhấn **Đăng ký**
4. Bạn sẽ được đăng nhập tự động và chuyển về trang chủ

### 2. Đăng nhập

1. Truy cập trang `/login/`
2. Điền: 
   - **Email**: Email của bạn
   - **Mật khẩu**: Mật khẩu của bạn
3. Tùy chọn: Đánh dấu **Ghi nhớ đăng nhập** để duy trì đăng nhập trong 30 ngày
4. Nhấn **Đăng nhập**

### 3. Đăng xuất

1. Nhấn nút **Đăng xuất** ở thanh bên (sidebar)
2. Bạn sẽ được quay về trang chủ

## Các tính năng bảo mật

### 1. Remember Me (Ghi nhớ đăng nhập)

- Khi bạn đánh dấu "Ghi nhớ đăng nhập", session sẽ tồn tại trong 30 ngày
- Nếu không đánh dấu, session sẽ kết thúc khi bạn đóng trình duyệt

### 2. Xác thực bằng Email

- Hệ thống sử dụng email làm username duy nhất
- Mỗi email chỉ có thể đăng ký một tài khoản

### 3. Yêu cầu đăng nhập

- Các trang quản lý (Chi bộ, Đảng viên, Huy hiệu) yêu cầu bạn phải đã đăng nhập
- Nếu bạn chưa đăng nhập, bạn sẽ được chuyển hướng đến trang đăng nhập

## Cấu hình (cho Quản trị viên)

### 1. Custom Authentication Backend

File `/qldv/backends.py` chứa lớp `EmailBackend` cho phép đăng nhập bằng email thay vì username. Backend này được kích hoạt trong `settings.py`:

```python
AUTHENTICATION_BACKENDS = [
    'qldv.backends.EmailBackend',
]
```

### 2. Login URL

Mặc định, chương trình yêu cầu đăng nhập sẽ chuyển hướng tới `login_url='login'` được định nghĩa trong decorator `@login_required`.

### 3. Thay đổi Session Timeout

Để thay đổi thời gian hết hạn mặc định của session, chỉnh sửa trong `views.py`, hàm `login_view()`:

```python
# 30 ngày (nếu có "remember me")
request.session.set_expiry(30 * 24 * 60 * 60)

# Hoặc timeout khi đóng trình duyệt
request.session.set_expiry(0)
```

## Tạo tài khoản admin

Để tạo tài khoản admin qua dòng lệnh:

```bash
python manage.py createsuperuser
```

Sau đó truy cập `/admin/` để quản lý người dùng.

## Xử lý sự cố

### Lỗi: "Email này đã được sử dụng"

- Điều này có nghĩa là email đã được đăng ký trong hệ thống
- Hãy sử dụng email khác hoặc thử đăng nhập nếu đó là tài khoản của bạn

### Lỗi: "Email hoặc mật khẩu không chính xác"

- Kiểm tra lại email và mật khẩu
- Hãy chắc chắn rằng bạn đã đánh vần chính xác

### Quên mật khẩu

- Hiện tại, hệ thống chưa có tính năng "Quên mật khẩu"
- Vui lòng liên hệ quản trị viên để reset mật khẩu

## Danh sách các Files đã thay đổi

1. **`qldv/backends.py`** (mới)
   - Chứa `EmailBackend` class cho xác thực bằng email

2. **`qldv/forms.py`** (được cập nhật)
   - Thêm `LoginForm` và `SignUpForm`

3. **`qldv/views.py`** (được cập nhật)
   - Thêm `login_view()`, `signup_view()`, `logout_view()`
   - Thêm `@login_required` decorator cho các view chính

4. **`qldv/templates/qldv/login.html`** (mới)
   - Template để đăng nhập

5. **`qldv/templates/qldv/signup.html`** (mới)
   - Template để đăng ký tài khoản

6. **`qldv/templates/qldv/base.html`** (được cập nhật)
   - Thêm hiển thị thông tin user ở sidebar
   - Thêm nút "Đăng xuất" cho user đã đăng nhập
   - Thêm chào mừng cho user chưa đăng nhập trên trang chủ

7. **`qldv/templates/qldv/home.html`** (được cập nhật)
   - Thêm hero section cho user chưa đăng nhập

8. **`quanlydangvien/urls.py`** (được cập nhật)
   - Thêm các route: `/login/`, `/signup/`, `/logout/`

9. **`quanlydangvien/settings.py`** (được cập nhật)
   - Thêm `AUTHENTICATION_BACKENDS` để sử dụng `EmailBackend`

## Chi tiết kỹ thuật

### Email Backend

Custom email backend cho phép xác thực bằng email bằng cách:
- Tìm user với email khớp
- Kiểm tra mật khẩu
- Trả về user nếu thành công, trả về None nếu thất bại

### Form Validation

- **LoginForm**: Xác thực email và mật khẩu có hợp lệ không
- **SignUpForm**: 
  - Kiểm tra password dài tối thiểu 8 ký tự
  - Kiểm tra hai password khớp nhau
  - Kiểm tra email chưa được sử dụng

### Security

- Sử dụng `csrf_token` trong tất cả các form
- Session được quản lý tự động bởi Django
- Mật khẩu được hash bằng `PBKDF2WithSHA256` (mặc định Django)

## Tương lai

Có thể thêm các tính năng sau:

1. Quên mật khẩu / Reset mật khẩu (qua email)
2. Xác thực hai bước (2FA)
3. OAuth (login qua Google, Facebook, etc.)
4. Email verification
5. User profile page

---

**Phiên bản**: 1.0  
**Ngày cập nhật**: Tháng 4, 2026
