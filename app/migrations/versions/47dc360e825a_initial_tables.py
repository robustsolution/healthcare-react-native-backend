from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "47dc360e825a"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        """
    CREATE TABLE string_ids (
      id uuid PRIMARY KEY,
      last_modified timestamp with time zone default now(),
      server_created_at timestamp with time zone default now(),
      deleted_at timestamp with time zone default null
    )
    """
    )

    op.execute(
        """
    CREATE TABLE string_content (
      id uuid REFERENCES string_ids(id) ON DELETE CASCADE,
      language varchar(5),
      content text,
      updated_at timestamp with time zone,
      last_modified timestamp with time zone default now(),
      server_created_at timestamp with time zone default now(),
      deleted_at timestamp with time zone default null
    );
    """
    )

    op.execute(
        """
    CREATE UNIQUE INDEX ON string_content (id, language);
    """
    )

    op.execute(
        """
    CREATE TABLE patients (
      id uuid PRIMARY KEY,
      given_name TEXT,
      surname TEXT,
      date_of_birth DATE,
      country TEXT,
      hometown TEXT,
      phone TEXT,
      sex varchar(8),
      camp varchar(50),
      image_timestamp timestamp with time zone,
      is_deleted boolean default false,
      created_at timestamp with time zone default now(),
      updated_at timestamp with time zone default now(),
      last_modified timestamp with time zone default now(),
      server_created_at timestamp with time zone default now(),
      deleted_at timestamp with time zone default null
    );
    """
    )

    op.execute(
        """
    CREATE TABLE clinics (
      id uuid PRIMARY KEY,
      name TEXT,
      is_deleted boolean default false,
      created_at timestamp with time zone default now(),
      updated_at timestamp with time zone default now(),
      last_modified timestamp with time zone default now(),
      server_created_at timestamp with time zone default now(),
      deleted_at timestamp with time zone default null
    );
    """
    )

    op.execute(
        """
    CREATE TABLE users (
      id uuid PRIMARY KEY,
      name text not null,
      role text not null,
      email text not null,
      hashed_password text not null,
      instance_url text,
      is_deleted boolean default false,
      created_at timestamp with time zone default now(),
      updated_at timestamp with time zone default now(),
      last_modified timestamp with time zone default now(),
      server_created_at timestamp with time zone default now(),
      deleted_at timestamp with time zone default null
    );
    """
    )

    op.execute(
        """
      CREATE UNIQUE INDEX ON users (email);
    """
    )

    op.execute(
        """
    CREATE TABLE tokens (
      user_id uuid REFERENCES users (id),
      token text not null,
      expiry timestamptz not null default now() + INTERVAL '60 minutes'
    );
    """
    )

    op.execute("CREATE INDEX ON tokens (token)")

    op.execute(
        """
    CREATE TABLE visits (
      id uuid PRIMARY KEY,
      patient_id uuid REFERENCES patients(id) ON DELETE CASCADE,
      clinic_id uuid REFERENCES clinics(id) ON DELETE CASCADE,
      provider_id uuid REFERENCES users(id) ON DELETE CASCADE,
      provider_name TEXT,
      check_in_timestamp timestamp with time zone,
      is_deleted boolean default false,
      metadata JSONB NOT NULL DEFAULT '{}',
      created_at timestamp with time zone default now(),
      updated_at timestamp with time zone default now(),
      last_modified timestamp with time zone default now(),
      server_created_at timestamp with time zone default now(),
      deleted_at timestamp with time zone default null
    );
    """
    )

    op.execute(
        """
        CREATE TABLE events (
            id uuid PRIMARY KEY,
            patient_id uuid REFERENCES patients(id) ON DELETE CASCADE,
            visit_id uuid REFERENCES visits(id) ON DELETE CASCADE DEFAULT NULL,
            event_type TEXT,
            event_metadata JSONB NOT NULL DEFAULT '{}',
            is_deleted boolean default false,
            created_at timestamp with time zone default now(),
            updated_at timestamp with time zone default now(),
            last_modified timestamp with time zone default now(),
            server_created_at timestamp with time zone default now(),
            deleted_at timestamp with time zone default null
        );
        """
    )

    op.execute(
        """
        CREATE TABLE event_forms (
            id uuid PRIMARY KEY,
            name TEXT,
            description TEXT,
            metadata JSONB NOT NULL DEFAULT '{}',
            language TEXT NOT NULL DEFAULT 'en',
            is_deleted boolean default false,
            created_at timestamp with time zone default now(),
            updated_at timestamp with time zone default now(),
            last_modified timestamp with time zone default now(),
            server_created_at timestamp with time zone default now(),
            deleted_at timestamp with time zone default null
        );
        """
    )

    op.execute(
        """
    CREATE FUNCTION get_string(uuid, text) RETURNS text 
    AS 'SELECT content FROM string_content WHERE id = $1 AND language = $2;' 
    LANGUAGE SQL IMMUTABLE RETURNS NULL ON NULL INPUT;
    """
    )

    # TODO: Add a trigger to update the last_modified field on the string_ids table
    # REF: https://watermelondb.dev/Advanced/Sync.html#tips-on-implementing-server-side-changes-tracking
    # REF2: https://github.com/Kinto/kinto/blob/814c30c5dd745717b8ea50d708d9163a38d2a9ec/kinto/core/storage/postgresql/schema.sql#L64-L116


def downgrade():
    op.execute("DROP TABLE events;")
    op.execute("DROP TABLE visits;")
    op.execute("DROP TABLE users CASCADE;")
    op.execute("DROP TABLE clinics;")
    op.execute("DROP TABLE patients;")
    op.execute("DROP TABLE string_content;")
    op.execute("DROP TABLE string_ids;")
    op.execute("DROP TABLE event_forms;")
