import os
from typing import NamedTuple, Optional

import psycopg2
from flask import g
from psycopg2.extras import NamedTupleCursor

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres@localhost:5432/postgres")

# Types
Pluseen = NamedTuple("Record", [("id", int), ("name", str)])
Deelnemer = NamedTuple("Record", [("id", int), ("name", str)])
Status = NamedTuple("Record", [("id", int), ("name", str), ("status", int)])


def get_db():
    if 'db' not in g:
        g.db = psycopg2.connect(DATABASE_URL, cursor_factory=NamedTupleCursor, sslmode="prefer")
    return g.db


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def do_query(query: str, vars: tuple = None):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(query, vars)
        if query.startswith("SELECT"):
            result = cursor.fetchall()
            return result
        else:
            db.commit()
            return None
    finally:
        cursor.close()


def list_pluseens() -> [Pluseen]:
    return do_query("SELECT * FROM pluseens ORDER BY name;")


def get_pluseen(pluseen_name: str) -> Optional[Pluseen]:
    results = do_query("SELECT * FROM pluseens WHERE name = %s;", (pluseen_name,))
    if len(results) == 1:
        return results[0]
    else:
        return None


def add_pluseen(pluseen_name: str) -> None:
    do_query("INSERT INTO pluseens (name) VALUES (%s) ON CONFLICT DO NOTHING;", (pluseen_name,))


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
        "SELECT d.id, d.name, COALESCE(p.status, 0) AS status FROM deelnemers d LEFT JOIN (SELECT p.deelnemer_id, p.status FROM pluseendeelnemers p WHERE p.pluseen_id = %s) AS p ON d.id = p.deelnemer_id ORDER BY d.name",
        (pluseen_id,)
    )


def get_status(pluseen_id: int, deelnemer_name: str) -> Optional[Status]:
    results = do_query(
        "SELECT d.id, d.name, COALESCE(p.status, 0) AS status FROM deelnemers d LEFT JOIN (SELECT p.deelnemer_id, p.status FROM pluseendeelnemers p WHERE p.pluseen_id = %s) AS p ON d.id = p.deelnemer_id WHERE d.name = %s",
        (pluseen_id, deelnemer_name)
    )
    if len(results) == 1:
        return results[0]
    else:
        return None


def set_status(pluseen_id: int, deelnemer_id: int, status: int) -> None:
    do_query(
        "INSERT INTO pluseendeelnemers (pluseen_id, deelnemer_id, status) VALUES (%s, %s, %s) ON CONFLICT (pluseen_id, deelnemer_id) DO UPDATE SET status=excluded.status;",
        (pluseen_id, deelnemer_id, status)
    )
