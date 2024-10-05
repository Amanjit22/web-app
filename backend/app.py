from flask import Flask, request, jsonify
import sqlite3
import logging
import os

app = Flask(__name__)

# Folder to store uploaded files
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Set up logging
logging.basicConfig(filename='app.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s: %(message)s')

# Connect to SQLite Database
def connect_db():
    conn = sqlite3.connect('database.db')
    return conn

# Initialize the database and create a table
def init_db():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            value1 TEXT NOT NULL,
            value2 TEXT NOT NULL
        )
    ''')
    conn.commit()
    
    # Call the init_db function before handling any requests
@app.before_first_request
def initialize_database():
    init_db()


# Route to handle form submission (POST request)
@app.route('/submit', methods=['POST'])
def submit_data():
    try:
        data = request.get_json()
        value1 = data.get('value1')
        value2 = data.get('value2')

        if not value1 or not value2:
            return jsonify({'error': 'Both values are required!'}), 400

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO entries (value1, value2) VALUES (?, ?)", (value1, value2))
        conn.commit()
        conn.close()

        logging.info(f"Inserted data: {value1}, {value2}")
        return jsonify({'message': 'Data inserted successfully!'}), 200

    except Exception as e:
        logging.error(f"Error inserting data: {e}")
        return jsonify({'error': 'An error occurred while inserting data.'}), 500

# Route to fetch data (GET request)
@app.route('/fetch', methods=['GET'])
def fetch_data():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM entries")
        rows = cursor.fetchall()
        conn.close()

        entries = [{'id': row[0], 'value1': row[1], 'value2': row[2]} for row in rows]
        logging.info(f"Fetched {len(entries)} entries")
        return jsonify(entries), 200

    except Exception as e:
        logging.error(f"Error fetching data: {e}")
        return jsonify({'error': 'An error occurred while fetching data.'}), 500

# Route to handle file uploads
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    logging.info(f"Uploaded file: {file.filename}")
    return jsonify({'message': 'File uploaded successfully!', 'file': file.filename}), 200

if __name__ == '__main__':
    init_db()  # Initialize database
    app.run(debug=True)

