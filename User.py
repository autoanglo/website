from flask.ext.login import LoginManager, login_user, logout_user, UserMixin, login_required

class User(UserMixin):
    def __init__(self, id, username=None, password=None):
        self.id = id
        try:
            self.name = username
            self.password = password
        except:
            pass
        
        
    def is_username(self, username):
        if self.name == username:
            return True
        else:
            return False
        
    def login_user(self, username, password):
        if (self.name == username) and (self.password == password):
            return True
        else:
            return False