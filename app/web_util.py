from werkzeug.datastructures import ImmutableMultiDict

from web_errors import WebError
from typing import Set, Dict
from flask import Request, request
from functools import wraps
from users.data_access import user_id_by_token
from users.user import User


def assert_data_has_keys(request_arg: Request, keys: Set[str], data_type='json'):
    if data_type == 'json':
        data = request_arg.get_json(force=True)
    elif data_type == 'form':
        data = request_arg.form
    else:
        raise WebError(f'Data type {data_type} not supported')

    provided_keys = set(data.keys())
    if provided_keys.issuperset(keys):
        return data
    missing = sorted(keys - set(provided_keys))
    raise WebError(f"Required data not supplied: {','.join(missing)}", 400)


# Decorator for endpoints specifically requiring admin access
def admin_authenticated(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'Authorization' not in request.headers:
            raise WebError('Authorization header must be supplied', 401)
        user_id = user_id_by_token(request.headers['Authorization'])
        if user_id is None:
            raise WebError('Invalid token', 401)

        user = User.from_id(user_id)
        if user.role not in ('admin', 'super_admin'):
            raise WebError("Admin Authentication required", 403)

        return f(user, *args, **kwargs)
    return wrap