from dataclasses import dataclass
from language_strings.language_string import LanguageString
from client_object import ClientObject
from datetime import datetime, date
from util import identity, parse_client_date, parse_client_timestamp


@dataclass
class Patient(ClientObject):
    id: str
    given_name: LanguageString
    surname: LanguageString
    date_of_birth: date
    sex: str
    country: LanguageString
    hometown: LanguageString
    phone: str
    edited_at: datetime

    def client_insert_values(self):
        return [self.id,
                self.format_string(self.given_name),
                self.format_string(self.surname),
                self.format_date(self.date_of_birth),
                self.sex,
                self.format_string(self.country),
                self.format_string(self.hometown),
                self.phone,
                self.format_ts(self.edited_at)]

    @classmethod
    def client_insert_sql(cls):
        return """INSERT INTO patients (id, given_name, surname, date_of_birth, sex, country, hometown, phone, edited_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"""

    def server_insert_values(self):
        return [self.id,
                self.format_string(self.given_name),
                self.format_string(self.surname),
                self.date_of_birth,
                self.sex,
                self.format_string(self.country),
                self.format_string(self.hometown),
                self.phone,
                self.edited_at]

    @classmethod
    def server_insert_sql(cls):
        return """INSERT INTO patients (id, given_name, surname, date_of_birth, sex, country, hometown, phone, edited_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""

    @classmethod
    def db_columns_from_server(cls):
        return [('id', lambda s: s.replace('-', '')),
                ('given_name', cls.make_language_string),
                ('surname', cls.make_language_string),
                ('date_of_birth', identity),
                ('sex', identity),
                ('country', cls.make_language_string),
                ('hometown', cls.make_language_string),
                ('phone', identity),
                ('edited_at', identity)]

    @classmethod
    def db_columns_from_client(cls):
        return [('id', identity),
                ('given_name', cls.make_language_string),
                ('surname', cls.make_language_string),
                ('date_of_birth', parse_client_date),
                ('sex', identity),
                ('country', cls.make_language_string),
                ('hometown', cls.make_language_string),
                ('phone', identity),
                ('edited_at', parse_client_timestamp)]

    @classmethod
    def table_name(cls):
        return "patients"
