from flask import Flask
from flask import render_template, redirect, url_for, request
from flask_navigation import Navigation
from flask_login import LoginManager, login_user, logout_user, UserMixin, login_required
import json

from User import User
from PageManager import PageManager
from DatabaseWrapper import Data
from UsersDatabaseWrapper import UserData

class Website(UserMixin):
    def __init__(self):
        self.data = Data()
        self.user_data = UserData()
        self.page_size = 5

        
    def galery_with_tag(self, page, tag=None): 
        if tag:
            data2 = self.data.get_posts_by_tag("showcase")
        else:
            data2 = self.data.data
        lower_index = self.page_size * page - self.page_size
        upper_index = self.page_size * page
        page_manager = PageManager(data2, self.page_size, page)
        return render_template("home.html", data=data2[lower_index:upper_index], pages=page_manager)
    
    def redirect_to(self, destination):
        return redirect(destination)
    
    def render_template(self, template):
        return render_template(template)

    def delete_post(self, post_id):
        self.data.delete_post_by_id(post_id)
        #return_url = request.referrer
        return self.redirect_to("/")
    
    def login_user(self, request):
        logged_in_user = None
        username = request.form['username']
        password = request.form['password']
        
        # This is a hacky way to add a user on the first start up of the site.
        if len(self.user_data.data) < 1:
            new_user=User(0, username, password)
            self.user_data.add_user(new_user)
            
        for user in self.user_data.data:
            if user.is_username(username):
                if user.login_user(username, password):
                    logged_in_user = user
                    break
        return logged_in_user
    
    def upload_post(self, request):
        post = {}
        post["title"] = request.form["title"]
        post["link"] = request.form["link"]
        post["description"] = request.form["description"]
        post["tags"] = request.form["tags"]
        self.data.add_post(post)
        return render_template("upload.html")