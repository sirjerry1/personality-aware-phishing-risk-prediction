import os
import sqlite3

from config import Config

from config import Config

def get_connection():
    print("Database Path:", Config.DATABASE)

    connection = sqlite3.connect(Config.DATABASE)
    connection.row_factory = sqlite3.Row
    return connection

def create_tables():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
CREATE TABLE IF NOT EXISTS participants(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    -- Demographics
    age TEXT,
    gender TEXT,
    occupation TEXT,
    education TEXT,
    email_use TEXT,
    cyber_training TEXT,

    -- TIPI Questions
    tipi_q1 INTEGER,
    tipi_q2 INTEGER,
    tipi_q3 INTEGER,
    tipi_q4 INTEGER,
    tipi_q5 INTEGER,
    tipi_q6 INTEGER,
    tipi_q7 INTEGER,
    tipi_q8 INTEGER,
    tipi_q9 INTEGER,
    tipi_q10 INTEGER,

    -- Phishing Scenarios
    scenario1 INTEGER,
    scenario2 INTEGER,
    scenario3 INTEGER,
    scenario4 INTEGER,
    scenario5 INTEGER,

    -- Post-study Survey
    confidence INTEGER,
    comments TEXT

)
""")

    connection.commit()
    connection.close()


if __name__ == "__main__":
    create_tables()
    print("Database created successfully!")