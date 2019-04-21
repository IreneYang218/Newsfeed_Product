from app import application
from flask import render_template, redirect, url_for, request, session, flash, g
from flask-bcrypt import Bcrypt
from functools import wraps
import sqlite3

# config
application.secret_key = "newsphi"
application.database = 'sample.db'

# login required decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap

@application.route('/')
def index():
    # and render posts with render_template
    return("<h1> WELCOME TO NEWSPHI</h1>")
    # return(render_template("index.html", author='Yixin Sun'))

@application.route('/personalized')
# Protect this page and required logged in first
@login_required
def feeds():
    return(render_template("secrete_page.html"))
    # return(render_template("index.html", author='Yixin Sun'))

# Route for handling the login page logic
@application.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            session['logged_in'] = True
            flash('You were just logged in!')
            return redirect(url_for('feeds'))
    return render_template('index.html', error=error)

@application.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were just logged out!')
    return redirect(url_for('index'))

def connect_db():
    return sqlite3.connect(application.database)

if __name__ == '__main__':
    application.run(debug=True)
