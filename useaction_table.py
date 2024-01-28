import sqlite3

conn = sqlite3.connect("database/clients.db", check_same_thread=False)

def create_table():
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clients (
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           name TEXT NOT NULL,
           last_name TEXT NOT NULL,
           birthdate DATE NOT NULL,
           email TEXT NOT NULL
        )
    """)
    conn.commit()
    
    
create_table()