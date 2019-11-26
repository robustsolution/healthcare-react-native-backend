from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '47dc360e825a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
    CREATE TABLE string_ids (
      id uuid PRIMARY KEY
    )
    """)

    op.execute("""
    CREATE TABLE string_content (
      id uuid REFERENCES string_ids(id) ON DELETE CASCADE,
      language varchar(5),
      content text,
      edited_at timestamp with time zone
    );
    """)

    op.execute("""
    CREATE UNIQUE INDEX ON string_content (id, language);
    """)

    op.execute("""
    CREATE TABLE patients (
      id uuid PRIMARY KEY,
      given_name uuid REFERENCES string_ids(id) ON DELETE CASCADE,
      surname uuid REFERENCES string_ids(id) ON DELETE CASCADE,
      date_of_birth DATE,
      place_of_birth uuid REFERENCES string_ids(id) ON DELETE CASCADE,
      edited_at timestamp with time zone
    );
    """)

    op.execute("""
    CREATE TABLE clinics (
      id uuid PRIMARY KEY,
      name uuid REFERENCES string_ids(id) ON DELETE CASCADE,
      edited_at timestamp with time zone
    );
    """)

    op.execute("""
    CREATE TABLE users (
      id uuid PRIMARY KEY,
      name uuid REFERENCES string_ids(id) ON DELETE CASCADE,
      role text,
      edited_at timestamp with time zone
    );
    """)

    op.execute("""
    CREATE TABLE visits (
      id uuid PRIMARY KEY,
      patient_id uuid REFERENCES patients(id) ON DELETE CASCADE,
      clinic_id uuid REFERENCES clinics(id) ON DELETE CASCADE,
      provider_id uuid REFERENCES users(id) ON DELETE CASCADE,
      check_in_timestamp timestamp with time zone,
      check_out_timestamp timestamp with time zone,
      edited_at timestamp with time zone
    );
    """)

    op.execute("""
    CREATE TABLE events (
      id uuid PRIMARY KEY,
      patient_id uuid REFERENCES patients(id) ON DELETE CASCADE,
      visit_id uuid REFERENCES visits(id) ON DELETE CASCADE,
      event_timestamp timestamp with time zone,
      event_metadata timestamp with time zone
    );
    """)


def downgrade():
    op.execute("DROP TABLE events;")
    op.execute("DROP TABLE visits;")
    op.execute("DROP TABLE users;")
    op.execute("DROP TABLE clinics;")
    op.execute("DROP TABLE patients;")
    op.execute("DROP TABLE string_content;")
    op.execute("DROP TABLE string_ids;")


