import sqlite3

class DatabaseConnection:
    """Custom context manager for database connection using SQLite"""

    def __enter__(self):
        self.conn = sqlite3.connect("my_database.db")
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.commit()
        self.conn.close()

# Example usage
if __name__ == "__main__":
    # Optional setup to create the table and add some test users
    with sqlite3.connect("my_database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            );
        """)
        # Insert users only if table is empty
        cursor.execute("SELECT COUNT(*) FROM users;")
        if cursor.fetchone()[0] == 0:
            cursor.executemany("INSERT INTO users (name) VALUES (?)", [
                ('Alice',), ('Bob',), ('Charlie',)
            ])
        conn.commit()

    # Use context manager to query users
    with DatabaseConnection() as db:
        db.execute("SELECT * FROM users")
        results = db.fetchall()
        for row in results:
            print(row)

