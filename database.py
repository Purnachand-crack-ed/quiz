import sqlite3

def create_database():
    print("Creating database and table...")

    conn = sqlite3.connect('quiz_results.db')
    cursor = conn.cursor()
    
    # Create table for storing user data and scores
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT NOT NULL,
            marks INTEGER NOT NULL
        )
    ''')
    
    conn.commit()
    print("Database and table created successfully.")

    conn.close()

if __name__ == "__main__":
    create_database()
