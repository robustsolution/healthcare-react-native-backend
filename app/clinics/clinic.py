from dataclasses import dataclass
from language_strings.language_string import LanguageString

@dataclass
class Clinic:
    id: str
    name: LanguageString
