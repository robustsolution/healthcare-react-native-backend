from dataclasses import dataclass
from client_object import ClientObject
from datetime import datetime
from util import identity, parse_client_timestamp


@dataclass
class IndividualLanguageString(ClientObject):
    id: str
    language: str
    content: str
    edited_at: datetime

    def client_insert_values(self):
        return [[self.id],
                [self.id, self.language, self.content, self.format_ts(self.edited_at)]]

    @classmethod
    def client_insert_sql(cls):
        return ["INSERT OR IGNORE INTO string_ids (id) VALUES (?)",
                "INSERT OR IGNORE INTO string_content (id, language, content, edited_at) VALUES (?, ?, ?, ?)"]

    @classmethod
    def server_insert_sql(cls):
        return ["INSERT INTO string_ids (id) VALUES (%s) ON CONFLICT (id) DO NOTHING;",
                "INSERT INTO string_content (id, language, content, edited_at) VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING"]

    def server_insert_values(self):
        return [[self.id],
                [self.id, self.language, self.content, self.edited_at]]

    @classmethod
    def db_columns_from_server(cls):
        return [('id', lambda s: s.replace('-', '')),
                ('language', identity),
                ('content', identity),
                ('edited_at', identity)]

    @classmethod
    def db_columns_from_client(cls):
        return [('id', identity),
                ('language', identity),
                ('content', identity),
                ('edited_at', parse_client_timestamp)]

    @classmethod
    def table_name(cls):
        return "string_content"
