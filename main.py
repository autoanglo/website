from flask import Flask
from flask import render_template, redirect, url_for, request
from flask.ext.navigation import Navigation
from flask.ext.login import LoginManager, login_user, logout_user, UserMixin, login_required
from User import User
from PageManager import PageManager
from DatabaseWrapper import Data
from UsersDatabaseWrapper import UserData

import json

app = Flask(__name__)
app.config.update(SECRET_KEY = '541')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

#@login_manager.user_loader
#def load_user(user_id):
#    return users[0]

nav = Navigation(app)
nav.Bar('top', [nav.Item('Home', 'home'), nav.Item('Showcase', 'showcase')])


# def load_json(tag=None):
#     with open("data.json", "r") as f:
#         data = json.loads(f.read())
#     
#     result = []
#     if tag is not None:
#         for item in data:
#             if tag in item["tags"]:
#                 result.append(item)
#                 return result
#     else:
#         return data
#         
#     
# def get_post_by_id(id): 
#     data = load_json()
#     for post in data:
#         if int(post["id"]) == int(id):
#             return post

@login_manager.user_loader
def load_user(userid):
    return User(userid)
   


            
data = Data()
user_data = UserData()
#users = [User("1", "Me", "Me")]
page_size = 5

@app.route('/', defaults={'page': 1})
def main():
    return redirect("https://www.etsy.com/shop/EmilyLandBasics")


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

#@app.route('/showcase')
#def showcase():
#    data = load_json()
#    return render_template("gallery.html", name="A concept character for a new story.")

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
            users.append(new_user)
        for user in user_data.data:
            if user.is_username(username):
                if user.login_user(username, password):
                    load_user(user.id)
                    return render_template("upload.html")
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
        self.data.add_post(post)
        with open("data.json", "w+") as f:
            f.write(json.dumps(data))
    return render_template("upload.html")

