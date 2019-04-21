from flask import Flask
from flask-bcrypt import Bcrypt
import os

# Initialization
# Create an application instance (an object of class Flask)  which handles all requests.
application = Flask(__name__)
application.secret_key = os.urandom(24)
bcrypt = Bcrypt(application)

from app import routes # routes.py needs to import "application" variable in __init__.py (Altough it violates PEP8 standards)
