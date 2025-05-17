import seed

def stream_users():
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")
    while True:
        row = cursor.fetchone()
        if row is None:
            break
        yield row
    cursor.close()
    connection.close()
