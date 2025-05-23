import requests
from flask import Flask, request, jsonify
import pymysql
import os
from dotenv import load_dotenv
load_dotenv()

conn = pymysql.connect(host=os.getenv('DB_HOST'), user=os.getenv('DB_USER'), password=os.getenv('DB_PASSWORD'), db=os.getenv('DB_NAME'))
if conn:
    print("Connected to MySQL")
else:
    print("Failed to connect to MySQL")
app = Flask(__name__,template_folder='templates')

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/api/data')
def get_data():
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("select * from chitiethoadon")
    data = cursor.fetchall()
    return jsonify(data)
if __name__ == '__main__':
    app.run(debug=True,port=6969)

