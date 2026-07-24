import os
import sqlite3

try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
    HAS_POSTGRES = True
except ImportError:
    HAS_POSTGRES = False

# Config environment variables
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_NAME = os.environ.get("DB_NAME", "vitalsync")
DB_USER = os.environ.get("DB_USER", "postgres")
DB_PASS = os.environ.get("DB_PASS", "postgres")
DB_PORT = os.environ.get("DB_PORT", "5432")

USE_POSTGRES = os.environ.get("USE_POSTGRES", "false").lower() == "true"


def get_connection():
    """
    Establish DB connection. Connects to ShaktiDB (PostgreSQL) if USE_POSTGRES is true,
    otherwise falls back to a local SQLite database for easy development/testing.
    """
    if USE_POSTGRES and HAS_POSTGRES:
        try:
            conn = psycopg2.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASS,
                port=int(DB_PORT)
            )
            return conn
        except Exception as e:
            print(f"Failed to connect to ShaktiDB/PostgreSQL: {e}. Falling back to SQLite3.")

    # Fallback SQLite Database file in workspace
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'vitalsync.db')
    conn = sqlite3.connect(db_path)
    # Ensure foreign key constraints are enforced in SQLite
    try:
        conn.execute('PRAGMA foreign_keys = ON')
    except Exception:
        pass
    # Configure SQLite to behave like a dict cursor
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """
    Reads schema.sql and initializes tables.

    For SQLite we remove the existing DB file to ensure a fresh database for
    tests and development runs. For Postgres (ShaktiDB) we execute each SQL
    statement in the schema file sequentially because psycopg2 does not
    support executescript.
    """
    schema_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'schema.sql')
    with open(schema_path, 'r') as f:
        schema_sql = f.read()

    if USE_POSTGRES and HAS_POSTGRES:
        conn = get_connection()
        cursor = conn.cursor()
        # Split on semicolons and execute statements individually to support
        # multi-statement schema files when using psycopg2.
        statements = [s.strip() for s in schema_sql.split(';') if s.strip()]
        for stmt in statements:
            try:
                cursor.execute(stmt + ';')
            except Exception as e:
                # Print and continue; surface errors for debugging.
                print(f"Schema statement failed: {e}\nStatement: {stmt}")
        conn.commit()
        cursor.close()
        conn.close()
    else:
        # Ensure a clean SQLite database file so tests don't hit UNIQUE constraints
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'vitalsync.db')
        try:
            if os.path.exists(db_path):
                os.remove(db_path)
        except Exception:
            pass

        conn = sqlite3.connect(db_path)
        # Enable foreign key support so ON DELETE CASCADE works as intended
        try:
            conn.execute('PRAGMA foreign_keys = ON')
        except Exception:
            pass
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.executescript(schema_sql)
        conn.commit()
        cursor.close()
        conn.close()

    print("Database initialized successfully.")
