import calendar
import datetime
import re
import unicodedata
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models


def _add_months(base_date, months):
    month_index = base_date.month - 1 + months
    year = base_date.year + month_index // 12
    month = month_index % 12 + 1
    day = min(base_date.day, calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)


def _add_working_days(base_date, working_days):
    current_date = base_date
    added = 0
    while added < working_days:
        current_date += datetime.timedelta(days=1)
        if current_date.weekday() < 5:
            added += 1
    return current_date


class DangBo(models.Model):
    """Đảng Bộ - Party Section"""
    DangBoID = models.AutoField(primary_key=True)
    TenDangBo = models.CharField(max_length=255)
    CapDangBo = models.CharField(max_length=100)
    TrangThai = models.CharField(max_length=50, default="Đang hoạt động")

    class Meta:
        db_table = 'DangBo'

    def __str__(self):
        return self.TenDangBo


class ChiBo(models.Model):
    """Chi Bộ - Party Cell/Unit"""
    ChiBoID = models.AutoField(primary_key=True)
    TenChiBo = models.CharField(max_length=255)
    DiaBan = models.CharField(max_length=255)
    TrangThai = models.CharField(max_length=50)
    DangBoID = models.ForeignKey(DangBo, on_delete=models.PROTECT, db_column='DangBoID')

    class Meta:
        db_table = 'ChiBo'

    @staticmethod
    def normalized_name_key(value):
        if value is None:
            return ""

        text = unicodedata.normalize("NFKC", str(value)).strip().lower()
        text = text.replace("_", " ")
        text = re.sub(r"[^\w\s]", " ", text, flags=re.UNICODE)
        text = re.sub(r"\s+", " ", text).strip()

        deaccented = unicodedata.normalize("NFD", text)
        deaccented = "".join(ch for ch in deaccented if unicodedata.category(ch) != "Mn")
        parts = deaccented.split()
        if len(parts) >= 2 and parts[0] == "chi" and parts[1] == "bo":
            parts = parts[2:]

        return " ".join(parts)

    def __str__(self):
        return self.TenChiBo


class DangVien(models.Model):
    """Đảng Viên - Party Member"""
    DIEN_DANG_VIEN_CHOICES = [
        ("DU_BI", "Dự bị"),
        ("CHO_XET", "Chờ xét"),
        ("CHINH_THUC", "Chính thức"),
        ("BI_XOA_TEN", "Bị xóa tên"),
    ]

    TRANG_THAI_SINH_HOAT_CHOICES = [
        ("Đang sinh hoạt", "Đang sinh hoạt"),
        ("Chuyển sinh hoạt", "Chuyển sinh hoạt"),
        ("Nghỉ", "Nghỉ"),
    ]

    DangVienID = models.AutoField(primary_key=True)
    SoCCCD = models.CharField(max_length=12, unique=True, null=True, blank=True)
    MaDangVien = models.CharField(max_length=50, unique=True, blank=True)
    HoTen = models.CharField(max_length=255)
    BiDanh = models.CharField(max_length=255, null=True, blank=True)
    GioiTinh = models.CharField(
        max_length=10,
        choices=[('Nam', 'Nam'), ('Nữ', 'Nữ')]
    )
    NgaySinh = models.DateField()
    QueQuan = models.CharField(max_length=255, null=True, blank=True)
    NoiThuongTru = models.CharField(max_length=255, null=True, blank=True)
    NoiTamTru = models.CharField(max_length=255, null=True, blank=True)
    DanToc = models.CharField(max_length=100, null=True, blank=True)
    NgheNghiep = models.CharField(max_length=255, null=True, blank=True)
    GDPT = models.CharField(max_length=100, null=True, blank=True)
    GDNN = models.CharField(max_length=255, null=True, blank=True)
    GDDH = models.CharField(max_length=255, null=True, blank=True)
    GDSĐH = models.CharField(max_length=255, null=True, blank=True)
    HocHam = models.CharField(max_length=100, null=True, blank=True)
    LyLuanChinhTri = models.CharField(max_length=255, null=True, blank=True)
    NgoaiNgu = models.CharField(max_length=255, null=True, blank=True)
    TinHoc = models.CharField(max_length=255, null=True, blank=True)
    TiengDTTS = models.CharField(max_length=255, null=True, blank=True)
    NgayVaoDang = models.DateField(null=True, blank=True)
    NgayChinhThuc = models.DateField(null=True, blank=True)
    ChiBoID = models.ForeignKey(ChiBo, on_delete=models.PROTECT, db_column='ChiBoID')
    DangBoID = models.ForeignKey(DangBo, on_delete=models.PROTECT, db_column='DangBoID')
    TrangThaiSinhHoat = models.CharField(
        max_length=50,
        choices=TRANG_THAI_SINH_HOAT_CHOICES,
        default="Đang sinh hoạt",
    )
    DienDangVien = models.CharField(max_length=20, choices=DIEN_DANG_VIEN_CHOICES, default="DU_BI")
    SoDienThoai = models.CharField(max_length=10, null=True, blank=True)
    GhiChu = models.TextField(blank=True, null=True)
    HuyHieuCaoNhat = models.CharField(max_length=100, null=True, blank=True)
    SoHuyHieu = models.IntegerField(default=0)

    def update_highest_badge(self):
        """
        Tái tính HuyHieuCaoNhat và SoHuyHieu dựa vào NgayVaoDang.
        Được gọi tự động khi HuyHieuDang được lưu hoặc xóa.
        """
        self.auto_compute_badge_from_ngay_vao_dang()
        DangVien.objects.filter(pk=self.pk).update(
            HuyHieuCaoNhat=self.HuyHieuCaoNhat,
            SoHuyHieu=self.SoHuyHieu,
        )


    class Meta:
        db_table = 'DangVien'

    MA_DANG_VIEN_PREFIX = "48"

    @staticmethod
    def _normalize_membership_value(value):
        if not value:
            return "DU_BI"

        text = str(value).strip()
        canonical = {
            "DU_BI": "DU_BI",
            "DỰ BỊ": "DU_BI",
            "DU BI": "DU_BI",
            "CHO_XET": "CHO_XET",
            "CHỜ XÉT": "CHO_XET",
            "CHO XET": "CHO_XET",
            "CHINH_THUC": "CHINH_THUC",
            "CHÍNH THỨC": "CHINH_THUC",
            "CHINH THUC": "CHINH_THUC",
            "BI_XOA_TEN": "BI_XOA_TEN",
            "BỊ XOÁ TÊN": "BI_XOA_TEN",
            "BỊ XÓA TÊN": "BI_XOA_TEN",
            "BI XOA TEN": "BI_XOA_TEN",
        }
        return canonical.get(text.upper(), "DU_BI")

    def get_probation_end_date(self):
        if not self.NgayVaoDang:
            return None
        return _add_months(self.NgayVaoDang, 12)

    def get_review_deadline(self):
        probation_end = self.get_probation_end_date()
        if not probation_end:
            return None
        return _add_working_days(probation_end, 30)

    def is_overdue_membership_review(self, reference_date=None):
        if self._normalize_membership_value(self.DienDangVien) != "CHO_XET":
            return False
        review_deadline = self.get_review_deadline()
        if not review_deadline:
            return False
        today = reference_date or datetime.date.today()
        return today > review_deadline

    def apply_membership_rules(self, reference_date=None):
        today = reference_date or datetime.date.today()
        current_status = self._normalize_membership_value(self.DienDangVien)

        if current_status == "BI_XOA_TEN":
            self.DienDangVien = "BI_XOA_TEN"
            self.NgayChinhThuc = None
            self.NgayVaoDang = None
            return

        if not self.NgayVaoDang:
            return

        probation_end = _add_months(self.NgayVaoDang, 12)

        if current_status == "CHINH_THUC":
            self.DienDangVien = "CHINH_THUC"
            self.NgayChinhThuc = probation_end
            return

        if current_status == "DU_BI":
            if today >= probation_end:
                self.DienDangVien = "CHO_XET"
                self.NgayChinhThuc = None
            else:
                self.DienDangVien = "DU_BI"
                self.NgayChinhThuc = None
            return

        if current_status == "CHO_XET":
            self.NgayChinhThuc = None
            self.DienDangVien = "CHO_XET"
            return

        self.DienDangVien = "BI_XOA_TEN"
        self.NgayChinhThuc = None

    @classmethod
    def generate_ma_dang_vien(cls):
        prefix = f"{cls.MA_DANG_VIEN_PREFIX}."
        max_sequence = 0

        existing_codes = cls.objects.filter(
            MaDangVien__startswith=prefix
        ).values_list("MaDangVien", flat=True)

        for code in existing_codes:
            if not code:
                continue
            parts = str(code).split(".", 1)
            if len(parts) != 2:
                continue
            sequence = parts[1]
            if len(sequence) == 6 and sequence.isdigit():
                max_sequence = max(max_sequence, int(sequence))

        next_sequence = max_sequence + 1
        if next_sequence > 999999:
            raise ValueError("Đã vượt quá giới hạn 999999 mã Đảng viên.")

        return f"{prefix}{next_sequence:06d}"

    BADGE_MILESTONES = [30, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90]

    def auto_compute_badge_from_ngay_vao_dang(self, review_date=None):
        """
        Tự động tính HuyHieuCaoNhat và SoHuyHieu dựa vào NgayVaoDang.

        Logic theo sơ đồ:
        - Với mỗi mốc huy hiệu y (30, 40, 45, ..., 90):
          + Tuổi Đảng = Năm xét - Năm vào Đảng
          + Nếu Tuổi Đảng >= y VÀ NgayVaoDang <= ngày xét → đủ điều kiện nhận mốc y
        - HuyHieuCaoNhat = mốc cao nhất đủ điều kiện
        - SoHuyHieu = số mốc đã đủ điều kiện
        """
        if not self.NgayVaoDang:
            return

        today = review_date or datetime.date.today()
        join_year = self.NgayVaoDang.year
        review_year = today.year

        # Tuổi Đảng theo năm (không dùng ngày chính xác, đúng với sơ đồ)
        tuoi_dang = review_year - join_year

        earned_milestones = []
        for milestone in self.BADGE_MILESTONES:
            # Điều kiện: Tuổi Đảng >= milestone VÀ NgayVaoDang <= ngày xét
            if tuoi_dang >= milestone and self.NgayVaoDang <= today:
                earned_milestones.append(milestone)

        if earned_milestones:
            highest = max(earned_milestones)
            self.HuyHieuCaoNhat = f"{highest} năm"
            self.SoHuyHieu = len(earned_milestones)
        else:
            self.HuyHieuCaoNhat = None
            self.SoHuyHieu = 0

    def save(self, *args, **kwargs):
        if not self.MaDangVien:
            self.MaDangVien = self.generate_ma_dang_vien()
        self.apply_membership_rules()
        # Nếu người dùng không tự chọn HuyHieuCaoNhat, tự tính từ NgayVaoDang
        if not self.HuyHieuCaoNhat:
            self.auto_compute_badge_from_ngay_vao_dang()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.HoTen


class HuyHieuDang(models.Model):
    """Huy Hiệu Đảng - Party Honors/Sanctions"""
    HuyHieuID = models.AutoField(primary_key=True)
    DangVienID = models.ForeignKey(DangVien, on_delete=models.CASCADE, db_column='DangVienID')
    LoaiHuyHieu = models.CharField(max_length=255)
    NgayDuDieuKien = models.DateField()
    DotTraoTang = models.CharField(max_length=50)
    TrangThai = models.CharField(max_length=50)
    SoQuyetDinh = models.CharField(max_length=50)
    NgayTrao = models.DateField()
    GhiChu = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'HuyHieuDang'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.DangVienID.update_highest_badge()

    def delete(self, *args, **kwargs):
        dv = self.DangVienID
        super().delete(*args, **kwargs)
        dv.update_highest_badge()

    def __str__(self):
        return f"{self.LoaiHuyHieu} - {self.DangVienID.HoTen}"



