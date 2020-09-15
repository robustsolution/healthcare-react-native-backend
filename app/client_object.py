from datetime import datetime, timezone, date
from language_strings.language_string import LanguageString


class ClientObject:
    @classmethod
    def table_name(cls):
        raise NotImplementedError()

    @classmethod
    def db_columns_from_server(cls):
        raise NotImplementedError()

    @classmethod
    def db_columns_from_client(cls):
        raise NotImplementedError()

    @classmethod
    def client_insert_sql(cls):
        raise NotImplementedError()

    def client_insert_values(self):
        raise NotImplementedError()

    @classmethod
    def client_update_sql(cls):
        raise NotImplementedError()

    def client_update_values(self):
        raise NotImplementedError()

    @classmethod
    def server_insert_sql(cls):
        raise NotImplementedError()

    def server_insert_values(self):
        raise NotImplementedError()

    @classmethod
    def server_update_sql(cls):
        raise NotImplementedError()

    def server_update_values(self):
        raise NotImplementedError()    

    def dependencies(self):
        """
        If a new client object has a foreign key into another object type
        (other than LanguageString), add it here so that the DbSynchronization
        class can handle it properly. For example, this method for the Event
        object could return

        {'patient_id': Patient, 'visit_id', Visit}

        """
        return {}

    @staticmethod
    def format_ts(dt: datetime):
        return dt.astimezone(timezone.utc).isoformat().replace('+00:00', 'Z')

    @staticmethod
    def format_string(s: LanguageString):
        if s is None:
            return None
        else:
            return s.id.replace('-', '')

    @staticmethod
    def make_language_string(s):
        if s is None:
            return None
        else:
            return LanguageString(s, {})

    @staticmethod
    def format_date(d: date):
        return str(d)

    @staticmethod
    def format_bool(b: bool):
        if b:
            return 1
        else:
            return 0
