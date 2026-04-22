import datetime
import re

BADGE_MILESTONES = (30, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90)

BADGE_DECISION_RULES = {
    50: {"prefix": "", "digits": 6, "range": "000001-999999"},
    55: {"prefix": "D", "digits": 6, "range": "D000001-D999999"},
    60: {"prefix": "", "digits": 5, "range": "00001-99999"},
    65: {"prefix": "C", "digits": 5, "range": "C00001-C99999"},
    70: {"prefix": "", "digits": 4, "range": "0001-9999"},
    75: {"prefix": "B", "digits": 4, "range": "B0001-B9999"},
    80: {"prefix": "", "digits": 3, "range": "001-999"},
    85: {"prefix": "A", "digits": 3, "range": "A001-A999"},
    90: {"prefix": "", "digits": 3, "range": "001-999"},
}

CEREMONY_DEFINITIONS = (
    ("3-2", "3/2", "Kỷ niệm ngày thành lập Đảng"),
    ("19-5", "19/5", "Sinh nhật Bác Hồ"),
    ("2-9", "2/9", "Quốc khánh"),
    ("7-11", "7/11", "Ngày Cách mạng Tháng Mười"),
)


def add_years(base_date, years):
    try:
        return base_date.replace(year=base_date.year + years)
    except ValueError:
        # Handle Feb 29 -> Feb 28 for non-leap year.
        return base_date.replace(month=2, day=28, year=base_date.year + years)


def calculate_party_age_at_date(ngay_vao_dang, review_date):
    years = review_date.year - ngay_vao_dang.year
    if (review_date.month, review_date.day) < (ngay_vao_dang.month, ngay_vao_dang.day):
        years -= 1
    return max(years, 0)


def parse_badge_year(loai_huy_hieu):
    if loai_huy_hieu is None:
        return None

    if isinstance(loai_huy_hieu, int):
        return loai_huy_hieu

    text = str(loai_huy_hieu)
    match = re.search(r"(\d{2})", text)
    if not match:
        return None
    return int(match.group(1))


def validate_badge_decision_number(so_quyet_dinh, badge_year):
    """Validate decision number format by badge year.

    Supports optional locality prefix, e.g. "HN 000001" or "HN D000001".
    """
    text = str(so_quyet_dinh or "").strip().upper()
    if not text:
        return True, None

    rule = BADGE_DECISION_RULES.get(int(badge_year)) if badge_year is not None else None
    if not rule:
        return True, None

    prefix = rule["prefix"]
    digits = rule["digits"]
    expected_range = rule["range"]

    core_pattern = rf"{prefix}\\d{{{digits}}}" if prefix else rf"\\d{{{digits}}}"
    full_pattern = re.compile(rf"^(?:[A-Z]{{1,5}}[\\s-]+)?(?P<core>{core_pattern})$")
    match = full_pattern.fullmatch(text)
    if not match:
        return False, (
            f"Số quyết định không đúng định dạng cho Huy hiệu {badge_year} năm. "
            f"Định dạng hợp lệ: {expected_range} (cho phép thêm tiền tố địa phương như 'HN ')."
        )

    core = match.group("core")
    numeric_part = core[len(prefix):] if prefix else core
    if int(numeric_part) <= 0:
        return False, (
            f"Số quyết định cho Huy hiệu {badge_year} năm phải nằm trong khoảng {expected_range}."
        )

    return True, None


def get_ceremony_dates(year):
    dates = []
    for key, short_name, name in CEREMONY_DEFINITIONS:
        day, month = key.split("-")
        review_date = datetime.date(year, int(month), int(day))
        dates.append(
            {
                "key": key,
                "date": review_date,
                "date_iso": review_date.isoformat(),
                "short_name": short_name,
                "name": name,
            }
        )
    return dates


def is_eligible_for_badge(dang_vien, review_date, badge_year, awarded_badges):
    if not dang_vien.NgayVaoDang:
        return False

    already_awarded = any(
        badge.DangVienID_id == dang_vien.DangVienID and parse_badge_year(badge.LoaiHuyHieu) == badge_year
        for badge in awarded_badges
    )
    if already_awarded:
        return False

    # Theo quy định mới: Có thể trao sớm nếu trong năm đó Đảng viên đủ tuổi Đảng
    # Tức là chỉ cần năm (review_date.year - NgayVaoDang.year) >= badge_year
    year_diff = review_date.year - dang_vien.NgayVaoDang.year
    return year_diff >= badge_year


def get_eligible_members(dang_viens, review_date, badge_year, awarded_badges):
    years_to_check = [badge_year] if badge_year else list(BADGE_MILESTONES)
    years_to_check.sort()

    eligible = []

    for dang_vien in dang_viens:
        for years in years_to_check:
            if is_eligible_for_badge(dang_vien, review_date, years, awarded_badges):
                eligible_date = add_years(dang_vien.NgayVaoDang, years)
                
                # Đảng viên được coi là "trao sớm" nếu ngày đủ điều kiện thực tế 
                # nằm sau ngày đợt trao (review_date) nhưng vẫn trong cùng năm.
                is_early = eligible_date > review_date

                eligible.append(
                    {
                        "dang_vien": dang_vien,
                        "eligible_for_years": years,
                        "party_age": calculate_party_age_at_date(dang_vien.NgayVaoDang, review_date),
                        "eligible_date": eligible_date,
                        "is_early": is_early,
                    }
                )
                break

    return eligible
