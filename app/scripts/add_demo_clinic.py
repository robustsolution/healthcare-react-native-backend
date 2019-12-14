from clinics.clinic import Clinic
from clinics.data_access import add_clinic
from language_strings.language_string import LanguageString

import uuid


clinic = Clinic(id=str(uuid.uuid4()), name=LanguageString(
    id=str(uuid.uuid4()), content_by_language={
        'en': 'EMA'
    }))

add_clinic(clinic)