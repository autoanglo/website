from flask import Flask
from flask import render_template, redirect, url_for, request
from flask_navigation import Navigation
from flask_login import LoginManager, login_user, logout_user, UserMixin, login_required
import json

from User import User
from PageManager import PageManager
from DatabaseWrapper import Data
from UsersDatabaseWrapper import UserData

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

@app.route('/', defaults={'page': 1})
@app.route('/page/<int:page>')
def home(page): 
    lower_index = page_size * page - page_size
    upper_index = page_size * page
    page_manager = PageManager(data.data, page_size, page)
    return render_template("home.html", data=data.data[lower_index:upper_index], pages=page_manager)

@app.route('/showcase', defaults={'page': 1})
@app.route('/showcase/<int:page>')
def showcase(page): 
    data2 = data.get_posts_by_tag("showcase")
    lower_index = page_size * page - page_size
    upper_index = page_size * page
    page_manager = PageManager(data2, page_size, page)
    return render_template("home.html", data=data2[lower_index:upper_index], pages=page_manager)

@app.route("/shop")
def shop():
    return redirect("https://www.etsy.com/shop/EmilyLandBasics")

@app.route("/about")
def about():
    about = "Dyno Unique "\
            "is a climbing gear company based in Oregon specializing in unique and fun chalk bags. All products" \
            "are hand made at home."
    return render_template("about.html", about=about)

@app.route('/post/<post_id>')
def view_post(post_id):
    return render_template("view_post.html", post=data.get_post_by_id(post_id))

##### ADMIN PAGES #####
@app.route('/post/<post_id>/delete')
@login_required
def delete_post(post_id):
    data.delete_post_by_id(post_id)
    return_url = request.referrer
    return redirect("/")

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if len(user_data.data) < 1:
            new_user=User(0, username, password)
            user_data.add_user(new_user)
        for user in user_data.data:
            print(user.name)
            if user.is_username(username):
                if user.login_user(username, password):
                    next = request.args.get('next')
                    login_user(user, remember=True)
                    return redirect(next)
        else:
            error = 'Invalid Credentials. Please try again.'
    return render_template('login.html', error=error)

@app.route('/upload', methods=['GET', 'POST'])  
@login_required
def upload():
    if request.method == 'POST':
        post = {}
        post["title"] = request.form["title"]
        post["link"] = request.form["link"]
        post["description"] = request.form["description"]
        post["tags"] = request.form["tags"]
        data.add_post(post)
    return render_template("upload.html")

