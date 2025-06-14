from flask import Flask, jsonify, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)

# MongoDB connection
client = MongoClient(os.getenv('MONGODB_URI'))
db = client['form_data']
collection = db['submissions']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api')
def api():
    try:
        with open('data.json', 'r') as file:
            data = json.load(file)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/submit', methods=['POST'])
def submit():
    try:
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        if not all([name, email, message]):
            flash('All fields are required!', 'error')
            return render_template('index.html')

        # Insert data into MongoDB
        submission = {
            'name': name,
            'email': email,
            'message': message
        }
        collection.insert_one(submission)
        
        return redirect(url_for('success'))
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
        return render_template('index.html')

@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    app.run(debug=True) 