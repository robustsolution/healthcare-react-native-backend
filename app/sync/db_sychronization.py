from werkzeug.datastructures import FileStorage
from tempfile import NamedTemporaryFile
from language_strings.language_string import LanguageString
from language_strings.individual_language_string import IndividualLanguageString
from clinics.clinic import Clinic
from sync.data_access import get_ids_and_edit_timestamps, get_table_rows, get_string_ids_and_edit_timestamps
import sqlite3
import os
import itertools
import dateutil.parser


class DbSynchronizer:
    def __init__(self, client_db_file: FileStorage):
        self.client_db_filename = self._write_client_db_to_tempfile(client_db_file)
        self.client_conn = sqlite3.connect(self.client_db_filename)
        self._test_client_db()

    def prepare_sync(self):
        self.server_sql = []
        self.client_sql = []

        self._prepare_table_sync(IndividualLanguageString)
        self._prepare_table_sync(Clinic)
        # self._prepare_strings_sync()
        return True

    def get_client_sql(self):
        return self.client_sql

    def _prepare_table_sync(self, object_type):
        table_name = object_type.table_name()
        server_ids = get_ids_and_edit_timestamps(table_name)
        client_ids = self._get_client_ids_and_edit_timestamps(table_name)

        to_add_to_server = []
        to_add_to_client = []
        to_update_on_server = []
        to_update_on_client = []

        for id, ts in client_ids.items():
            if id not in server_ids:
                to_add_to_server.append(id)
            elif ts > server_ids[id]:
                to_update_on_server.append(id)
            else:
                to_update_on_client.append(id)
        for id in server_ids.keys():
            if id not in client_ids:
                to_add_to_client.append(id)

        self.server_sql.extend(itertools.chain(
            self._generate_server_add_sql(object_type, to_add_to_server),
            self._generate_server_update_sql(object_type, to_add_to_server)))

        self.client_sql.extend(itertools.chain(
            self._generate_client_add_sql(object_type, to_add_to_client),
            self._generate_client_update_sql(object_type, to_add_to_client)))

    def _generate_server_add_sql(self, object_type, ids):
        return []

    def _generate_server_update_sql(self, object_type, ids):
        return []

    def _generate_client_add_sql(self, object_type, ids):
        sql = object_type.client_insert_sql()
        values = [obj.client_insert_values() for obj in get_table_rows(object_type, ids)]

        if not values:
            return None

        if isinstance(sql, list):
            result = []
            for i, s in enumerate(sql):
                component_values = []
                for value_tuple in values:
                    component_values.append(value_tuple[i])
                result.append({
                    'sql': s,
                    'values': component_values
                })
            return result
        else:
            return [{
                'sql': sql,
                'values': values
            }]

    def _generate_client_update_sql(self, object_type, ids):
        return []

    def __del__(self):
        print('Garbage collecting uploaded client DB.')
        self.client_conn.close()
        os.remove(self.client_db_filename)

    def _test_client_db(self):
        cur = self.client_conn.cursor()
        cur.execute("SELECT COUNT(*) FROM patients")
        [num_patients] = cur.fetchone()
        print(f'Opened DB from client with {num_patients} patients.')

    def _get_client_ids_and_edit_timestamps(self, table_name):
        cur = self.client_conn.cursor()
        cur.execute(f'SELECT id, edited_at FROM {table_name}')
        return {k: dateutil.parser.parse(ts) for k, ts in cur}

    def _get_string_client_ids_and_edit_timestamps(self):
        cur = self.client_conn.cursor()
        cur.execute(f'SELECT id, language, edited_at FROM string_content')
        return {(id, lang): dateutil.parser.parse(ts) for id, lang, ts in cur}

    @staticmethod
    def _write_client_db_to_tempfile(client_db_file: FileStorage):
        handle = NamedTemporaryFile('wb', delete=False, suffix='.db')
        client_db_file.save(handle)
        handle.close()
        return handle.name
