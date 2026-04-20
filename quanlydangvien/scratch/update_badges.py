import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quanlydangvien.settings')
django.setup()

from qldv.models import DangVien

def update_all_badges():
    dvs = DangVien.objects.all()
    count = dvs.count()
    print(f"Updating badges for {count} members...")
    for i, dv in enumerate(dvs):
        dv.update_highest_badge()
        if i % 100 == 0:
            print(f"Processed {i}/{count}")
    print("Done!")

if __name__ == "__main__":
    update_all_badges()
