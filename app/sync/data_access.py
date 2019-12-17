from db_util import get_connection


def get_ids_and_edit_timestamps(table_name):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(f'SELECT id, edited_at FROM {table_name}')
            return {k.replace('-', ''): ts for k, ts in cur}


def get_table_rows(object_type, ids):
    table_name = object_type.table_name()
    columns, constructors = zip(*object_type.db_columns())
    column_select_str = ', '.join(columns)
    with get_connection() as conn:
        with conn.cursor() as cur:
            for id in ids:
                cur.execute(f'SELECT {column_select_str} FROM {table_name} WHERE id = %s', [id])
                row = cur.fetchone()
                if row:
                    values = [c(r) for c, r in zip(constructors, row)]
                    yield object_type(**dict(zip(columns, values)))


def get_string_ids_and_edit_timestamps():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, language, edited_at FROM string_content)")
            return {(id, lang): ts for id, lang, ts in cur}