from django.contrib import admin

from .models import ChiBo, DangBo, DangVien, HuyHieuDang


@admin.register(DangBo)
class DangBoAdmin(admin.ModelAdmin):
	list_display = ("DangBoID", "TenDangBo", "CapDangBo", "TrangThai")
	search_fields = ("TenDangBo", "CapDangBo")


@admin.register(ChiBo)
class ChiBoAdmin(admin.ModelAdmin):
	list_display = ("ChiBoID", "TenChiBo", "DiaBan", "TrangThai", "DangBoID")
	list_filter = ("TrangThai", "DiaBan")
	search_fields = ("TenChiBo", "DiaBan")


@admin.register(DangVien)
class DangVienAdmin(admin.ModelAdmin):
	list_display = (
		"DangVienID",
		"MaDangVien",
		"HoTen",
		"GioiTinh",
		"NgaySinh",
		"ChiBoID",
		"TrangThaiSinhHoat",
	)
	list_filter = ("GioiTinh", "TrangThaiSinhHoat", "ChiBoID")
	search_fields = ("MaDangVien", "HoTen", "SoCCCD", "SoDienThoai")


@admin.register(HuyHieuDang)
class HuyHieuDangAdmin(admin.ModelAdmin):
	list_display = ("HuyHieuID", "DangVienID", "LoaiHuyHieu", "NgayDuDieuKien", "NgayTrao", "TrangThai")
	list_filter = ("LoaiHuyHieu", "TrangThai")
	search_fields = ("DangVienID__HoTen", "SoQuyetDinh")


