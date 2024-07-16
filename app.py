from flask import Flask, jsonify, render_template, request
import psycopg2
import os

app = Flask(__name__)


def get_db_connection():
    conn = psycopg2.connect(
        dbname="data_dashboard",
        user="postgres",
        password="1234",
        host="localhost"
    )
    return conn


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/data', methods=['GET'])
def get_data():
    filters = request.args
    query = "SELECT * FROM insights WHERE 1=1"

    if filters:
        for key, value in filters.items():
            if value:
                query += f" AND {key}='{value}'"

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    data = [dict(zip(columns, row)) for row in rows]
    cursor.close()
    conn.close()
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
