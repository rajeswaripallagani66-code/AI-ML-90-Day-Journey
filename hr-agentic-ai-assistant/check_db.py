import sqlite3
conn = sqlite3.connect('app/hr.db')
rows = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
print(rows)
for r in rows:
    print("TABLE:", r[0])
    try:
        cols = conn.execute(f"PRAGMA table_info({r[0]})").fetchall()
        print(cols)
    except Exception as e:
        print(e)