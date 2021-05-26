from db_util import get_connection
from web_errors import WebError
import bcrypt
from language_strings.data_access import update_language_string
from language_strings.language_string import LanguageString
from datetime import datetime
import uuid


def user_data_by_email(email):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT id, name, role, email, hashed_password FROM users WHERE email = %s',
                        [email])
            row = cur.fetchone()
            if not row:
                raise WebError("email not found", status_code=404)
            return row


def user_data_by_id(user_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT id, name, role, email, hashed_password FROM users WHERE id = %s',
                        [user_id])
            row = cur.fetchone()
            if not row:
                raise WebError("id not found", status_code=404)
            return row

def user_name_by_id(user_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT name FROM users WHERE id = %s',
                        [user_id])
            row = cur.fetchone()
            if not row:
                return None
            return LanguageString.from_id(row)


def update_password(user_id, new_password):
    with get_connection() as conn:
        with conn.cursor() as cur:
            new_password_hashed = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
            cur.execute('UPDATE users SET hashed_password = %s WHERE id = %s',
                        [new_password_hashed, user_id])


def add_user(user):
    update_language_string(user.name)
    with get_connection() as conn:
        with conn.cursor() as cur:
            query = '''
            INSERT INTO users (id, name, role, email, hashed_password, edited_at) VALUES (%s, %s, %s, %s, %s, %s);
            '''
            cur.execute(query, [user.id, user.name.id, user.role, user.email, user.hashed_password, datetime.now()])


def create_token(user_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            token = str(uuid.uuid4())
            cur.execute('INSERT INTO tokens (user_id, token) VALUES (%s, %s)', [user_id, token])
            return token


def invalidate_all_tokens(user_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('DELETE FROM tokens WHERE user_id = %s', [user_id])


def user_id_by_token(token):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT user_id FROM tokens WHERE token = %s AND expiry > now()', [token])
            result = cur.fetchone()
            if result:
                return result[0]
            else:
                return None

def all_user_data():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT id, name, role, email, hashed_password FROM users ORDER BY name', [])
            yield from cur

def delete_user_by_id(user_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('DELETE FROM users WHERE id = %s', [user_id])
