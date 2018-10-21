import json

json_file = "user_data.json"

class UserData:
    def __init__(self):
        if not os.path.exists(data_file):
            self.data = []
        else:
            with open(json_file, "r") as f:
                self.data = json.loads(f.read())
        
    def add_user(self, user):
        self.data.append(user)
        with open(json_file, "w+") as f:
            f.write(json.dumps(self.data))
        