from db_util import get_connection
from datetime import datetime


def language_string_data_by_id(id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT language, content FROM string_content WHERE id = %s',
                        [id])
            yield from cur


def update_language_string(language_string):
    if language_string is None:
        return
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO string_ids (id) VALUES (%s) ON CONFLICT (id) DO NOTHING",
                        [language_string.id])
            for language, content in language_string.content_by_language.items():
                cur.execute("INSERT INTO string_content (id, language, content, edited_at) " +
                            "VALUES (%s, %s, %s, %s) " +
                            "ON CONFLICT (id, language) DO UPDATE " +
                            "SET content = EXCLUDED.content, edited_at = EXCLUDED.edited_at",
                            [language_string.id, language, content, datetime.now()])
