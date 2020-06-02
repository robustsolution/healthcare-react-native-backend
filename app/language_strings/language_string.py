from language_strings.data_access import language_string_data_by_id
from web_errors import WebError
from typing import Dict, Optional


class LanguageString:
    def __init__(self, id: str, content_by_language: Dict[str, str]):
        self.id = id
        self.content_by_language = content_by_language

    @classmethod
    def from_id(cls, id):
        if id is None:
            return None
        data = {language: content
                for language, content in language_string_data_by_id(id)}
        if not len(data):
            raise WebError(f"string id '{id}' not found.", 404)
        return cls(id, data)

    def to_dict(self):
        return {
            'id': self.id.replace('-', ''),
            'content': self.content_by_language,
        }

    def get(self, language_code):
        if language_code in self.content_by_language:
            return self.content_by_language[language_code]
        else:
            for _, content in self.content_by_language.items():
                return content


def to_id(language_string: Optional[LanguageString]):
    if language_string is None:
        return None
    else:
        return language_string.id