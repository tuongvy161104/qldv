from django.core.management.base import BaseCommand
from qldv.models import DangVien


class Command(BaseCommand):
    help = 'Xóa tất cả dữ liệu đảng viên'

    def handle(self, *args, **options):
        count = DangVien.objects.count()
        if count == 0:
            self.stdout.write(self.style.WARNING('Không có dữ liệu đảng viên để xóa.'))
            return
        
        DangVien.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'Đã xóa thành công {count} đảng viên.'))
