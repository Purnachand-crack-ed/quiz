import sqlite3

def view_entries():
    conn = sqlite3.connect('quiz_results.db')
    cursor = conn.cursor()
    
    # Fetch all entries from the results table
    cursor.execute('SELECT * FROM results')
    rows = cursor.fetchall()
    
    # Print the entries
    for row in rows:
        print(f"ID: {row[0]}, Name: {row[1]}, Phone: {row[2]}, Email: {row[3]}, Marks: {row[4]}")
    
    conn.close()

if __name__ == "__main__":
    view_entries()
