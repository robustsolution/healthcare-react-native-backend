from dataclasses import dataclass
from client_object import ClientObject
from datetime import datetime
from util import identity

@dataclass
class Visit(ClientObject):
    id: str
    patient_id: str
    clinic_id: str
    provider_id: str
    check_in_timestamp: datetime
    check_out_timestamp: datetime
    edited_at: datetime

    def client_insert_values(self):
        return [self.id,
                self.patient_id,
                self.clinic_id,
                self.provider_id,
                self.format_ts(self.check_in_timestamp),
                self.format_ts(self.check_out_timestamp)]

    @classmethod
    def client_insert_sql(cls):
        return """INSERT INTO visits (id, patient_id, clinic_id, provider_id, check_in_timestamp, check_out_timestamp) VALUES (?, ?, ?, ?, ?, ?)"""

    @classmethod
    def db_columns(cls):
        return [('id', lambda s: s.replace('-', '')),
                ('patient_id', lambda s: s.replace('-', '')),
                ('clinic_id', lambda s: s.replace('-', '')),
                ('provider_id', lambda s: s.replace('-', '')),
                ('check_in_timestamp', identity),
                ('check_out_timestamp', identity)]

    @classmethod
    def table_name(cls):
        return "visits"
