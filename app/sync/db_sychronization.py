from werkzeug.datastructures import FileStorage
from tempfile import NamedTemporaryFile
import sqlite3
import os


class DbSynchronizer:
    def __init__(self, client_db_file: FileStorage):
        self.client_db_filename = self._write_client_db_to_tempfile(client_db_file)
        self.client_conn = sqlite3.connect(self.client_db_filename)
        self._test_client_db()

    def do_sync(self):
        self.server_sql_commands = []
        self.client_sql_commands = []
        return True

    def get_client_sql(self):
        return self.client_sql_commands

    def __del__(self):
        print('Garbage collecting uploaded client DB.')
        os.remove(self.client_db_filename)

    def _test_client_db(self):
        c = self.client_conn.cursor()
        c.execute("SELECT COUNT(*) FROM patients")
        [num_patients] = c.fetchone()
        print(f'Opened DB from client with {num_patients} patients.')

    @staticmethod
    def _write_client_db_to_tempfile(client_db_file: FileStorage):
        handle = NamedTemporaryFile('wb', delete=False, suffix='.db')
        client_db_file.save(handle)
        handle.close()
        return handle.name
