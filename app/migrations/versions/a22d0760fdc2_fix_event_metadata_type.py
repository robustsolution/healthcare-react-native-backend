"""Fix event metadata type

Revision ID: a22d0760fdc2
Revises: 9cfd04c8af71
Create Date: 2020-03-07 20:15:58.426007

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a22d0760fdc2'
down_revision = '9cfd04c8af71'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("ALTER TABLE events DROP COLUMN event_metadata;")
    op.execute("ALTER TABLE events ADD COLUMN event_metadata JSONB NOT NULL DEFAULT '{}';")


def downgrade():
    op.execute("ALTER TABLE events DROP COLUMN event_metadata;")
    op.execute("ALTER TABLE events ADD COLUMN event_metadata timestamp with time zone;")

