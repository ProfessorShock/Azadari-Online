from flask import Blueprint
from flask.templating import render_template

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login_page():
    return render_template('login.html')

@auth.route('/sign-up')
def signup_page():
    return render_template('signup.html')

@auth.route('/logout')
def logout():
    pass