from dataclasses import dataclass
from client_object import ClientObject
from datetime import datetime
from util import identity


@dataclass
class IndividualLanguageString(ClientObject):
    id: str
    language: str
    content: str
    edited_at: datetime

    def client_insert_values(self):
        return [[self.id],
                [self.id, self.language, self.content, self.edited_at.isoformat()]]

    @classmethod
    def client_insert_sql(cls):
        return ["INSERT OR IGNORE INTO string_ids (id) VALUES (?)",
                "INSERT INTO string_content (id, language, content, edited_at) VALUES (?, ?, ?, ?)"]

    @classmethod
    def db_columns(cls):
        return [('id', identity),
                ('language', identity),
                ('content', identity),
                ('edited_at', identity)]

    @classmethod
    def table_name(cls):
        return "string_content"

