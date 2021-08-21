from flask import Blueprint
from flask.templating import render_template

views = Blueprint('views', __name__)

@views.route('/')
def home_page():
    return render_template('home.html')

@views.route('/mylyrics')
def mylyrics_page():
    return render_template('mylyrics.html')

@views.route('/alllyrics')
def alllyrics_page():
    return render_template('alllyrics.html')