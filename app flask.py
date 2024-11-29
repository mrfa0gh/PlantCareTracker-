from flask import Flask, jsonify, render_template
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('plants.db')
    conn.row_factory = sqlite3.Row 
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/plant-data', methods=['GET'])
def get_plant_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT plant, uv, moisture, vegetation_index, time FROM plant_data")
    data = [{"plant": row['plant'], "uv": row['uv'], "moisture": row['moisture'], "vegetation_index": row['vegetation_index'], "time": row['time']} for row in cursor.fetchall()]
    conn.close()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
