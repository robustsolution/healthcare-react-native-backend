from dataclasses import dataclass
from client_object import ClientObject
from datetime import datetime
from typing import Dict
from util import identity

@dataclass
class Event(ClientObject):
    id: str
    patient_id: str
    visit_id: str
    event_type: str
    event_timestamp: datetime
    event_metadata: Dict
    edited_at: datetime

    def client_insert_values(self):
        return [self.id,
                self.patient_id,
                self.visit_id,
                self.event_type,
                self.format_ts(self.event_timestamp),
                self.format_json(self.event_metadata),
                self.format_ts(self.edited_at)]

    @classmethod
    def client_insert_sql(cls):
        return """INSERT INTO events (id, patient_id, visit_id, event_type, event_timestamp, event_metadata, edited_at) VALUES (?, ?, ?, ?, ?, ?, ?)"""

    @classmethod
    def db_columns(cls):
        return [('id', lambda s: s.replace('-', '')),
                ('patient_id', lambda s: s.replace('-', '')),
                ('visit_id', lambda s: s.replace('-', '')),
                ('event_type', identity),
                ('event_timestamp', identity),
                ('event_metadata', identity),
                ('edited_at', identity),]

    @classmethod
    def table_name(cls):
        return "events"
