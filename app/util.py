from datetime import datetime, timezone


def identity(x):
    return x


def parse_client_timestamp(ts: str):
    return datetime.strptime(ts, '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=timezone.utc)
