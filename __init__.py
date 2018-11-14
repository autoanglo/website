from flask import Flask
from flask import render_template, redirect, url_for, request
from flask_navigation import Navigation
from flask_login import LoginManager, login_user, logout_user, UserMixin, login_required
import json

from User import User
from PageManager import PageManager
from DatabaseWrapper import Data
from UsersDatabaseWrapper import UserData
from website import Website

#### APP Setup ####
app = Flask(__name__)
app.config.update(SECRET_KEY = '541')

#### Login Manager Setup ####
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def user_loader(userid):
    return user_data.get_user_by_id(userid)

#### Navigation bar setup ####
nav = Navigation(app)
nav.Bar('top', [nav.Item('Home', 'home'), nav.Item('Showcase', 'showcase'), nav.Item("Shop", r"shop"), nav.Item("About", "about")])

#### Globals ####
data = Data()
user_data = UserData()
page_size = 5
website = Website()

@app.route('/', defaults={'page': 1})
@app.route('/page/<int:page>')
def home(page):
    return website.galery_with_tag(page)

@app.route('/showcase', defaults={'page': 1})
@app.route('/showcase/<int:page>')
def showcase(page): 
    return website.galery_with_tag(page, "showcase")
    

@app.route("/shop")
def shop():
    return website.redirect_to("https://www.etsy.com/shop/EmilyLandBasics")

@app.route("/about")
def about():
    return website.render_template("about.html")

@app.route('/post/<post_id>')
def view_post(post_id):
    return render_template("view_post.html", post=data.get_post_by_id(post_id))

##### ADMIN PAGES #####
@app.route('/post/<post_id>/delete')
@login_required
def delete_post(post_id):
    website.delete_post(post_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    user = None
    if request.method == 'POST':
        user = website.login_user(request)
        if user:
            next = request.args.get('next')
            if not next:
                next = ""
            login_user(user, remember=True)
            return redirect(next)
        else:
            error = 'Invalid Credentials. Please try again.'
    return render_template('login.html', error=error)

@app.route('/upload', methods=['GET', 'POST'])  
@login_required
def upload():
    if request.method == 'POST':
        return website.upload_post(request)
    return render_template("upload.html")

