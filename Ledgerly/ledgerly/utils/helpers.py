
from datetime import datetime, date
from .config import DATE_FORMAT, CURRENCY_SYMBOL

def format_currency(amount):
    """Format amount with currency symbol"""
    return f"{CURRENCY_SYMBOL}{amount:,.2f}"

def parse_date(date_str):
    """Parse date string or return today's date"""
    if date_str == "today":
        return date.today()
    elif isinstance(date_str, str):
        try:
            return datetime.strptime(date_str, DATE_FORMAT).date()
        except ValueError:
            return date.today()
    return date_str
