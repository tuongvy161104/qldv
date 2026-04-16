# Hướng dẫn kiểm tra tính năng Đăng nhập

## Bước 1: Khởi động Development Server

```bash
cd "/Users/tuongvy/Documents/Tuong Vy/thư mục không có tiêu đề/myproject/quanlydangvien"
source ../venv/bin/activate
python manage.py runserver
```

Server sẽ chạy tại `http://127.0.0.1:8000/`

## Bước 2: Kiểm tra các URL chính

### A. Trang chủ (Chưa đăng nhập)
- URL: `http://127.0.0.1:8000/`
- Kỳ vọng: Hiển thị lời chào mừng với nút "Đăng nhập" và "Đăng ký tài khoản"

### B. Trang Đăng ký
- URL: `http://127.0.0.1:8000/signup/`
- Bước:
  1. Điền thông tin:
     - Tên: `John`
     - Họ: `Doe`
     - Email: `john@example.com`
     - Mật khẩu: `Test1234`
     - Xác nhận mật khẩu: `Test1234`
  2. Nhấn "Đăng ký"
  3. Kỳ vọng: Được đăng nhập tự động và chuyển về trang chủ

### C. Trang chủ (Đã đăng nhập)
- Sau đăng ký thành công
- Kỳ vọng: 
  - Hiển thị các thống kê (Chi bộ, Đảng viên, Huy hiệu)
  - Sidebar hiển thị "Chào mừng John" và nút "Đăng xuất"

### D. Trang Đăng nhập
- URL: `http://127.0.0.1:8000/login/`
- Sau khi đăng xuất, hãy kiểm tra đăng nhập lại:
  1. Email: `john@example.com`
  2. Mật khẩu: `Test1234`
  3. Có thể đánh dấu "Ghi nhớ đăng nhập"
  4. Nhấn "Đăng nhập"
  5. Kỳ vọng: Chuyển về trang chủ

### E. Đăng xuất
- Nhấn nút "Đăng xuất" ở sidebar
- Kỳ vọng: Chuyển về trang chủ và hiển thị thông báo "Bạn đã đăng xuất thành công"

## Bước 3: Kiểm tra các trang được bảo vệ

Khi đã đăng nhập, hãy kiểm tra các trang:

1. **Chi bộ**: `http://127.0.0.1:8000/chibo/`
2. **Đảng viên**: `http://127.0.0.1:8000/dangvien/`
3. **Huy hiệu**: `http://127.0.0.1:8000/huyhieu/`

Nếu chưa đăng nhập, bạn sẽ bị chuyển hướng đến trang đăng nhập.

## Bước 4: Kiểm tra Validation

### A. Kiểm tra Email hợp lệ
- Trên trang `/signup/`:
  1. Nhập email không đúng định dạng (ví dụ: `invalidemail`)
  2. Nhấn "Đăng ký"
  3. Kỳ vọng: Hiển thị lỗi "Nhập một địa chỉ email hợp lệ"

### B. Kiểm tra Mật khẩu quá ngắn
- Trên trang `/signup/`:
  1. Mật khẩu: `test123` (chỉ 7 ký tự)
  2. Nhấn "Đăng ký"
  3. Kỳ vọng: Hiển thị lỗi "Mật khẩu phải có ít nhất 8 ký tự"

### C. Kiểm tra Mật khẩu không khớp
- Trên trang `/signup/`:
  1. Mật khẩu: `Test1234`
  2. Xác nhận mật khẩu: `Test5678`
  3. Nhấn "Đăng ký"
  4. Kỳ vọng: Hiển thị lỗi "Mật khẩu không khớp"

### D. Kiểm tra Email đã được sử dụng
- Trên trang `/signup/`:
  1. Sử dụng email `john@example.com` lần nữa
  2. Nhấn "Đăng ký"
  3. Kỳ vọng: Hiển thị lỗi "Email này đã được sử dụng"

### E. Kiểm tra Đăng nhập sai
- Trên trang `/login/`:
  1. Email: `john@example.com`
  2. Mật khẩu: `WrongPassword`
  3. Nhấn "Đăng nhập"
  4. Kỳ vọng: Hiển thị lỗi "Email hoặc mật khẩu không chính xác"

## Bước 5: Kiểm tra Remember Me

1. Trên trang `/login/`:
   - Email: `john@example.com`
   - Mật khẩu: `Test1234`
   - Đánh dấu "Ghi nhớ đăng nhập"
   - Nhấn "Đăng nhập"
2. Đóng trình duyệt hoàn toàn (tất cả tab)
3. Mở trình duyệt lại và truy cập `http://127.0.0.1:8000/`
4. Kỳ vọng: Bạn vẫn đang đăng nhập (session vẫn tồn tại)

## Bước 6: Kiểm tra Admin

1. Tạo superuser:
   ```bash
   python manage.py createsuperuser
   ```
   - Username: `admin`
   - Email: `admin@example.com`
   - Password: `Admin1234`

2. Truy cập `/admin/`
   - Username: `admin`
   - Password: `Admin1234`

3. Kiểm tra Users trong Admin panel
   - Bạn sẽ thấy `john@example.com` trong danh sách Users

## Thông tin quan trọng

- Tất cả các thông báo (success, error, warning) sẽ tự động biến mất sau 7 giây
- Mật khẩu được lưu trữ sicher (hash) trong cơ sở dữ liệu
- Session được lưu trữ mặc định trong database (hoặc cache tùy cấu hình)

## Các file có liên quan

- `qldv/backends.py` - Email authentication backend
- `qldv/forms.py` - LoginForm, SignUpForm
- `qldv/views.py` - View functions cho login/logout/signup
- `qldv/templates/qldv/login.html` - Template đăng nhập
- `qldv/templates/qldv/signup.html` - Template đăng ký
- `quanlydangvien/urls.py` - URL patterns
- `quanlydangvien/settings.py` - Configuration

---

**Ghi chú**: Nếu gặp bất kỳ lỗi nào, vui lòng kiểm tra console của Django server để xem thông báo lỗi chi tiết.
