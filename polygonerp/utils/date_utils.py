from datetime import date, timedelta


def get_dates_for_current_month():
    today = date.today()
    first_day = date(today.year, today.month, 1)
    next_month = date(today.year + int(today.month / 12), (today.month % 12) + 1, 1)
    delta = (next_month - first_day).days
    return [first_day + timedelta(days=i) for i in range(delta)]