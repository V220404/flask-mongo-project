from flask import Flask, jsonify, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
from bson.objectid import ObjectId
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
todo_collection = db['todos']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/todo')
def todo():
    todos = list(todo_collection.find())
    return render_template('todo.html', todos=todos)

@app.route('/add_todo', methods=['POST'])
def add_todo():
    try:
        item_name = request.form.get('item_name')
        item_description = request.form.get('item_description')

        if not all([item_name, item_description]):
            flash('All fields are required!', 'error')
            return redirect(url_for('todo'))

        todo = {
            'item_name': item_name,
            'item_description': item_description
        }
        todo_collection.insert_one(todo)
        flash('Todo added successfully!', 'success')
        return redirect(url_for('todo'))
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
        return redirect(url_for('todo'))

@app.route('/delete_todo/<todo_id>', methods=['POST'])
def delete_todo(todo_id):
    try:
        todo_collection.delete_one({'_id': ObjectId(todo_id)})
        flash('Todo deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting todo: {str(e)}', 'error')
    return redirect(url_for('todo'))

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