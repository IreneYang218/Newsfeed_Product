from app import application, classes, db
from flask import render_template, redirect, url_for
from flask import request, jsonify  # handle form
from flask_login import current_user, login_user, login_required, logout_user


@application.route('/index')
@application.route('/')
def index():
    """Render introduction page."""
    return render_template('index.html')


@application.route('/NewsPhi')
def newsPhi():
    """Render main page."""
    return render_template('main_app.html')


@application.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration."""
    if request.method == 'POST':
        print(request.json)
        password = request.json['password']
        email = request.json['email']
        username = email.split('@')[0]

        user_count = classes.User.query.filter_by(email=email).count()
        if user_count > 0:  # email exists
            return '<h1> Error - Existing User:' + email + '</h1>'
        user = classes.User(username, email, password)
        db.session.add(user)
        db.session.commit()
        return '<h1> Registered : ' + email + '</h1>'


@application.route('/login', methods=['POST'])
def login():
    """Handle user log-in."""
    error = None
    email = request.json['email']
    password = request.json['password']

    # Look for it in the database.
    user = classes.User.query.filter_by(email=email).first()
    if user is not None and user.check_password(password):
        login_user(user)
        resp = jsonify({'status': 'ok', 'user': user.email})
        resp.status_code = 200
    else:
        error = 'Invalid Credentials. Please try again.'
        resp = jsonify({'status': 'failed', 'msg': error})
        resp.status_code = 403
    return resp


@application.route('/userinfo', methods=['GET'])
@login_required
def get_useinfo():
    """Get user's information."""
    return jsonify({'email': current_user.email})


@application.route('/logout', methods=['POST'])
@login_required
def logout():
    """Handle user log-out"""
    logout_user()
    return jsonify({'status': 'ok'})
