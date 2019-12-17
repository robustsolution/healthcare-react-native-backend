"""update_patient_hometown

Revision ID: 9ba22457d34a
Revises: 657ba64ed784
Create Date: 2019-12-17 12:00:02.587492

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9ba22457d34a'
down_revision = '657ba64ed784'
branch_labels = None
depends_on = None


def upgrade():
    op.execute('ALTER TABLE patients DROP COLUMN place_of_birth')
    op.execute('ALTER TABLE patients ADD COLUMN country uuid REFERENCES string_ids(id) ON DELETE CASCADE')
    op.execute('ALTER TABLE patients ADD COLUMN hometown uuid REFERENCES string_ids(id) ON DELETE CASCADE')


def downgrade():
    op.execute('ALTER TABLE patients ADD COLUMN place_of_birth uuid REFERENCES string_ids(id) ON DELETE CASCADE')
    op.execute('ALTER TABLE patients DROP COLUMN country')
    op.execute('ALTER TABLE patients DROP COLUMN hometown')

