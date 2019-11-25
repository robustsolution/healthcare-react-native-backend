"""Initial Tables

Revision ID: 47dc360e825a
Revises:
Create Date: 2019-07-28 21:03:19.737020

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '47dc360e825a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    raise NotImplementedError('Please implement first migration.')

    # op.execute("""
    #     CREATE TABLE foo (bar text);
    #     """)


def downgrade():
    raise NotImplementedError('Please implement first migration.')

    # op.execute("""
    #     DROP TABLE foo;
    #     """)
