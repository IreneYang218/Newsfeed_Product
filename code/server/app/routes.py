from app import application, classes, db
from flask import render_template, redirect, url_for  # need for Week3 Homework
from flask import request  # handle form
from flask_login import current_user, login_user, login_required, logout_user


@application.route('/index')
@application.route('/')
def index():
    """Render main page"""
    # button for signup
    # button for login
    # return("<h1> WELCOME TO NEWSPHI </h1>")
    return render_template('index.html')

#
# @application.route('/login_page', methods=['GET', 'POST'])
# def login_page():
#     """Render the user log in page"""
#     if request.method == 'GET':
#         return render_template('login.html')
#
#
# @application.route('/signup_page', methods=['GET', 'POST'])
# def signup_page():
#     """render the user sign up page"""
#     if request.method == 'GET':
#         return render_template('signup.html')


@application.route('/register', methods=['GET', 'POST'])
def register():
    """User register"""
    error = None
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


@application.route('/login', methods=['GET', 'POST'])
def login():
    """Log user in"""
    error = None
    if request.method == 'POST':
        email = request.json['email']
        password = request.json['password']
        username = email.split('@')[0]
        # Look for it in the database.
        user = classes.User.query.filter_by(email=email).first()
        if user is not None and user.check_password(password):

            login_user(user)
            return redirect(url_for('secret_page'))
            # return '<h1> Logged in : ' + username + '</h1>'
        else:
            error = 'Invalid Credentials. Please try again.'
            # return '<h1> Invalid username and password combination! </h1>'
    return redirect(url_for('index'))


@application.route('/secret_page', methods=['GET', 'POST'])
@login_required
def secret_page():
    """Render the page for login user"""
    return render_template('secret.html',
                           name=current_user.username,
                           email=current_user.email)


@application.route('/logout')
@login_required
def logout():
    """Log user out"""
    before_logout = '<h1> Before logout - is_autheticated : ' \
                    + str(current_user.is_authenticated) + '</h1>'

    logout_user()

    after_logout = '<h1> After logout - is_autheticated : ' \
                   + str(current_user.is_authenticated) + '</h1>'
    return before_logout + after_logout
