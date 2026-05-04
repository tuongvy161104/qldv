# Sử dụng Python image chính thức.
FROM python:3.12-slim

# Thiết lập biến môi trường
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PORT 8080

# Thiết lập thư mục làm việc
WORKDIR /app

# Cài đặt các dependencies cần thiết cho hệ thống (nếu dùng psycopg2)
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Cài đặt Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép toàn bộ mã nguồn vào container
COPY . /app/

# Chuyển vào thư mục chứa manage.py
WORKDIR /app/quanlydangvien

# Thu thập static files
RUN python manage.py collectstatic --noinput

# Chạy migrations và khởi động ứng dụng bằng Gunicorn
CMD sh -c "python manage.py migrate && exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 quanlydangvien.wsgi:application"
