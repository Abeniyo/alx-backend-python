import sqlite3

class DatabaseConnection:
    """Custom context manager for database connection"""

    def __enter__(self):
        self.conn = sqlite3.connect("my_database.db")
        self.cursor = self.conn.cursor()
        return self.cursor  # Return cursor to run queries

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.commit()
        self.conn.close()

# Setup: Ensure table and data exist (not part of the class)
with sqlite3.connect("my_database.db") as conn:
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        );
    ''')
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("INSERT INTO users (name) VALUES (?)", [
            ('Alice',), ('Bob',), ('Charlie',)
        ])
    conn.commit()

# Use the custom context manager to run SELECT query
with DatabaseConnection() as db:
    db.execute("SELECT * FROM users")
    rows = db.fetchall()
    for row in rows:
        print(row)
