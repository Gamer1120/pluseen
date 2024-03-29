import os
from datetime import datetime
from typing import NamedTuple, Optional

from flask import g
from psycopg import Connection
from psycopg.rows import namedtuple_row

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres@localhost:5432/postgres")

# Types
Pluseen = NamedTuple("Record", [("id", int), ("name", str), ("description", str), ("created_at", datetime)])
Deelnemer = NamedTuple("Record", [("id", int), ("name", str)])
Status = NamedTuple("Record", [("id", int), ("name", str), ("status", int), ("comment", str), ("updated_at", datetime)])


def get_db() -> Connection:
    if 'db' not in g:
        g.db = Connection.connect(DATABASE_URL, row_factory=namedtuple_row)
    return g.db


db_definition = {
    "pluseens": {
        "id": "SERIAL NOT NULL PRIMARY KEY",
        "name": "TEXT NOT NULL UNIQUE",
        "description": "TEXT",
        "created_at": "TIMESTAMPTZ NOT NULL DEFAULT now()"
    },
    "deelnemers": {
        "id": "SERIAL NOT NULL PRIMARY KEY",
        "name": "TEXT NOT NULL UNIQUE"
    },
    "pluseendeelnemers": {
        "pluseen_id": "INT NOT NULL REFERENCES pluseens (id) ON DELETE CASCADE",
        "deelnemer_id": "INT NOT NULL REFERENCES deelnemers (id) ON DELETE CASCADE",
        "status": "INT NOT NULL",
        "comment": "TEXT",
        "updated_at": "TIMESTAMPTZ NOT NULL DEFAULT now()",
        "": "PRIMARY KEY (pluseen_id, deelnemer_id)"
    }
}


def init_db() -> None:
    table_query = do_query("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
    db_tables = list(map(lambda x: x.table_name, table_query))
    for (table, table_definition) in db_definition.items():
        if table in db_tables:
            column_query = do_query("SELECT column_name FROM information_schema.columns WHERE table_schema = 'public' AND table_name = %s;", (table,))
            table_columns = list(map(lambda x: x.column_name, column_query))
            for (column, column_definition) in table_definition.items():
                if column and column not in table_columns:
                    do_query(f"ALTER TABLE {table} ADD COLUMN {column} {column_definition};")
        else:
            table_definition = ",".join(" ".join(_) for _ in table_definition.items())
            do_query(f"CREATE TABLE {table} ({table_definition});")


def close_db(e=None) -> None:
    db = g.pop('db', None)
    if db is not None:
        db.close()


def do_query(query: str, vars: Optional[tuple] = None):
    print(query, vars)
    db = get_db()
    with db.execute(query, vars, prepare=True) as cursor:
        if query.startswith("SELECT"):
            return cursor.fetchall()
        else:
            db.commit()
            return None


def list_pluseens() -> [Pluseen]:
    return do_query("SELECT * FROM pluseens ORDER BY DATE_TRUNC('day', created_at) DESC, LOWER(name);")


def get_pluseen(pluseen_name: str) -> Optional[Pluseen]:
    results = do_query("SELECT * FROM pluseens WHERE name = %s;", (pluseen_name,))
    if len(results) == 1:
        return results[0]
    else:
        return None


def add_pluseen(pluseen_name: str, description: Optional[str] = None) -> None:
    do_query("INSERT INTO pluseens (name, description, created_at) VALUES (%s, %s, now()) ON CONFLICT DO NOTHING;", (pluseen_name, description))


def update_pluseen(pluseen_name: str, description: Optional[str] = None) -> None:
    do_query("UPDATE pluseens SET description = %s WHERE name = %s;", (description, pluseen_name))


def list_deelnemers() -> [Deelnemer]:
    return do_query("SELECT * FROM deelnemers ORDER BY name;")


def get_deelnemer(deelnemer_name: str) -> Optional[Deelnemer]:
    results = do_query("SELECT * FROM deelnemers WHERE name = %s;", (deelnemer_name,))
    if len(results) == 1:
        return results[0]
    else:
        return None


def get_statuses(pluseen_id: int) -> [Status]:
    return do_query(
        "SELECT d.id, d.name, COALESCE(p.status, 0) AS status, p.comment, p.updated_at "
        "FROM deelnemers d "
        "LEFT JOIN (SELECT * FROM pluseendeelnemers p WHERE p.pluseen_id = %s) AS p ON d.id = p.deelnemer_id "
        "ORDER BY d.name",
        (pluseen_id,)
    )


def get_status(pluseen_id: int, deelnemer_name: str) -> Optional[Status]:
    results = do_query(
        "SELECT d.id, d.name, COALESCE(p.status, 0) AS status, p.comment, p.updated_at "
        "FROM deelnemers d "
        "LEFT JOIN (SELECT * FROM pluseendeelnemers p WHERE p.pluseen_id = %s) AS p ON d.id = p.deelnemer_id "
        "WHERE d.name = %s",
        (pluseen_id, deelnemer_name)
    )
    if len(results) == 1:
        return results[0]
    else:
        return None


def set_status(pluseen_id: int, deelnemer_id: int, status: int, comment: Optional[str]) -> None:
    do_query(
        "INSERT INTO pluseendeelnemers (pluseen_id, deelnemer_id, status, comment, updated_at) VALUES (%s, %s, %s, %s, now()) "
        "ON CONFLICT (pluseen_id, deelnemer_id) DO UPDATE SET status=excluded.status, comment=excluded.comment, updated_at=now();",
        (pluseen_id, deelnemer_id, status, comment)
    )
