import json
import os

from User import User

json_file = "user_data.json"

class UserData:
    def __init__(self):
        self.data = []
        if os.path.exists(json_file):
            with open(json_file, "r") as f:
                for user in json.loads(f.read()):
                    self.data.append(User(user["id"], user["username"], user["password"]))
        
    def add_user(self, user):
        self.data.append(user)
        with open(json_file, "w+") as f:
            for user in self.data:
                f.write(json.dumps(user.get_dict()))
                
    def get_user_by_id(self, id):
        for user in self.data:
            if user.id == id:
                return user
            
        return None
        