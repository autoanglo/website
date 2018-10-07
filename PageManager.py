class PageManager:
    def __init__(self, data, items_per_page=5, current_page=1):
        self.data = data
        self.items_per_page = items_per_page
        
        if current_page != 1:
            self.previouse_page = current_page - 1
            
        if len(data) > current_page * items_per_page:
            self.next_page = current_page + 1