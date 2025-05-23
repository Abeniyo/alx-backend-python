import os
import sqlite3

# Check if 0-databaseconnection.py exists and is not empty
file_path = "0-databaseconnection.py"
if not os.path.exists(file_path):
    print(f"Error: {file_path} does not exist")
elif os.path.getsize(file_path) == 0:
    print(f"Error: {file_path} is empty")
else:
    print(f"{file_path} exists and is not empty")

# Define DatabaseConnection context manager
class DatabaseConnection:
    def __enter__(self):
        try:
            self.conn = sqlite3.connect('users.db')
            self.cursor = self.conn.cursor()
            # Ensure users table exists
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                                (id INTEGER PRIMARY KEY, name TEXT, email TEXT)''')
            self.conn.commit()
            return self.cursor
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
            raise

    def __exit__(self, exc_type, exc_value, traceback):
        try:
            if hasattr(self, 'conn'):
                self.conn.commit()
                self.cursor.close()
                self.conn.close()
        except sqlite3.Error as e:
            print(f"Error closing database: {e}")
            raise

# Using context manager to perform query
try:
    with DatabaseConnection() as cursor:
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        if results:
            print("\nQuery Results:")
            for row in results:
                print(row)
        else:
            print("\nNo records found in users table")
except sqlite3.Error as e:
    print(f"Database error: {e}")
except Exception as e:
    print(f"General error: {e}")
