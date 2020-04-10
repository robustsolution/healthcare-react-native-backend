from datetime import datetime, timezone, date


def identity(x):
    return x


def parse_client_timestamp(ts: str):
    return datetime.strptime(ts, '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=timezone.utc)


def parse_client_date(date_str: str):
    return date.fromisoformat(date_str)
