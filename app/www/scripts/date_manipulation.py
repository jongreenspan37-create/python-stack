import calendar
from datetime import date, timedelta


def _add_months(d, months):
    month_index = d.month - 1 + months
    year = d.year + month_index // 12
    month = month_index % 12 + 1
    day = min(d.day, calendar.monthrange(year, month)[1])
    return date(year, month, day)


def _add_years(d, years):
    year = d.year + years
    day = d.day
    if d.month == 2 and d.day == 29 and not calendar.isleap(year):
        day = 28
    return date(year, d.month, day)


def adjust_date(body):
    try:
        base = date.fromisoformat(body["date"])
        amount = int(body["amount"])
        unit = body["unit"]
    except (KeyError, TypeError, ValueError):
        return {"error": "invalid date, amount, or unit"}

    if unit == "day":
        result = base + timedelta(days=amount)
    elif unit == "month":
        result = _add_months(base, amount)
    elif unit == "year":
        result = _add_years(base, amount)
    else:
        return {"error": "unit must be day, month, or year"}

    return {"result": result.isoformat()}
