"""add_patient_sex_and_phone

Revision ID: 4817070bc1ac
Revises: 9ba22457d34a
Create Date: 2019-12-17 13:28:49.810356

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4817070bc1ac'
down_revision = '9ba22457d34a'
branch_labels = None
depends_on = None


def upgrade():
    op.execute('ALTER TABLE patients ADD COLUMN sex varchar(1)')
    op.execute('ALTER TABLE patients ADD COLUMN phone text')


def downgrade():
    op.execute('ALTER TABLE patients DROP COLUMN sex')
    op.execute('ALTER TABLE patients DROP COLUMN phone')
