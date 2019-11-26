"""Create initial user

Revision ID: 657ba64ed784
Revises: 47dc360e825a
Create Date: 2019-11-25 18:33:30.688004

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime
import uuid


# revision identifiers, used by Alembic.
revision = '657ba64ed784'
down_revision = '47dc360e825a'
branch_labels = None
depends_on = None


def upgrade():
    user_name_id = str(uuid.uuid4())
    op.execute(f"INSERT INTO string_ids (id) VALUES ('{user_name_id}')")
    op.execute(f"""
    INSERT INTO string_content (id, language, content, edited_at) 
    VALUES ('{user_name_id}', 'en', 'Sam Brotherton', '{datetime.now().isoformat()}')
    """)
    op.execute(f"""
    INSERT INTO users (id, name, role, email, hashed_password, edited_at) 
    VALUES ('{str(uuid.uuid4())}', '{user_name_id}', 'super_admin', 'sam@hikmahealth.org', '$2b$12$VaVVnY5MtFLFE5KjNu.aMekKC2OyKet3i1v1pU3fbZOBsaA43hASy', '{datetime.now().isoformat()}')
    """)


def downgrade():
    op.execute("DELETE FROM users WHERE email = 'sam@hikmahealth.org';")
