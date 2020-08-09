"""allow_visit_delete

Revision ID: e778cb1d223e
Revises: cdca5f411be5
Create Date: 2020-08-09 15:54:00.554946

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e778cb1d223e'
down_revision = 'cdca5f411be5'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
    ALTER TABLE VISITS ADD COLUMN deleted boolean default false
    """)


def downgrade():
    op.execute("""
        ALTER TABLE VISITS DROP COLUMN deleted
        """)

