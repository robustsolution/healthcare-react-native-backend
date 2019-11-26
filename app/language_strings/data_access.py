from db_util import get_connection
from web_errors import WebError


def language_string_data_by_id(id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT language, content FROM string_content WHERE id = %s',
                        [id])
            yield from cur
