from flask import Flask, request, jsonify
import sqlite3
import logging
import os

app = Flask(__name__)

# Set up logging
logging.basicConfig(filename='app.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s: %(message)s')

# Connect to SQLite Database
def connect_db():
    """Establish a connection to the SQLite database."""
    conn = sqlite3.connect('database.db')  # SQLite database file
    return conn

# Initialize the database and create a table
def init_db():
    """Initialize the database, creating the 'entries' table if it doesn't exist."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            value1 TEXT NOT NULL,
            value2 TEXT NOT NULL
        )
    ''')
    conn.commit()  # Save (commit) the changes
    conn.close()   # Close the connection to the database

# Route to handle form submission (POST request)
@app.route('/submit', methods=['POST'])
def submit_data():
    """Handles the submission of form data."""
    try:
        data = request.get_json()  # Get the JSON data from the request
        value1 = data.get('value1')
        value2 = data.get('value2')

        # Validate the input values
        if not value1 or not value2:
            return jsonify({'error': 'Both values are required!'}), 400

        # Insert the data into the SQLite database
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO entries (value1, value2) VALUES (?, ?)", (value1, value2))
        conn.commit()
        conn.close()

        # Log success
        logging.info(f"Inserted data: {value1}, {value2}")
        return jsonify({'message': 'Data inserted successfully!'}), 200

    except Exception as e:
        logging.error(f"Error inserting data: {e}")
        return jsonify({'error': 'An error occurred while inserting data.'}), 500

# Route to fetch data (GET request)
@app.route('/fetch', methods=['GET'])
def fetch_data():
    """Fetches all data from the database."""
    try:
        conn = connect_db()  # Open a database connection
        cursor = conn.cursor()

        # Query to fetch all data from the 'entries' table
        cursor.execute("SELECT * FROM entries")
        rows = cursor.fetchall()  # Get all rows of data
        conn.close()  # Close the connection

        # Create a list of dictionaries with fetched data
        entries = [{'id': row[0], 'value1': row[1], 'value2': row[2]} for row in rows]
        logging.info(f"Fetched {len(entries)} entries")
        return jsonify(entries), 200

    except Exception as e:
        logging.error(f"Error fetching data: {e}")
        return jsonify({'error': 'An error occurred while fetching data.'}), 500

# Initialize the database before the first request
if __name__ == '__main__':
    init_db()  # Initialize database when the app starts
    app.run(debug=True)

