# Flask Form Application with MongoDB

This is a Flask application that demonstrates form submission to MongoDB Atlas and includes an API endpoint.

## Features

- Form submission with MongoDB Atlas integration
- API endpoint that returns JSON data
- Error handling and success messages
- Modern UI with Bootstrap

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file in the root directory with your MongoDB Atlas connection string:
```
MONGODB_URI=your_mongodb_connection_string
```

3. Run the application:
```bash
python app.py
```

## Usage

- Access the form at: `http://localhost:5000/`
- Access the API endpoint at: `http://localhost:5000/api`

## API Endpoint

The `/api` endpoint returns a JSON list of items from the `data.json` file.

## Form Submission

The form collects:
- Name
- Email
- Message

Upon successful submission, users are redirected to a success page. If there's an error, it's displayed on the form page. 