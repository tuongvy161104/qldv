"""
Quick setup test data for commendation system
Run: python manage.py shell < setup_test_data.py
"""

from decimal import Decimal
from datetime import date
from qldv.models import DangVien, DangVienDanhGia
from django.utils import timezone

# Get some existing party members
dang_viens = DangVien.objects.filter(DienDangVien='CHINH_THUC', TrangThaiSinhHoat='Đang sinh hoạt')[:3]

if not dang_viens:
    print("❌ Không có đảng viên chính thức nào. Vui lòng thêm đảng viên trước.")
else:
    print(f"✓ Tìm thấy {len(dang_viens)} đảng viên\n")
    
    # Thêm đánh giá 1 năm (2024)
    print("📝 Thêm đánh giá năm 2024...")
    dv1 = dang_viens[0]
    dg1, created = DangVienDanhGia.objects.get_or_create(
        DangVienID=dv1,
        Nam=2024,
        defaults={'XepLoai': 'HTXSNV', 'GhiChu': 'Hoàn thành xuất sắc'}
    )
    status1 = "✓ Tạo mới" if created else "~ Đã tồn tại"
    print(f"  {status1}: {dv1.HoTen} - {dg1.get_XepLoai_display()} (2024)")
    
    # Thêm đánh giá 5 năm liên tiếp (2020-2024)
    if len(dang_viens) >= 2:
        print("\n📝 Thêm đánh giá 5 năm liên tiếp (2020-2024)...")
        dv2 = dang_viens[1]
        for year in range(2020, 2025):
            dg, created = DangVienDanhGia.objects.get_or_create(
                DangVienID=dv2,
                Nam=year,
                defaults={'XepLoai': 'HTXSNV', 'GhiChu': 'Hoàn thành xuất sắc'}
            )
            status = "✓" if created else "~"
            print(f"  {status} {dv2.HoTen} - {dg.get_XepLoai_display()} ({year})")
    
    # Thêm đánh giá 5 năm khác (2019-2023)
    if len(dang_viens) >= 3:
        print("\n📝 Thêm đánh giá 5 năm khác (2019-2023)...")
        dv3 = dang_viens[2]
        for year in range(2019, 2024):
            dg, created = DangVienDanhGia.objects.get_or_create(
                DangVienID=dv3,
                Nam=year,
                defaults={'XepLoai': 'HTXSNV', 'GhiChu': 'Hoàn thành xuất sắc'}
            )
            status = "✓" if created else "~"
            print(f"  {status} {dv3.HoTen} - {dg.get_XepLoai_display()} ({year})")

print("\n" + "="*60)
print("✅ Setup hoàn tất!")
print("\nBước tiếp theo:")
print("  1. Chạy: python manage.py sync_khenthuong --year 2024")
print("  2. Vào: /de-nghi-khenthuong/")
print("  3. Xem danh sách đề nghị khen thưởng")
print("="*60)
