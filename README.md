# Quản lý Đảng viên

Đây là dự án web quản lý thông tin Đảng viên được xây dựng bằng Django. Ứng dụng hỗ trợ quản lý Đảng bộ, Chi bộ, thông tin Đảng viên, huy hiệu, lịch sử biến động và nhập/xuất dữ liệu từ file CSV/Excel.

## 1. Tính năng chính

- Quản lý Đảng bộ và Chi bộ
- Quản lý thông tin Đảng viên
- Tính toán và theo dõi huy hiệu theo thời gian tham gia Đảng
- Hỗ trợ nhập dữ liệu từ CSV/Excel
- Hệ thống đăng nhập, đăng ký và đổi mật khẩu
- Giao diện quản trị Django tích hợp sẵn

## 2. Công nghệ sử dụng

- Python 3.12
- Django 6.0.4
- PostgreSQL (mặc định trong cấu hình)
- Gunicorn
- WhiteNoise
- openpyxl

## 3. Cấu trúc thư mục

```text
qldv/
├── Dockerfile
├── requirements.txt
└── quanlydangvien/
    ├── manage.py
    ├── quanlydangvien/
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    └── qldv/
        ├── models.py
        ├── views.py
        ├── forms.py
        ├── middleware.py
        ├── backends.py
        ├── templates/
        └── migrations/
```

## 4. Yêu cầu hệ thống

- Python 3.10+ (khuyến nghị 3.12)
- pip
- PostgreSQL (nếu dùng cấu hình mặc định)

## 5. Cài đặt môi trường

1. Di chuyển vào thư mục dự án:

```bash
cd qldv
```

2. Tạo môi trường ảo:

```bash
python -m venv venv
```

3. Kích hoạt môi trường ảo:

- Windows:

```bash
venv\Scripts\activate
```

- Linux/macOS:

```bash
source venv/bin/activate
```

4. Cài đặt dependency:

```bash
pip install -r requirements.txt
```

## 6. Cấu hình biến môi trường

Dự án đọc biến môi trường từ file `.env` nếu có. Một số biến thường dùng:

```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=postgres://postgres:12345@localhost:5432/quanlydangvien
```

Nếu không cấu hình, hệ thống sẽ dùng giá trị mặc định trong file cấu hình.

## 7. Chạy ứng dụng locally

1. Di chuyển vào thư mục chứa `manage.py`:

```bash
cd quanlydangvien
```

2. Chạy migrations:

```bash
python manage.py migrate
```

3. Tạo tài khoản quản trị:

```bash
python manage.py createsuperuser
```

4. Khởi động server:

```bash
python manage.py runserver
```

Sau đó mở trình duyệt tại:

```text
http://127.0.0.1:8000/
```

## 8. Chạy bằng Docker

Dự án đã có Dockerfile sẵn. Bạn có thể build và chạy như sau:

```bash
docker build -t qldv .
docker run -p 8080:8080 qldv
```

## 9. Hướng dẫn nhập dữ liệu

Ứng dụng hỗ trợ nhập dữ liệu cho Chi bộ và Đảng viên từ file CSV hoặc Excel (.xlsx). Sau khi đăng nhập vào hệ thống, bạn có thể truy cập các chức năng nhập dữ liệu từ giao diện web.

### 9.1 File dữ liệu mẫu

Để thử nghiệm nhanh, repo đã cung cấp các file mẫu tại thư mục:

- sample_data/sample_data_chibo.csv
- sample_data/sample_data_dangvien.csv

Bạn có thể dùng các file này làm tài liệu mẫu trước khi nhập dữ liệu thật.

### 9.2 Định dạng file

#### a) Nhập Chi bộ
File nên có các cột cơ bản sau:

- TenChiBo
- DiaBan
- TrangThai
- TenDangBo

#### b) Nhập Đảng viên
File nên có các cột cơ bản sau:

- SoCCCD
- HoTen
- GioiTinh
- NgaySinh
- NgayVaoDang
- DienDangVien
- TrangThaiSinhHoat
- TenChiBo
- TenDangBo

Một số trường có thể bổ sung tùy nhu cầu như: QueQuan, NoiThuongTru, DanToc, SoDienThoai, GhiChu.

### 9.3 Cách nhập trên giao diện

1. Đăng nhập vào hệ thống.
2. Truy cập chức năng nhập dữ liệu tương ứng:
   - Chi bộ
   - Đảng viên
3. Chọn file CSV hoặc Excel (.xlsx) từ máy tính.
4. Nhấn nút import.
5. Kiểm tra kết quả trên danh sách dữ liệu sau khi import thành công.

### 9.4 Lưu ý quan trọng

- File nên được lưu theo định dạng UTF-8 để tránh lỗi ký tự tiếng Việt.
- Giá trị ở cột GioiTinh nên là Nam hoặc Nữ.
- Giá trị ở cột DienDangVien nên là một trong các giá trị: DU_BI, CHO_XET, CHINH_THUC, BI_XOA_TEN.
- Nếu dữ liệu trùng với thông tin đã có trong hệ thống, hệ thống có thể từ chối nhập để tránh lặp dữ liệu.

## 10. Ghi chú

- Đây là dự án học tập/đồ án tốt nghiệp, nên có thể cần điều chỉnh thêm trước khi đưa vào môi trường production.
- Nếu triển khai production, nên thay đổi `SECRET_KEY`, bật `DEBUG=False` và cấu hình database/host phù hợp.

## 11. Liên hệ

Nếu cần hỗ trợ hoặc mở rộng tính năng, có thể tiếp tục phát triển thêm các module như:

- báo cáo thống kê
- xuất báo cáo PDF/Excel
- phân quyền người dùng chi tiết
- tích hợp xác thực LDAP/SSO
