import requests


class FakeDataLakeApi:
    def __init__(self, server: str) -> None:
        self.server = server
    
    def create(self, metadata: dict=None, b: bytes=None):
        if not metadata:
            metadata = {}
        response = requests.post(self.server + '/create', json=metadata)
        id = response.json()['id']
        if response.status_code == 200:
            if b:
                response = requests.put(self.server + '/upload/' + str(id), files={'file' : b})
            return id
        return None

    def read(self, id):
        response = requests.get(self.server + '/d/' + str(id))
        if response.status_code == 200:
            response_data = response.json()
            metadata = response_data['data']
            if response.status_code == 200:
                response = requests.get(self.server + '/download/' + str(id))
                if response.status_code == 200:
                    return metadata, response.content
                else:
                    return metadata, None
        return None, None
    
    def update(self, id, metadata: dict, b: bytes):
        response = requests.post(self.server + '/update/' + str(id), json=metadata)
        if response.status_code == 200:
            response = requests.put(self.server + '/upload/' + str(id), files={'file' : b})
            return response.status_code == 200
        return False


    def delete(self, id):
        response = requests.delete(self.server + '/delete/' + str(id))
        return response.status_code == 200
