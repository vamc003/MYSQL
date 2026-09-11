"""
Project Astra - MySQL Database Source Extractor

Purpose:
    Connect to a MySQL database and extract database objects into the
    repository structure:

    database/EMPLOYEE/
        tables/
        views/
        procedures/
        functions/
        triggers/
        events/

The database name is read from .env. The EMPLOYEE folder is used as the
repository folder name by default; change REPOSITORY_DATABASE_FOLDER if
needed.

Required packages:
    mysql-connector-python
    python-dotenv
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

import mysql.connector
from dotenv import load_dotenv


# ---------------------------------------------------------------------------
# Project paths
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATABASE_ROOT = PROJECT_ROOT / "database"

# Repository folder used for the extracted database.
# Change this if your MySQL database name is different.
REPOSITORY_DATABASE_FOLDER = "EMPLOYEE"

OUTPUT_ROOT = DATABASE_ROOT / REPOSITORY_DATABASE_FOLDER


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

ENV_FILE = PROJECT_ROOT / ".env"
load_dotenv(ENV_FILE)


def get_config() -> dict:
    """Read MySQL connection settings from .env."""

    required = {
        "host": os.getenv("MYSQL_HOST"),
        "user": os.getenv("MYSQL_USER"),
        "password": os.getenv("MYSQL_PASSWORD"),
        "database": os.getenv("MYSQL_DATABASE"),
    }

    missing = [key for key, value in required.items() if value is None]

    if missing:
        raise ValueError(
            "Missing required .env settings: "
            + ", ".join(missing)
        )

    return {
        "host": required["host"],
        "port": int(os.getenv("MYSQL_PORT", "3306")),
        "user": required["user"],
        "password": required["password"],
        "database": required["database"],
    }


# ---------------------------------------------------------------------------
# Utility functions
# ---------------------------------------------------------------------------

def safe_filename(name: str) -> str:
    """Convert a MySQL object name into a safe Windows filename."""

    return re.sub(r'[<>:"/\\|?*]', "_", name)


def ensure_output_directories() -> None:
    """Create the object directories if they do not already exist."""

    for folder in (
        "tables",
        "views",
        "procedures",
        "functions",
        "triggers",
        "events",
    ):
        (OUTPUT_ROOT / folder).mkdir(parents=True, exist_ok=True)


def write_text(path: Path, content: str) -> None:
    """Write UTF-8 text with a consistent newline at the end."""

    path.parent.mkdir(parents=True, exist_ok=True)

    if not content.endswith("\n"):
        content += "\n"

    path.write_text(content, encoding="utf-8")


def quote_identifier(name: str) -> str:
    """Quote a MySQL identifier safely using backticks."""

    return "`" + name.replace("`", "``") + "`"


def yaml_value(value) -> str:
    """Represent a simple scalar safely in YAML."""

    if value is None:
        return "null"

    text = str(value)

    # Quote values that could be interpreted as YAML types or contain
    # characters that make an unquoted scalar unsafe.
    if (
        text == ""
        or text.lower() in {"null", "true", "false", "yes", "no"}
        or re.search(r"[:#{}\[\],&*!|>'\"%@`]", text)
        or text != text.strip()
    ):
        escaped = text.replace("\\", "\\\\").replace('"', '\\"')
        return f'"{escaped}"'

    return text


# ---------------------------------------------------------------------------
# Connection
# ---------------------------------------------------------------------------

def connect_to_mysql():
    """Create and return a MySQL connection."""

    config = get_config()

    print("Connecting to MySQL...")
    print(f"Host     : {config['host']}")
    print(f"Port     : {config['port']}")
    print(f"Database : {config['database']}")

    connection = mysql.connector.connect(**config)

    if not connection.is_connected():
        raise ConnectionError("MySQL connection was not established.")

    print("Connection successful.")
    return connection


# ---------------------------------------------------------------------------
# Tables
# ---------------------------------------------------------------------------

def get_tables(cursor) -> list[str]:
    """Return base table names from the configured database."""

    cursor.execute(
        """
        SELECT TABLE_NAME
        FROM information_schema.TABLES
        WHERE TABLE_SCHEMA = %s
          AND TABLE_TYPE = 'BASE TABLE'
        ORDER BY TABLE_NAME
        """,
        (os.getenv("MYSQL_DATABASE"),),
    )

    return [row[0] for row in cursor.fetchall()]


def extract_table(cursor, table_name: str) -> None:
    """Extract CREATE TABLE and column metadata."""

    db = os.getenv("MYSQL_DATABASE")

    cursor.execute(f"SHOW CREATE TABLE {quote_identifier(table_name)}")
    row = cursor.fetchone()

    # SHOW CREATE TABLE normally returns:
    # (TableName, CreateTable)
    create_sql = row[1]

    table_dir = OUTPUT_ROOT / "tables"
    sql_path = table_dir / f"{safe_filename(table_name)}.sql"
    metadata_path = table_dir / f"{safe_filename(table_name)}_metadata.yml"

    write_text(sql_path, create_sql.rstrip() + ";")

    cursor.execute(
        """
        SELECT
            COLUMN_NAME,
            COLUMN_TYPE,
            IS_NULLABLE,
            COLUMN_DEFAULT,
            COLUMN_KEY,
            EXTRA,
            COLUMN_COMMENT
        FROM information_schema.COLUMNS
        WHERE TABLE_SCHEMA = %s
          AND TABLE_NAME = %s
        ORDER BY ORDINAL_POSITION
        """,
        (db, table_name),
    )

    columns = cursor.fetchall()

    cursor.execute(
        """
        SELECT TABLE_COMMENT
        FROM information_schema.TABLES
        WHERE TABLE_SCHEMA = %s
          AND TABLE_NAME = %s
        """,
        (db, table_name),
    )

    table_comment_row = cursor.fetchone()
    table_comment = table_comment_row[0] if table_comment_row else ""

    lines = [
        f"table: {yaml_value(table_name)}",
        f"description: {yaml_value(table_comment)}",
        "columns:",
    ]

    for (
        column_name,
        column_type,
        nullable,
        default_value,
        column_key,
        extra,
        column_comment,
    ) in columns:
        lines.extend(
            [
                f"  - name: {yaml_value(column_name)}",
                f"    type: {yaml_value(column_type)}",
                f"    nullable: {yaml_value(nullable)}",
                f"    default: {yaml_value(default_value)}",
                f"    key: {yaml_value(column_key)}",
                f"    extra: {yaml_value(extra)}",
                f"    description: {yaml_value(column_comment)}",
            ]
        )

    write_text(metadata_path, "\n".join(lines))

    print(f"  [TABLE]     {table_name}")


# ---------------------------------------------------------------------------
# Views
# ---------------------------------------------------------------------------

def get_views(cursor) -> list[str]:
    """Return view names."""

    cursor.execute(
        """
        SELECT TABLE_NAME
        FROM information_schema.VIEWS
        WHERE TABLE_SCHEMA = %s
        ORDER BY TABLE_NAME
        """,
        (os.getenv("MYSQL_DATABASE"),),
    )

    return [row[0] for row in cursor.fetchall()]


def extract_view(cursor, view_name: str) -> None:
    """Extract CREATE VIEW."""

    cursor.execute(f"SHOW CREATE VIEW {quote_identifier(view_name)}")
    row = cursor.fetchone()

    create_sql = row[1]

    path = OUTPUT_ROOT / "views" / f"{safe_filename(view_name)}.sql"
    write_text(path, create_sql.rstrip() + ";")

    print(f"  [VIEW]      {view_name}")


# ---------------------------------------------------------------------------
# Procedures and Functions
# ---------------------------------------------------------------------------

def get_routines(cursor, routine_type: str) -> list[str]:
    """Return stored procedure/function names."""

    cursor.execute(
        """
        SELECT ROUTINE_NAME
        FROM information_schema.ROUTINES
        WHERE ROUTINE_SCHEMA = %s
          AND ROUTINE_TYPE = %s
        ORDER BY ROUTINE_NAME
        """,
        (os.getenv("MYSQL_DATABASE"), routine_type),
    )

    return [row[0] for row in cursor.fetchall()]


def extract_routine(cursor, routine_name: str, routine_type: str) -> None:
    """Extract a stored procedure or function definition."""

    object_type = routine_type.upper()

    if object_type == "PROCEDURE":
        cursor.execute(
            f"SHOW CREATE PROCEDURE {quote_identifier(routine_name)}"
        )
        path = OUTPUT_ROOT / "procedures" / f"{safe_filename(routine_name)}.sql"
    else:
        cursor.execute(
            f"SHOW CREATE FUNCTION {quote_identifier(routine_name)}"
        )
        path = OUTPUT_ROOT / "functions" / f"{safe_filename(routine_name)}.sql"

    row = cursor.fetchone()

    # For MySQL, SHOW CREATE PROCEDURE/FUNCTION returns the object name,
    # SQL mode, and Create Procedure/Create Function definition.
    create_sql = row[2]

    write_text(path, create_sql.rstrip())

    print(f"  [{object_type:<10}] {routine_name}")


# ---------------------------------------------------------------------------
# Triggers
# ---------------------------------------------------------------------------

def get_triggers(cursor) -> list[str]:
    """Return trigger names."""

    cursor.execute(
        """
        SELECT TRIGGER_NAME
        FROM information_schema.TRIGGERS
        WHERE TRIGGER_SCHEMA = %s
        ORDER BY TRIGGER_NAME
        """,
        (os.getenv("MYSQL_DATABASE"),),
    )

    return [row[0] for row in cursor.fetchall()]


def extract_trigger(cursor, trigger_name: str) -> None:
    """Extract CREATE TRIGGER."""

    cursor.execute(f"SHOW CREATE TRIGGER {quote_identifier(trigger_name)}")
    row = cursor.fetchone()

    # SHOW CREATE TRIGGER returns:
    # Trigger, sql_mode, SQL Original Statement, character_set_client, ...
    create_sql = row[2]

    path = OUTPUT_ROOT / "triggers" / f"{safe_filename(trigger_name)}.sql"
    write_text(path, create_sql.rstrip() + ";")

    print(f"  [TRIGGER]   {trigger_name}")


# ---------------------------------------------------------------------------
# Events
# ---------------------------------------------------------------------------

def get_events(cursor) -> list[str]:
    """Return event names."""

    cursor.execute(
        """
        SELECT EVENT_NAME
        FROM information_schema.EVENTS
        WHERE EVENT_SCHEMA = %s
        ORDER BY EVENT_NAME
        """,
        (os.getenv("MYSQL_DATABASE"),),
    )

    return [row[0] for row in cursor.fetchall()]


def extract_event(cursor, event_name: str) -> None:
    """Extract CREATE EVENT."""

    cursor.execute(f"SHOW CREATE EVENT {quote_identifier(event_name)}")
    row = cursor.fetchone()

    # SHOW CREATE EVENT returns Event, sql_mode, time_zone, Create Event.
    create_sql = row[3]

    path = OUTPUT_ROOT / "events" / f"{safe_filename(event_name)}.sql"
    write_text(path, create_sql.rstrip() + ";")

    print(f"  [EVENT]     {event_name}")


# ---------------------------------------------------------------------------
# Main extraction process
# ---------------------------------------------------------------------------

def run_extraction() -> None:
    """Run the complete MySQL object extraction."""

    connection = None
    cursor = None

    try:
        ensure_output_directories()
        connection = connect_to_mysql()
        cursor = connection.cursor()

        print("\nStarting MySQL source extraction...")
        print(f"Output: {OUTPUT_ROOT}\n")

        # Tables
        tables = get_tables(cursor)
        print(f"Tables found: {len(tables)}")
        for table_name in tables:
            extract_table(cursor, table_name)

        # Views
        views = get_views(cursor)
        print(f"\nViews found: {len(views)}")
        for view_name in views:
            extract_view(cursor, view_name)

        # Procedures
        procedures = get_routines(cursor, "PROCEDURE")
        print(f"\nProcedures found: {len(procedures)}")
        for procedure_name in procedures:
            extract_routine(cursor, procedure_name, "PROCEDURE")

        # Functions
        functions = get_routines(cursor, "FUNCTION")
        print(f"\nFunctions found: {len(functions)}")
        for function_name in functions:
            extract_routine(cursor, function_name, "FUNCTION")

        # Triggers
        triggers = get_triggers(cursor)
        print(f"\nTriggers found: {len(triggers)}")
        for trigger_name in triggers:
            extract_trigger(cursor, trigger_name)

        # Events
        events = get_events(cursor)
        print(f"\nEvents found: {len(events)}")
        for event_name in events:
            extract_event(cursor, event_name)

        print("\n" + "=" * 60)
        print("MYSQL SOURCE EXTRACTION COMPLETED")
        print("=" * 60)
        print(f"Output directory: {OUTPUT_ROOT}")

    except mysql.connector.Error as exc:
        print("\nMySQL ERROR:")
        print(exc)
        sys.exit(1)

    except Exception as exc:
        print("\nEXTRACTION ERROR:")
        print(exc)
        sys.exit(1)

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()
            print("\nMySQL connection closed.")


if __name__ == "__main__":
    run_extraction()
