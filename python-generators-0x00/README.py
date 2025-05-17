# Python Generators - Task 0: Getting Started with Python Generators

This project introduces the concept of **Python generators** for efficient data processing, focusing on streaming rows from a SQL database one at a time using lazy evaluation. This approach is ideal for handling large datasets without overloading system memory.

## Task Objective

Create a Python script (`seed.py`) that:

- Sets up a MySQL database called `ALX_prodev`
- Creates a `user_data` table with appropriate constraints and data types
- Reads user data from `user_data.csv`
- Inserts records into the database while avoiding duplicates
- Uses **generators** to efficiently stream rows one by one

## Technologies

- Python 3
- MySQL Server
- MySQL Connector for Python (`mysql-connector-python`)
- CSV
- UUID
- Generators

##  Database Schema

**Database:** `ALX_prodev`  
**Table:** `user_data`

| Column   | Type     | Constraints              |
|----------|----------|--------------------------|
| user_id  | VARCHAR  | Primary Key, UUID, Indexed |
| name     | VARCHAR  | NOT NULL                 |
| email    | VARCHAR  | NOT NULL                 |
| age      | DECIMAL  | NOT NULL                 |

## Project Structure

