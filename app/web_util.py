from werkzeug.datastructures import ImmutableMultiDict

from web_errors import WebError
from typing import Set, Dict
from flask import Request


def assert_data_has_keys(request: Request, keys: Set[str], data_type='json'):
    if data_type == 'json':
        data = request.get_json(force=True)
    elif data_type == 'form':
        data = request.form
    else:
        raise WebError(f'Data type {data_type} not supported')

    provided_keys = set(data.keys())
    if provided_keys.issuperset(keys):
        return data
    missing = sorted(keys - set(provided_keys))
    raise WebError(f"Required data not supplied: {','.join(missing)}", 400)
