from web_errors import WebError
from typing import Set, Dict
from flask import Request


def assert_data_has_keys(request: Request, keys: Set[str]):
    data = request.get_json(force=True)
    if set(data.keys()).issuperset(keys):
        return data
    missing = sorted(keys - set(data.keys()))
    raise WebError(f"Required data not supplied: {','.join(missing)}", 400)
