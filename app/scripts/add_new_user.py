from users.user import User
from users.data_access import add_user
from language_strings.language_string import LanguageString

import uuid
import sys
import bcrypt

name = sys.argv[1]
email_address = sys.argv[2]
password = sys.argv[3]
role = 'super_admin'
id = str(uuid.uuid4())
name_str = LanguageString(id=str(uuid.uuid4()), content_by_language={'en': name})
hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

user = User(id, name_str, role, email_address, hashed_password)
add_user(user)