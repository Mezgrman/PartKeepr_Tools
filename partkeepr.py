import json
import requests


class PartKeepr:
    def __init__(self, base_url, username, password):
        # base_url is something like https://my.partkeepr.host (no trailing slash)
        self.base_url = base_url
        self.session = requests.Session()
        self.session.auth = (username, password)
        self.user = self.login()
    
    def login(self):
        return self.session.post(self.base_url + "/api/users/login").json()
    
    def get(self, url):
        return self.session.get(self.base_url + url).json()
    
    def create(self, url, data):
        return self.session.post(self.base_url + url, json=data).json()
    
    def update(self, url, data):
        return self.session.put(self.base_url + url, json=data).json()
    
    def delete(self, url):
        self.session.delete(self.base_url + url)
    
    def upload(self, url, file):
        return self.session.post(self.base_url + url, files=file).json()
    
    def get_paged(self, url):
        result = []
        next_page = url
        while next_page:
            data = self.get(next_page)
            result.extend(data['hydra:member'])
            next_page = data.get('hydra:nextPage')
        return result
    
    def get_parts(self):
        return self.get_paged("/api/parts")
    
    def get_part(self, part_id):
        return self.get("/api/parts/{}".format(part_id))
    
    def get_manufacturers(self):
        return self.get_paged("/api/manufacturers")
    
    def get_storage_locations(self):
        return self.get_paged("/api/storage_locations")
    
    def create_manufacturer(self, manufacturer):
        return self.create("/api/manufacturers", manufacturer)
    
    def create_part_manufacturer(self, part_manufacturer):
        return self.create("/api/part_manufacturers", part_manufacturer)
    
    def create_storage_location(self, storage_location):
        return self.create("/api/storage_locations", storage_location)
    
    def update_part(self, part):
        return self.update(part['@id'], part)
    
    def update_part_manufacturer(self, part_manufacturer):
        return self.update(part_manufacturer['@id'], part_manufacturer)
    
    def update_part_distributor(self, part_distributor):
        return self.update(part_distributor['@id'], part_distributor)
    
    def upload_temp_file(self, file):
        return self.upload("/api/temp_uploaded_files/upload", {'userfile': file})
    
    def upload_temp_file_from_url(self, url):
        return self.create("/api/temp_uploaded_files/upload", {'url': url})
    
    def part_add_stock(self, part_id, quantity):
        return self.update(part_id + "/addStock", {'quantity': quantity})
    
    def part_remove_stock(self, part_id, quantity):
        return self.update(part_id + "/removeStock", {'quantity': quantity})
    
    def part_set_stock(self, part_id, quantity):
        return self.update(part_id + "/setStock", {'quantity': quantity})