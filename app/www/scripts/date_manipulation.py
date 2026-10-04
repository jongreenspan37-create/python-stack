# Adds days, months or years to a date. Called by the date form on index.html.
import calendar
from datetime import date, timedelta


# Adds months, capping the day at the end of the month (Jan 31 + 1 month = Feb 29).
def _add_months(d, months):
    # Count months from January = 0 so // and % handle year boundaries.
    month_index = d.month - 1 + months
    year = d.year + month_index // 12
    month = month_index % 12 + 1
    # monthrange(...)[1] = number of days in that month.
    day = min(d.day, calendar.monthrange(year, month)[1])
    return date(year, month, day)


# Adds years; Feb 29 becomes Feb 28 when the new year isn't a leap year.
def _add_years(d, years):
    year = d.year + years
    day = d.day
    if d.month == 2 and d.day == 29 and not calendar.isleap(year):
        day = 28
    return date(year, d.month, day)


# Body: {"date": "2024-01-31", "amount": 1, "unit": "day" | "month" | "year"}
# Returns {"result": "2024-02-29"} or {"error": ..}
def adjust_date(body):
    try:
        # fromisoformat parses "YYYY-MM-DD" and raises ValueError for bad dates.
        base = date.fromisoformat(body["date"])
        amount = int(body["amount"])
        unit = body["unit"]
    except (KeyError, TypeError, ValueError):
        return {"error": "invalid date, amount, or unit"}

    if unit == "day":
        # timedelta = a length of time; adding days has no end-of-month problem.
        result = base + timedelta(days=amount)
    elif unit == "month":
        result = _add_months(base, amount)
    elif unit == "year":
        result = _add_years(base, amount)
    else:
        return {"error": "unit must be day, month, or year"}

    return {"result": result.isoformat()}
