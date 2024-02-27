# Import necessary modules from Flask framework
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Create a Flask application instance
app = Flask(__name__)

# Wrap the Flask app instance in CORS to allow cross-origin resource sharing
CORS(app)

# Configure the SQLAlchemy database URI and disable modification tracking
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create an instance of SQLAlchemy and bind it to the Flask app
db = SQLAlchemy(app)
