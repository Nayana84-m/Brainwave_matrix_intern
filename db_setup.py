import sqlite3

def create_db():
    conn = sqlite3.connect('reflections.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS reflections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            gratitude TEXT NOT NULL,
            message TEXT NOT NULL,
            wish TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_db()
