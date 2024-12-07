import sqlite3

def create_database(db_name):
    try:
        # Connect to SQLite (creates the file if it doesn't exist)
        conn = sqlite3.connect(f"{db_name}.db")
        cursor = conn.cursor()

        # Example: Create a table to ensure the database is usable
        cursor.execute("CREATE TABLE IF NOT EXISTS example_table (id INTEGER PRIMARY KEY, name TEXT);")
        
        print(f"Database '{db_name}.db' created or already exists.")
        
        # Commit and close the connection
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"Error connecting to SQLite: {e}")

# Parameters
db_name = 'plm_mgo'

# Create the database
create_database(db_name)
