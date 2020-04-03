"""make_user_email_unique

Revision ID: 4d19d1f9140f
Revises: e1dd215005de
Create Date: 2020-04-02 16:15:00.994025

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4d19d1f9140f'
down_revision = 'e1dd215005de'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("CREATE UNIQUE INDEX ON users (email);")


def downgrade():
    op.execute("DROP INDEX users_email_idx;")
