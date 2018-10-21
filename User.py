try:
    from flask.ext.login import LoginManager, login_user, logout_user, UserMixin, login_required
except:
    from flask_login import LoginManager, login_user, logout_user, UserMixin, login_required

class User(UserMixin):
    def __init__(self, id, username=None, password=None):
        self.id = id
        self.name = str(username)
        self.password = str(password)
        
    def is_username(self, username):
        if self.name == username:
            return True
        else:
            return False
        
    def login_user(self, username, password):
        if (self.name == str(username)) and (self.password == str(password)):
            return True
        else:
            return False