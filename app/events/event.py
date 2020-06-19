from dataclasses import dataclass
from client_object import ClientObject
from datetime import datetime
from typing import Dict
from util import identity, parse_client_timestamp, parse_server_uuid

@dataclass
class Event(ClientObject):
    id: str
    patient_id: str
    visit_id: str
    event_type: str
    event_timestamp: datetime
    event_metadata: str
    edited_at: datetime

    def client_insert_values(self):
        return [self.id,
                self.patient_id,
                self.visit_id,
                self.event_type,
                self.format_ts(self.event_timestamp),
                self.event_metadata,
                self.format_ts(self.edited_at)]

    @classmethod
    def client_insert_sql(cls):
        return """INSERT INTO events (id, patient_id, visit_id, event_type, event_timestamp, event_metadata, edited_at) VALUES (?, ?, ?, ?, ?, ?, ?)"""

    def server_insert_values(self):
        return [self.id,
                self.patient_id,
                self.visit_id,
                self.event_type,
                self.event_timestamp,
                self.event_metadata,
                self.edited_at]

    @classmethod
    def server_insert_sql(cls):
        return """INSERT INTO events (id, patient_id, visit_id, event_type, event_timestamp, event_metadata, edited_at) VALUES (%s, %s, %s, %s, %s, %s, %s)"""

    @classmethod
    def db_columns_from_server(cls):
        return [('id', lambda s: s.replace('-', '')),
                ('patient_id', parse_server_uuid),
                ('visit_id', parse_server_uuid),
                ('event_type', identity),
                ('event_timestamp', identity),
                ('event_metadata', identity),
                ('edited_at', identity),]

    @classmethod
    def db_columns_from_client(cls):
        return [('id', identity),
                ('patient_id', identity),
                ('visit_id', identity),
                ('event_type', identity),
                ('event_timestamp', parse_client_timestamp),
                ('event_metadata', identity),
                ('edited_at', parse_client_timestamp)]

    @classmethod
    def table_name(cls):
        return "events"
