import sqlite3
import pandas as pd

# Connect to the database
connection = sqlite3.connect("research.db")

# Read the participants table
df = pd.read_sql_query(
    "SELECT * FROM participants",
    connection
)

# Export to CSV
df.to_csv(
    "participants.csv",
    index=False
)

connection.close()

print("=" * 40)
print("Export completed successfully!")
print(f"Participants exported: {len(df)}")
print("File created: participants.csv")
print("=" * 40)