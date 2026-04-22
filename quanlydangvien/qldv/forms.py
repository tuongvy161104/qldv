from django import forms

from .models import ChiBo, DangVien, HuyHieuDang
from .services.huyhieu_service import parse_badge_year, validate_badge_decision_number

# Danh sách 54 dân tộc của Việt Nam
ETHNIC_GROUPS = [
    ("Kinh", "Kinh"),
    ("Tày", "Tày"),
    ("Thái", "Thái"),
    ("Mường", "Mường"),
    ("Khmer", "Khmer"),
    ("Hoa", "Hoa"),
    ("Yên", "Yên"),
    ("Tơ Đô", "Tơ Đô"),
    ("Sán Chỉ", "Sán Chỉ"),
    ("Nùng", "Nùng"),
    ("Hmông", "Hmông"),
    ("Ai", "Ai"),
    ("Phú Lạo", "Phú Lạo"),
    ("Lô Lô", "Lô Lô"),
    ("Sán Dìu", "Sán Dìu"),
    ("Hà Nhì", "Hà Nhì"),
    ("Phù Lá", "Phù Lá"),
    ("Lahu", "Lahu"),
    ("Ơ Đu", "Ơ Đu"),
    ("Mảng", "Mảng"),
    ("Khơ Mú", "Khơ Mú"),
    ("Giáy", "Giáy"),
    ("Kor", "Kor"),
    ("Tu Dì", "Tu Dì"),
    ("Mạ", "Mạ"),
    ("Chơ Ro", "Chơ Ro"),
    ("Xinh Mun", "Xinh Mun"),
    ("Công", "Công"),
    ("Chứt", "Chứt"),
    ("Bru-Vân Kiều", "Bru-Vân Kiều"),
    ("Ế Đê", "Ế Đê"),
    ("Gia Rai", "Gia Rai"),
    ("Ê Đê", "Ê Đê"),
    ("Ba Na", "Ba Na"),
    ("Xơ Đăng", "Xơ Đăng"),
    ("Cơ Tu", "Cơ Tu"),
    ("Hrê", "Hrê"),
    ("Mnong", "Mnong"),
    ("Raglai", "Raglai"),
    ("Tà Ôi", "Tà Ôi"),
    ("Kơ Ho", "Kơ Ho"),
    ("Giẻ Triêng", "Giẻ Triêng"),
    ("Pà Thẻn", "Pà Thẻn"),
    ("Rơ Măm", "Rơ Măm"),
    ("Brâu", "Brâu"),
    ("Sò Drai", "Sò Drai"),
    ("Mã Liềng", "Mã Liềng"),
    ("Cơ Lao", "Cơ Lao"),
    ("La Chí", "La Chí"),
    ("Người Dao", "Người Dao"),
    ("Sô La", "Sô La"),
    ("Sắc", "Sắc"),
    ("La Hú", "La Hú"),
]

ETHNIC_GROUPS_NO_KINH = [item for item in ETHNIC_GROUPS if item[0] != "Kinh"]
EMPTY_CHOICE = [("", "------")]

PROVINCE_CITY_CHOICES = [
    ("", "------"),
    ("Tuyên Quang", "Tuyên Quang"),
    ("Cao Bằng", "Cao Bằng"),
    ("Lai Châu", "Lai Châu"),
    ("Lào Cai", "Lào Cai"),
    ("Thái Nguyên", "Thái Nguyên"),
    ("Điện Biên", "Điện Biên"),
    ("Lạng Sơn", "Lạng Sơn"),
    ("Sơn La", "Sơn La"),
    ("Phú Thọ", "Phú Thọ"),
    ("Bắc Ninh", "Bắc Ninh"),
    ("Quảng Ninh", "Quảng Ninh"),
    ("Hà Nội", "Hà Nội"),
    ("Hải Phòng", "Hải Phòng"),
    ("Hưng Yên", "Hưng Yên"),
    ("Ninh Bình", "Ninh Bình"),
    ("Thanh Hóa", "Thanh Hóa"),
    ("Nghệ An", "Nghệ An"),
    ("Hà Tĩnh", "Hà Tĩnh"),
    ("Quảng Trị", "Quảng Trị"),
    ("Huế", "Huế"),
    ("Đà Nẵng", "Đà Nẵng"),
    ("Quảng Ngãi", "Quảng Ngãi"),
    ("Gia Lai", "Gia Lai"),
    ("Đắk Lắk", "Đắk Lắk"),
    ("Khánh Hoà", "Khánh Hoà"),
    ("Lâm Đồng", "Lâm Đồng"),
    ("Đồng Nai", "Đồng Nai"),
    ("Tây Ninh", "Tây Ninh"),
    ("Hồ Chí Minh", "Hồ Chí Minh"),
    ("Đồng Tháp", "Đồng Tháp"),
    ("An Giang", "An Giang"),
    ("Vĩnh Long", "Vĩnh Long"),
    ("Cần Thơ", "Cần Thơ"),
    ("Cà Mau", "Cà Mau"),
]


class ChiBoForm(forms.ModelForm):
    TRANG_THAI_CHOICES = [
        ("Đang hoạt động", "Đang hoạt động"),
        ("Ngừng hoạt động", "Ngừng hoạt động"),
    ]
    
    DIA_BAN_CHOICES = [
        ("Nại Hiên Đông", "Nại Hiên Đông"),
        ("Mân Thái", "Mân Thái"),
        ("Thọ Quang", "Thọ Quang"),
    ]

    class Meta:
        model = ChiBo
        fields = ["TenChiBo", "DiaBan", "TrangThai"]
        labels = {
            "TenChiBo": "Tên Chi bộ",
            "DiaBan": "Địa bàn",
            "TrangThai": "Trạng thái",
        }

    def __init__(self, *args, **kwargs):
        self.dang_bo = kwargs.pop("dang_bo", None)
        super().__init__(*args, **kwargs)
        self.fields["TenChiBo"].widget.attrs.update(
            {"placeholder": "Ví dụ: Chi bộ Công an Phường Sơn Trà"}
        )
        self.fields["TrangThai"] = forms.ChoiceField(
            choices=self.TRANG_THAI_CHOICES,
            label="Trạng thái",
            initial="Đang hoạt động",
        )
        self.fields["DiaBan"] = forms.ChoiceField(
            choices=self.DIA_BAN_CHOICES,
            label="Địa bàn",
        )
    
    def clean(self):
        cleaned_data = super().clean()
        ten_chi_bo = cleaned_data.get("TenChiBo")
        dia_ban = cleaned_data.get("DiaBan")
        
        valid_dia_ban = [choice[0] for choice in self.DIA_BAN_CHOICES]
        if dia_ban and dia_ban not in valid_dia_ban:
            self.add_error("DiaBan", f"Địa bàn phải là một trong: {', '.join(valid_dia_ban)}")

        if ten_chi_bo:
            input_key = ChiBo.normalized_name_key(ten_chi_bo)
            candidates = ChiBo.objects.select_related("DangBoID")
            if self.dang_bo is not None:
                candidates = candidates.filter(DangBoID=self.dang_bo)
            if self.instance.pk:
                candidates = candidates.exclude(pk=self.instance.pk)

            for existing in candidates:
                if ChiBo.normalized_name_key(existing.TenChiBo) == input_key:
                    self.add_error(
                        "TenChiBo",
                        f"Chi bộ đã tồn tại trong hệ thống (trùng với '{existing.TenChiBo}').",
                    )
                    break
        
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.dang_bo is None:
            raise forms.ValidationError("Không tìm thấy Đảng bộ mặc định.")
        instance.DangBoID = self.dang_bo
        if commit:
            instance.save()
        return instance


class ChiBoImportForm(forms.Form):
    import_file = forms.FileField(
        label="File import Chi bộ",
        help_text="Chấp nhận .csv hoặc .xlsx.",
    )


class DangVienForm(forms.ModelForm):
    TRANG_THAI_SINH_HOAT_CHOICES = [
        ("Đang sinh hoạt", "Đang sinh hoạt"),
        ("Chuyển sinh hoạt", "Chuyển sinh hoạt"),
        ("Nghỉ", "Nghỉ"),
    ]
    
    SoCCCD = forms.CharField(
        label="Số CCCD",
        max_length=12,
        widget=forms.TextInput(attrs={"placeholder": "12 chữ số", "maxlength": "12", "inputmode": "numeric", "pattern": "[0-9]*"}),
    )

    SoDienThoai = forms.CharField(
        required=True,
        label="Số điện thoại",
        max_length=10,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Nhập số điện thoại",
                "maxlength": "10",
                "inputmode": "numeric",
                "pattern": "[0-9]*",
            }
        ),
    )

    class Meta:
        model = DangVien
        fields = [
            "SoCCCD",
            "HoTen",
            "BiDanh",
            "GioiTinh",
            "NgaySinh",
            "QueQuan",
            "DanToc",
            "NoiThuongTru",
            "NoiTamTru",
            "NgheNghiep",
            "GDPT",
            "GDNN",
            "GDDH",
            "GDSĐH",
            "HocHam",
            "LyLuanChinhTri",
            "NgoaiNgu",
            "TinHoc",
            "TiengDTTS",
            "NgayVaoDang",
            "ChiBoID",
            "DienDangVien",
            "TrangThaiSinhHoat",
            "SoDienThoai",
            "GhiChu",
            "HuyHieuCaoNhat",
            "SoHuyHieu",
        ]
        labels = {
            "SoCCCD": "Số CCCD",
            "HoTen": "Họ và tên",
            "BiDanh": "Bí danh",
            "GioiTinh": "Giới tính",
            "NgaySinh": "Ngày sinh",
            "QueQuan": "Quê quán",
            "DanToc": "Dân tộc",
            "NoiThuongTru": "Nơi thường trú",
            "NoiTamTru": "Nơi tạm trú",
            "NgheNghiep": "Nghề nghiệp",
            "GDPT": "Giáo dục phổ thông",
            "GDNN": "Giáo dục nghề nghiệp",
            "GDDH": "Giáo dục đại học",
            "GDSĐH": "Giáo dục sau đại học",
            "HocHam": "Học hàm",
            "LyLuanChinhTri": "Lý luận chính trị",
            "NgoaiNgu": "Ngoại ngữ",
            "TinHoc": "Tin học",
            "TiengDTTS": "Tiếng dân tộc thiểu số",
            "NgayVaoDang": "Ngày vào Đảng (kết nạp)",
            "ChiBoID": "Chi bộ",
            "DienDangVien": "Diện Đảng viên",
            "TrangThaiSinhHoat": "Trạng thái sinh hoạt",
            "SoDienThoai": "Số điện thoại",
            "GhiChu": "Ghi chú",
            "HuyHieuCaoNhat": "Huy hiệu cao nhất",
            "SoHuyHieu": "Số huy hiệu",
        }
        widgets = {
            "NgaySinh": forms.DateInput(attrs={"type": "date"}),
            "NgayVaoDang": forms.DateInput(attrs={"type": "date"}),
            "GhiChu": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        self.dang_bo = kwargs.pop("dang_bo", None)
        super().__init__(*args, **kwargs)
        chi_bo_queryset = ChiBo.objects.select_related("DangBoID")
        if self.dang_bo is not None:
            chi_bo_queryset = chi_bo_queryset.filter(DangBoID=self.dang_bo)
        self.fields["ChiBoID"].queryset = chi_bo_queryset.order_by("TenChiBo")

        self.fields["QueQuan"].widget = forms.Select(choices=PROVINCE_CITY_CHOICES)
        self.fields["QueQuan"].required = True

        self.fields["GioiTinh"].choices = EMPTY_CHOICE + [
            choice for choice in self.fields["GioiTinh"].choices if choice[0] != ""
        ]

        self.fields["DanToc"].widget = forms.Select(choices=EMPTY_CHOICE + ETHNIC_GROUPS)
        self.fields["DanToc"].required = True

        self.fields["DienDangVien"].widget = forms.Select(choices=EMPTY_CHOICE + DangVien.DIEN_DANG_VIEN_CHOICES)
        self.fields["DienDangVien"].required = True
        
        self.fields["TrangThaiSinhHoat"].widget = forms.Select(choices=EMPTY_CHOICE + self.TRANG_THAI_SINH_HOAT_CHOICES)

        self.fields["ChiBoID"].empty_label = "------"
        
        # GDPT: Chọn 1/12, 2/12, ..., 12/12 hoặc Không
        gdpt_choices = [("Không", "Không")] + [(f"{i}/12", f"{i}/12") for i in range(1, 13)]
        self.fields["GDPT"].widget = forms.Select(choices=EMPTY_CHOICE + gdpt_choices)
        self.fields["GDPT"].required = False
        
        # GDNN: Điền hoặc chọn Không
        self.fields["GDNN"].widget.attrs.update({"placeholder": "VD: Kỹ sư điện, ..."})
        self.fields["GDNN"].required = True
        
        # GDDH: Điền hoặc chọn Không, gợi ý các giá trị
        self.fields["GDDH"].widget.attrs.update({"placeholder": "VD: Kỹ sư cơ khí,..."})
        self.fields["GDDH"].required = True
        
        # GDSĐH: Điền hoặc chọn Không, gợi ý các giá trị
        self.fields["GDSĐH"].widget.attrs.update({"placeholder": "VD: Thạc sỹ kinh tế, ... "})
        self.fields["GDSĐH"].required = True
        
        # HocHam: Ghi chức danh được nhà nước phong
        self.fields["HocHam"].widget.attrs.update({"placeholder": "VD: Giáo sư, Phó giáo sư,... "})
        self.fields["HocHam"].required = True
        
        # LyLuanChinhTri: Chọn từ sơ cấp, trung cấp, cao cấp, cử nhân hoặc Không
        ly_luan_choices = [
            ("Không", "Không"),
            ("Sơ cấp", "Sơ cấp"),
            ("Trung cấp", "Trung cấp"),
            ("Cao cấp", "Cao cấp"),
            ("Cử nhân", "Cử nhân"),
        ]
        self.fields["LyLuanChinhTri"].widget = forms.Select(choices=EMPTY_CHOICE + ly_luan_choices)
        self.fields["LyLuanChinhTri"].required = True
        
        # NgoaiNgu: Chọn Không hoặc nhập
        self.fields["NgoaiNgu"].widget.attrs.update({"placeholder": "VD: Đại học tiếng Anh, tiếng Pháp,..."})
        self.fields["NgoaiNgu"].required = True
        
        # TinHoc: Chọn Không hoặc nhập
        self.fields["TinHoc"].widget.attrs.update({"placeholder": "VD: Tin học văn phòng, trình độ A/B/C,..."})
        self.fields["TinHoc"].required = True
        
        # TiengDTTS: Chọn từ danh sách dân tộc thiểu số hoặc Không (loại trừ Kinh)
        tieng_dtts_choices = [("Không", "Không")] + ETHNIC_GROUPS_NO_KINH
        self.fields["TiengDTTS"].widget = forms.Select(choices=EMPTY_CHOICE + tieng_dtts_choices)
        self.fields["TiengDTTS"].required = True

        # Huy hiệu cao nhất: Dropdown từ 30 đến 90
        badge_choices = [("", "------")] + [(f"{m} năm", f"{m} năm") for m in [30, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90]]
        self.fields["HuyHieuCaoNhat"].widget = forms.Select(choices=badge_choices)

        # Theo nghiệp vụ hiện tại: tất cả trường bắt buộc, trừ Ghi chú và Huy hiệu.
        optional_fields = {"GhiChu", "NgayVaoDang", "HuyHieuCaoNhat"}
        for field_name, field in self.fields.items():
            field.required = field_name not in optional_fields

    def clean(self):
        cleaned_data = super().clean()

        # Với các trường văn bản trình độ/chuyên môn, nếu để trống thì quy ước lưu 'Không'.
        for field_name in ["GDNN", "GDDH", "GDSĐH", "HocHam", "NgoaiNgu", "TinHoc"]:
            value = (cleaned_data.get(field_name) or "").strip()
            cleaned_data[field_name] = value or "Không"

        dien_dang_vien = cleaned_data.get("DienDangVien")
        ngay_vao_dang = cleaned_data.get("NgayVaoDang")
        if dien_dang_vien != "BI_XOA_TEN" and not ngay_vao_dang:
            self.add_error("NgayVaoDang", "Ngày vào Đảng là bắt buộc trừ khi diện Đảng viên là Bị xóa tên.")
        if dien_dang_vien == "BI_XOA_TEN":
            cleaned_data["NgayVaoDang"] = None
        
        # Validate SoCCCD is exactly 12 digits
        so_cccd = cleaned_data.get("SoCCCD")
        if so_cccd:
            so_cccd = so_cccd.strip()
            cleaned_data["SoCCCD"] = so_cccd
            if not so_cccd.isdigit() or len(so_cccd) != 12:
                self.add_error("SoCCCD", "Số CCCD phải là 12 chữ số")
            else:
                # Check if SoCCCD already exists
                existing = DangVien.objects.filter(SoCCCD=so_cccd)
                if self.instance.pk:
                    existing = existing.exclude(pk=self.instance.pk)
                if existing.exists():
                    self.add_error("SoCCCD", "Đã tồn tại Đảng viên")

        so_dien_thoai = cleaned_data.get("SoDienThoai")
        if so_dien_thoai:
            so_dien_thoai = so_dien_thoai.strip()
            cleaned_data["SoDienThoai"] = so_dien_thoai
            if not so_dien_thoai.isdigit() or len(so_dien_thoai) != 10:
                self.add_error("SoDienThoai", "Số điện thoại phải là 10 chữ số")
        
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.dang_bo is None:
            raise forms.ValidationError("Không tìm thấy Đảng bộ mặc định.")
        instance.DangBoID = self.dang_bo

        # Nếu người dùng không chọn HuyHieuCaoNhat, xóa để model tự tính từ NgayVaoDang
        if not self.cleaned_data.get("HuyHieuCaoNhat"):
            instance.HuyHieuCaoNhat = None

        if commit:
            instance.save()
        return instance


class DangVienImportForm(forms.Form):
    import_file = forms.FileField(
        label="File import Đảng viên",
        help_text="Chấp nhận .csv hoặc .xlsx. Mã Đảng viên sẽ tự động tạo.",
    )


class HuyHieuImportForm(forms.Form):
    import_file = forms.FileField(
        label="File import Huy hiệu",
        help_text="Chấp nhận .csv hoặc .xlsx. Chỉ nhập cho Đảng viên đã tồn tại.",
    )


class HuyHieuLegacyForm(forms.Form):
    MaDangVien = forms.CharField(required=False, label="Mã Đảng viên")
    SoCCCD = forms.CharField(required=False, label="Số CCCD")
    LoaiHuyHieu = forms.CharField(required=True, label="Loại huy hiệu", max_length=255)
    NgayDuDieuKien = forms.DateField(required=True, label="Ngày đủ điều kiện", widget=forms.DateInput(attrs={"type": "date"}))
    DotTraoTang = forms.CharField(required=True, label="Đợt trao tặng", max_length=50)
    TrangThai = forms.CharField(required=True, label="Trạng thái", max_length=50)
    SoQuyetDinh = forms.CharField(required=True, label="Số quyết định", max_length=50)
    NgayTrao = forms.DateField(required=True, label="Ngày trao", widget=forms.DateInput(attrs={"type": "date"}))
    GhiChu = forms.CharField(required=False, label="Ghi chú", widget=forms.Textarea(attrs={"rows": 2}))

    def clean(self):
        cleaned_data = super().clean()
        ma_dang_vien = (cleaned_data.get("MaDangVien") or "").strip()
        so_cccd = (cleaned_data.get("SoCCCD") or "").strip()
        if not ma_dang_vien and not so_cccd:
            raise forms.ValidationError("Cần nhập Mã Đảng viên hoặc Số CCCD để xác định Đảng viên.")

        loai_huy_hieu = cleaned_data.get("LoaiHuyHieu")
        so_quyet_dinh = cleaned_data.get("SoQuyetDinh")
        badge_year = parse_badge_year(loai_huy_hieu)
        is_valid, error_message = validate_badge_decision_number(so_quyet_dinh, badge_year)
        if not is_valid:
            self.add_error("SoQuyetDinh", error_message)

        return cleaned_data


class HuyHieuEditForm(forms.ModelForm):
    class Meta:
        model = HuyHieuDang
        fields = [
            "LoaiHuyHieu",
            "NgayDuDieuKien",
            "DotTraoTang",
            "TrangThai",
            "SoQuyetDinh",
            "NgayTrao",
            "GhiChu",
        ]
        labels = {
            "LoaiHuyHieu": "Loại huy hiệu",
            "NgayDuDieuKien": "Ngày đủ điều kiện",
            "DotTraoTang": "Đợt trao tặng",
            "TrangThai": "Trạng thái",
            "SoQuyetDinh": "Số quyết định",
            "NgayTrao": "Ngày trao",
            "GhiChu": "Ghi chú",
        }
        widgets = {
            "NgayDuDieuKien": forms.DateInput(attrs={"type": "date"}),
            "NgayTrao": forms.DateInput(attrs={"type": "date"}),
            "GhiChu": forms.Textarea(attrs={"rows": 2}),
        }

    def clean(self):
        cleaned_data = super().clean()
        loai_huy_hieu = cleaned_data.get("LoaiHuyHieu")
        so_quyet_dinh = cleaned_data.get("SoQuyetDinh")
        badge_year = parse_badge_year(loai_huy_hieu)
        is_valid, error_message = validate_badge_decision_number(so_quyet_dinh, badge_year)
        if not is_valid:
            self.add_error("SoQuyetDinh", error_message)
        return cleaned_data


class LoginForm(forms.Form):
    """Form đăng nhập"""
    identifier = forms.CharField(
        label="Tên đăng nhập",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Nhập tên đăng nhập hoặc email",
            "autocomplete": "username"
        })
    )
    password = forms.CharField(
        label="Mật khẩu",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Nhập mật khẩu",
            "autocomplete": "current-password"
        })
    )
    remember_me = forms.BooleanField(
        label="Ghi nhớ đăng nhập",
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"})
    )


class SignUpForm(forms.Form):
    """Form đăng ký tài khoản mới"""
    full_name = forms.CharField(
        label="Họ và Tên",
        max_length=300,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Nhập họ và tên của bạn"
        })
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Nhập email của bạn",
            "autocomplete": "email"
        })
    )
    password = forms.CharField(
        label="Mật khẩu",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Nhập mật khẩu (tối thiểu 8 ký tự)",
            "autocomplete": "new-password"
        })
    )
    password_confirm = forms.CharField(
        label="Xác nhận mật khẩu",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Nhập lại mật khẩu",
            "autocomplete": "new-password"
        })
    )

    def clean_email(self):
        from django.contrib.auth.models import User
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email này đã được sử dụng.")
        return email

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if len(password) < 8:
            raise forms.ValidationError("Mật khẩu phải có ít nhất 8 ký tự.")
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Mật khẩu không khớp.")
        return cleaned_data
