from datetime import datetime as dt
from decimal import Decimal

def _to_bool(val: str) -> bool:
    """Return True for 'on', 'true', '1' (case‑insensitive)."""
    return str(val).lower() in {"1", "true", "on", "yes"}

def parse_date(field, data):
    try:
        return dt.fromisoformat(data.get(field))
    except (TypeError, ValueError):
        return None

def parse_int(field, data, default=0):
    try:
        return int(data.get(field, default))
    except (TypeError, ValueError):
        return default

def parse_decimal(field, data, default="0"):
    try:
        return Decimal(data.get(field, default))
    except (TypeError, ValueError, Decimal.InvalidOperation):
        return Decimal(default)