from werkzeug.datastructures import FileStorage
from tempfile import NamedTemporaryFile
from openpyxl import load_workbook
from web_errors import WebError
from dataclasses import dataclass
from datetime import datetime
from typing import Iterable
from patients.data_access import patient_exists, add_patient
from patients.patient import Patient
import uuid
from language_strings.language_string import LanguageString
from datetime import date, timedelta
import itertools


@dataclass
class PatientDataRow:
    camp: str
    visit_data: datetime
    ema_number: int
    first_name: str
    surname: str
    age: str
    gender: str
    home_country: str
    allergies: str
    medical_hx: str
    chronic_condition: str
    current_medication_1: str
    current_medication_2: str
    current_medication_3: str
    current_medication_4: str
    current_medication_5: str
    current_medication_6: str
    presenting_complaint: str
    heart_rate: float
    blood_pressure: str
    o2_sats: float
    respiratory_rate: float
    temperature: float
    bg: float
    examination: str
    diagnosis: str
    treatment: str
    dispensed_medicine_1: str
    dispensed_medicine_quantity_1: str
    dispensed_medicine_2: str
    dispensed_medicine_quantity_2: str
    dispensed_medicine_3: str
    dispensed_medicine_quantity_3: str
    dispensed_medicine_4: str
    dispensed_medicine_quantity_4: str
    prescription: str
    follow_up: str
    referral: str
    seen_by: str
    fee: str
    notes: str


COLUMNS = ['camp', 'visit_data', 'ema_number', 'first_name', 'surname', 'age', 'gender', 'home_country', 'allergies',
           'medical_hx', 'chronic_condition', 'current_medication_1', 'current_medication_2', 'current_medication_3',
           'current_medication_4', 'current_medication_5', 'current_medication_6', 'presenting_complaint', 'heart_rate',
           'blood_pressure', 'o2_sats', 'respiratory_rate', 'temperature', 'bg', 'examination', 'diagnosis',
           'treatment', 'dispensed_medicine_1', 'dispensed_medicine_quantity_1', 'dispensed_medicine_2',
           'dispensed_medicine_quantity_2', 'dispensed_medicine_3', 'dispensed_medicine_quantity_3',
           'dispensed_medicine_4', 'dispensed_medicine_quantity_4', 'prescription', 'follow_up', 'referral', 'seen_by',
           'fee', 'notes']

COLUMN_TYPES = [str, None, int, str, str, str, str, str, str, str, str, str, str, str, str, str, str, str, float, str,
                float, float, float, float, str, str, str, str, str, str, str, str, str, str, str, str, str, str, str,
                str, str]


class PatientDataImporter:
    def __init__(self, data_file: FileStorage):
        self.data_filename = self._write_file_to_tempfile(data_file)

    def run(self):
        all_rows = [self._parse_row(row) for row in self.iter_data_rows()]
        self._create_patients(all_rows)

    def _parse_row(self, row):
        if len(row) != 41:
            raise WebError('All data rows must have exactly 41 data points.', 400)
        values = [self._parse_cell(value, formatter) for value, formatter in zip(row, COLUMN_TYPES)]
        return PatientDataRow(**dict(zip(COLUMNS, values)))

    def _parse_cell(self, cell, formatter):
        if cell == 'Nil' or cell is None:
            return None
        if formatter is None:
            return cell
        return formatter(cell)

    @staticmethod
    def _write_file_to_tempfile(data_file: FileStorage):
        handle = NamedTemporaryFile('wb', delete=False, suffix='.xlsx')
        data_file.save(handle)
        handle.close()
        return handle.name

    def iter_data_rows(self):
        wb = load_workbook(self.data_filename)
        ws = wb.active
        for idx, row in enumerate(ws.iter_rows(min_row=3, max_col=41, values_only=True)):
            if all(x is None for x in row):
                continue
            yield row

    def _create_patients(self, rows: Iterable[PatientDataRow]):
        for patient_data in set(map(lambda r: (r.first_name, r.surname, r.gender, r.home_country, r.age), rows)):
            first_name, surname, gender, home_country, age = patient_data
            if not patient_exists(first_name, surname, home_country, gender):
                self._create_patient(first_name, surname, home_country, gender, age)

    def _create_patient(self, given_name, surname, home_country, sex, age):
        given_name_ls = LanguageString(id=str(uuid.uuid4()), content_by_language={'en': given_name})
        surname_ls = LanguageString(id=str(uuid.uuid4()), content_by_language={'en': surname})
        inferred_dob = self._infer_dob(age)
        patient = Patient(
            id=str(uuid.uuid4()),
            edited_at=datetime.now(),
            given_name=given_name_ls,
            surname=surname_ls,
            date_of_birth=inferred_dob,
            sex=sex,
            country=LanguageString(id=str(uuid.uuid4()), content_by_language={'en': home_country}),
            phone=None,
            hometown=None
        )
        add_patient(patient)

    def _infer_dob(self, age_string):
        try:
            int_prefix = int(''.join(itertools.takewhile(str.isnumeric, age_string)))
            today = date.today()
            if 'months' in age_string:
                return today - timedelta(days=30 * int_prefix)
            elif 'weeks' in age_string:
                return today - timedelta(weeks=int_prefix)
            elif 'days' in age_string:
                return today - timedelta(days=int_prefix)
            else:
                # Assume years if no unit is specified
                return today - timedelta(days=365 * int_prefix)
        except ValueError:
            raise WebError('Unparseable age string: ' + age_string, 400)
