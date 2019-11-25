from db_util import get_connection


def get_one():
    query = 'SELECT 1;'

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, [])
            [result] = cur.fetchone()  # Literally, haha
            return result
