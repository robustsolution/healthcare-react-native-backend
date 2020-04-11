"""make_event_metadata_text

Revision ID: fc3a6a2ca002
Revises: 628a38e43688
Create Date: 2020-04-11 08:10:58.332881

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fc3a6a2ca002'
down_revision = '628a38e43688'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("DELETE FROM events;")
    op.execute("ALTER TABLE events DROP COLUMN event_metadata;")
    op.execute("ALTER TABLE events ADD COLUMN event_metadata TEXT;")


def downgrade():
    op.execute("DELETE FROM events;")
    op.execute("ALTER TABLE events DROP COLUMN event_metadata;")
    op.execute("ALTER TABLE events ADD COLUMN event_metadata JSONB NOT NULL DEFAULT '{}';")