from config import PG_USER, PG_PASSWORD, PG_HOST, PG_DB
import psycopg2


def get_connection():
    return psycopg2.connect(host=PG_HOST, database=PG_DB, user=PG_USER, password=PG_PASSWORD)
