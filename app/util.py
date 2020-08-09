from datetime import datetime, timezone, date
from typing import Optional, Any

def identity(x):
    return x


def parse_client_timestamp(ts: str):
    try:
        return datetime.strptime(ts, '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=timezone.utc)
    except ValueError:
        return datetime.strptime(ts, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)


def parse_client_date(date_str: str):
    return date.fromisoformat(date_str)


def parse_client_bool(bool_int: int):
    return bool_int != 0

def parse_server_uuid(s: str):
    if s is None:
        return None
    return s.replace('-', '')


def as_string(s: Optional[Any]):
    if s is None:
         return None
    return str(s)