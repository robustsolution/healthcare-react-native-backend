"""add edited_at to events

Revision ID: 43531bcf6e4a
Revises: a22d0760fdc2
Create Date: 2020-03-07 20:48:40.952904

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '43531bcf6e4a'
down_revision = 'a22d0760fdc2'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("ALTER TABLE events ADD COLUMN edited_at timestamp with time zone")


def downgrade():
    op.execute("ALTER TABLE events DROP COLUMN edited_at")
