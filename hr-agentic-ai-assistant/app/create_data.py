import sqlite3

conn = sqlite3.connect("hr.db")
cur = conn.cursor()
cur.execute("DROP TABLE IF EXISTS employees")
cur.execute("CREATE TABLE employees (emp_id TEXT PRIMARY KEY, name TEXT, leaves_left INT, manager_email TEXT)")
cur.execute("DROP TABLE IF EXISTS leaves")
cur.execute("CREATE TABLE leaves (id INTEGER PRIMARY KEY AUTOINCREMENT, emp_id TEXT, start_date TEXT, days INT)")

# 50 employees - 2 real + 48 dummy
cur.execute("INSERT INTO employees VALUES ('EMP123','Rajeswari',12,'manager@company.com')")
cur.execute("INSERT INTO employees VALUES ('EMP124','Syashu',8,'manager@company.com')")
for i in range(125, 173):
    cur.execute("INSERT INTO employees VALUES (?,?,?,?)", (f"EMP{i}", f"Employee{i}", 10, "manager@company.com"))

conn.commit(); conn.close()
print("DB Created - 50 employees")