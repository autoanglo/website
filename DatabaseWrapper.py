import json


class Data:
    def __init__(self, tag=None):
        with open("data.json", "r") as f:
            self.data = json.loads(f.read())
            self.data.reverse()
        
        max_id = 0
        for post in self.data:
            if post["id"] > max_id:
                max_id = post["id"]
                
        self._cur_id = max_id
        
    def _id(self):
        self._cur_id = self._cur_id + 1
        return seld._cur_id
    
    def get_posts_by_tag(self, tag):
        result = []
        if tag is not None:
            for item in self.data:
                if tag in item["tags"]:
                    result.append(item)
                    return result
        else:
            return data
    
    def add_post(self, post):
        post["id"] = self._id()
        self.data.append(post)
        with open("data.json", "w+") as f:
            f.write(json.dumps(data))

    def get_post_by_id(self, id):
        for post in self.data:
            if int(post["id"]) == int(id):
                return post
        
    def delete_post_by_id(self, id):
        post = self.get_post_by_id(id)
        self.data.remove(post)
        with open("data.json", "w+") as f:
            f.write(json.dumps(self.data))
    
    def edit_post_id(self, id):
        pass