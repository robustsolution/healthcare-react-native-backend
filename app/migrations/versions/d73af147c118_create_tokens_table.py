"""create_tokens_table

Revision ID: d73af147c118
Revises: fc3a6a2ca002
Create Date: 2020-04-29 11:05:20.619408

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd73af147c118'
down_revision = 'fc3a6a2ca002'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
    CREATE TABLE tokens (
      user_id uuid REFERENCES users (id),
      token text not null,
      expiry timestamptz not null default now() + INTERVAL '60 minutes'
    );
    """)

    op.execute('CREATE INDEX ON tokens (token)')

def downgrade():
    pass
