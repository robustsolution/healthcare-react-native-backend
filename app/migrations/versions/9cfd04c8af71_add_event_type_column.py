"""add_event_type_column

Revision ID: 9cfd04c8af71
Revises: 4817070bc1ac
Create Date: 2020-01-14 10:21:05.999520

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9cfd04c8af71'
down_revision = '4817070bc1ac'
branch_labels = None
depends_on = None


def upgrade():
    op.execute('ALTER TABLE events ADD COLUMN event_type TEXT;')


def downgrade():
    op.execute('ALTER TABLE events DROP COLUMN event_type;')
