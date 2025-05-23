import sqlite3

class DatabaseConnection:
    """Custom context manager for SQLite DB without __init__"""

    def __enter__(self):
        # Open database connection (hardcoded DB name)
        self.conn = sqlite3.connect("my_database.db")
        self.cursor = self.conn.cursor()
        return self.cursor  # Return cursor to allow query execution

    def __exit__(self, exc_type, exc_value, traceback):
        # Commit and close connection
        self.conn.commit()
        self.conn.close()

# Ensure the database and users table exist with some data
with sqlite3.connect("my_database.db") as conn:
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        );
    """)
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("INSERT INTO users (name) VALUES (?)", [
            ('Alice',), ('Bob',), ('Charlie',)
        ])
    conn.commit()

# Use the custom context manager to run SELECT * FROM users
with DatabaseConnection() as db:
    db.execute("SELECT * FROM users")
    for row in db.fetchall():
        print(row)
