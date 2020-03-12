import sqlite3
from collections import namedtuple

Entry = namedtuple("Entry", ["id", "user", "score"])


class SQLite:
    def __init__(self, file="sqlite.db"):
        self.file = file

    def __enter__(self):
        self.conn = sqlite3.connect(self.file)
        self.conn.row_factory = sqlite3.Row
        return self.conn.cursor()

    def __exit__(self, type, value, traceback):
        self.conn.commit()
        self.conn.close()


ENTRIES_SCHEMA = """
CREATE TABLE IF NOT EXISTS entries(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user TEXT NOT NULL UNIQUE,
  score INT NOT NULL
);
"""

DB = "entries.db"


def get_entries():
    with SQLite(DB) as cur:
        cur.execute("SELECT id, user, score FROM ENTRIES")
        return [Entry(*row) for row in cur.fetchall()]


def push_submission(user, score):
    with SQLite(DB) as cur:
        cur.execute("INSERT INTO entries (user, score) VALUES (?, ?)", (user, score))


def create_schema():
    with SQLite(DB) as cur:
        cur.execute(ENTRIES_SCHEMA)
