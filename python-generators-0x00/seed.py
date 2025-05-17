import mysql.connector
import csv
import uuid

def connect_db():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="root"
        )
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def create_database(connection):
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
    connection.commit()
    cursor.close()

def connect_to_prodev():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",  # Update with your actual password
            database="ALX_prodev"
        )
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def create_table(connection):
    cursor = connection.cursor()
    query = """
    CREATE TABLE IF NOT EXISTS user_data (
        user_id VARCHAR(36) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        age DECIMAL NOT NULL
    )
    """
    cursor.execute(query)
    connection.commit()
    print("Table user_data created successfully")
    cursor.close()

def insert_data(connection, csv_file):
    cursor = connection.cursor()
    with open(csv_file, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            user_id = str(uuid.uuid4())
            cursor.execute("""
                SELECT COUNT(*) FROM user_data WHERE email = %s
            """, (row['email'],))
            if cursor.fetchone()[0] == 0:
                cursor.execute("""
                    INSERT INTO user_data (user_id, name, email, age)
                    VALUES (%s, %s, %s, %s)
                """, (user_id, row['name'], row['email'], row['age']))
    connection.commit()
    cursor.close()
