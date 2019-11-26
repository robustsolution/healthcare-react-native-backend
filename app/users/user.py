from users.data_access import user_data_by_email
from web_errors import WebError

import bcrypt


class User:
    def __init__(self, id, name, role, email, hashed_password):
        self.id = id
        self.name = name
        self.role = role
        self.email = email
        self.hashed_password = hashed_password

    @classmethod
    def authenticate(cls, email, password):
        user = cls.from_db_row(user_data_by_email(email))
        if not bcrypt.checkpw(password.encode(), user.hashed_password):
            raise WebError("password incorrect", status_code=401)
        else:
            return user

    @classmethod
    def from_db_row(cls, db_row):
        id, name, role, email, hashed_password = db_row
        return cls(id, name, role, email, hashed_password.encode())

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'role': self.role,
            'email': self.email,
        }