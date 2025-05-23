import os
import sqlite3

# Check if file exists and is not empty
if not os.path.exists('0-databaseconnection.py'):
    print("Error: 0-databaseconnection.py does not exist")
elif os.path.getsize('0-databaseconnection.py') == 0:
    print("Error: 0-databaseconnection.py is empty")
else:
    print("0-databaseconnection.py exists and is not empty")

class DatabaseConnection:
    def __enter__(self):
        self.conn = sqlite3.connect('users.db')
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

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
    print(f"Error: {e}")
