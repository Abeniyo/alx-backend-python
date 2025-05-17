import seed

def stream_user_ages():
    connection = seed.connect_to_prodev()
    cursor = connection.cursor()
    cursor.execute("SELECT age FROM user_data")
    while True:
        row = cursor.fetchone()
        if row is None:
            break
        yield row[0]
    cursor.close()
    connection.close()

def compute_average_age():
    total = 0
    count = 0
    for age in stream_user_ages():
        total += age
        count += 1
    average = total / count if count > 0 else 0
    print(f"Average age of users: {average}")
