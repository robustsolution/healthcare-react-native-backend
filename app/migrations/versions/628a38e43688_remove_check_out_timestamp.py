"""remove_check_out_timestamp

Revision ID: 628a38e43688
Revises: 4d19d1f9140f
Create Date: 2020-04-09 23:17:09.960506

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '628a38e43688'
down_revision = '4d19d1f9140f'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("ALTER TABLE visits DROP COLUMN check_out_timestamp")


def downgrade():
    op.execute("ALTER TABLE visits ADD COLUMN check_out_timestamp timestamp with time zone")
