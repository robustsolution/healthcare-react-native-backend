from patients.patient import Patient
from patients.data_access import add_patient
from language_strings.language_string import LanguageString

import uuid
from datetime import datetime, date

for given_name, surname, sex in [
    ['Ahmad', 'Muhammad', 'M'],
    ['Yousef', 'Adam', 'M'],
    ['Salman', 'Mahmoud', 'M'],
    ['Zaynab', 'Ali', 'F'],
    ['Ayesha', 'Noor', 'F'],
    ['Laylah', 'Saleh', 'F']]:
    given_name_ls = LanguageString(id=str(uuid.uuid4()), content_by_language={'en': given_name})
    surname_ls = LanguageString(id=str(uuid.uuid4()), content_by_language={'en': surname})
    patient = Patient(
        id=str(uuid.uuid4()),
        edited_at=datetime.now(),
        given_name=given_name_ls,
        surname=surname_ls,
        date_of_birth=date(2000, 10, 31),
        sex=sex,
        country=LanguageString(id=str(uuid.uuid4()), content_by_language={'en': 'Syria'}),
        hometown=LanguageString(id=str(uuid.uuid4()), content_by_language={'en': 'Damascus'}),
        phone=None
    )
    add_patient(patient)
