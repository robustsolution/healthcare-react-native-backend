"""add_photos_table

Revision ID: e1dd215005de
Revises: 43531bcf6e4a
Create Date: 2020-04-02 15:54:20.210515

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e1dd215005de'
down_revision = '43531bcf6e4a'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
    CREATE TABLE photos (
      patient_id uuid,
      filename text
    )
    """)

    op.execute("""
    CREATE UNIQUE INDEX ON photos (patient_id);    
    """)

def downgrade():
    op.execute("DROP TABLE photos;")
