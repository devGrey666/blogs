from flask import Blueprint, render_template
from flask_login import login_required
main = Blueprint('main', __name__)
@main.route('/')
@main.route("/home")
def home():
    return render_template("home.html", title='Home')

@main.route("/blogs")
@login_required
def blogs():
    return render_template("blogs.html", title='Blogs')

@main.route("/about")
@login_required
def about():
    return render_template("about.html", title='About Page')

