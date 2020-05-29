"""allow_data_import

Revision ID: cdca5f411be5
Revises: d73af147c118
Create Date: 2020-05-28 15:49:59.224162

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cdca5f411be5'
down_revision = 'd73af147c118'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
    CREATE FUNCTION get_string(uuid, text) RETURNS text 
    AS 'SELECT content FROM string_content WHERE id = $1 AND language = $2;' 
    LANGUAGE SQL IMMUTABLE RETURNS NULL ON NULL INPUT;
    """)


def downgrade():
    op.execute("""DROP FUNCTION get_string;""")
