from flask import Flask, jsonify
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({
        "status": "success",
        "message": "Career Guidance API is running",
        "version": "1.0"
    })

@app.route('/api/health')
def health():
    db_exists = os.path.exists('career_guidance.db')

    college_count = 0
    if db_exists:
        try:
            conn = sqlite3.connect('career_guidance.db')
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM colleges')
            college_count = cursor.fetchone()[0]
            conn.close()
        except:
            college_count = 0

    return jsonify({
        "status": "healthy",
        "database_exists": db_exists,
        "colleges_loaded": college_count,
        "ready": db_exists and college_count > 0
    })

@app.route('/api/colleges')
def get_colleges():
    try:
        conn = sqlite3.connect('career_guidance.db')
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM colleges LIMIT 20')
        columns = [desc[0] for desc in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]

        conn.close()

        return jsonify({
            "status": "success",
            "count": len(results),
            "colleges": results
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == '__main__':
    print("🚀 Starting Simple API Server...")
    print("✅ API will be available at: http://localhost:5000")
    print("✅ Health check: http://localhost:5000/api/health")
    print("\nPress Ctrl+C to stop")

    app.run(host='0.0.0.0', port=5000, debug=True)
