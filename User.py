from flask_login import LoginManager, login_user, logout_user, UserMixin, login_required

class User(UserMixin):
    def __init__(self, id, username=None, password=None):
        self.id = id
        self.name = str(username)
        self.password = str(password)
        self.authenticated = False
        
    def get_dict(self):
        return {"id":self.id, "username":self.name, "password":self.password}
        
    def is_username(self, username):
        if self.name == username:
            return True
        else:
            return False
        
    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated
    
    def login_user(self, username, password):
        if (self.name == str(username)) and (self.password == str(password)):
            self.authenticated = True
        else:
            self.authenticated = False
            
        return self.authenticated
    
    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False
    
    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.id
    
    def is_active(self):
        """True, as all users are active."""
        return True