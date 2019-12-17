from dataclasses import dataclass
from language_strings.language_string import LanguageString
from client_object import ClientObject
from datetime import datetime
from util import identity


@dataclass
class Clinic(ClientObject):
    id: str
    name: LanguageString
    edited_at: datetime

    def client_insert_values(self):
        return [self.id, self.name.id.replace('-', ''), self.format_ts(self.edited_at)]

    @classmethod
    def client_insert_sql(cls):
        return """INSERT INTO clinics (id, name, edited_at) VALUES (?, ?, ?)"""

    @classmethod
    def db_columns(cls):
        return [('id', lambda s: s.replace('-', '')),
                ('name', lambda x: LanguageString(x, {})),
                ('edited_at', identity)]

    @classmethod
    def table_name(cls):
        return "clinics"

