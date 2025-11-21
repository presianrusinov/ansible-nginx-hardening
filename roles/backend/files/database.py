import sqlite3

DB_PATH = "/var/www/ai_project/data.sqlite"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    with open("/var/www/ai_project/schema.sql", "r") as f:
        conn.executescript(f.read())
    conn.close()

