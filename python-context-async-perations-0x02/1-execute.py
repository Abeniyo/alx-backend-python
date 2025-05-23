import sqlite3

class ExecuteQuery:
    def __init__(self, query, params):
        self.query = query
        self.params = params
    def __enter__(self):
        self.conn = sqlite3.connect('users.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.query, self.params)
        return self.cursor.fetchall()
    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.commit()
        self.conn.close()

with ExecuteQuery("SELECT * FROM users WHERE age > ?", (25,)) as results:
    print(results)
