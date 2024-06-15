import uuid

class FakeDataLake:
    def __init__(self) -> None:
        self.d = {}
        self.blobs = {}
    
    def create(self, doc: dict):
        id = str(uuid.uuid4())
        self.d[id] = doc
        return id
    
    def read(self, id: str):
        return self.d.get(id, None)
    
    def update(self, id: str, doc: dict):
        if id in self.d:
            self.d[id] = doc
            return True
        else:
            return False
    
    def delete(self, id: str):
        if id in self.d:
            del self.d[id]
            if id in self.blobs:
                del self.blobs[id]
            return True
        else:
            return False
    
    def list(self):
        return list(self.d.keys())
    
    def get_blob(self, id):
        return self.blobs.get(id, None)
    
    def put_blob(self, id, blob):
        if id in self.d:
            self.blobs[id] = blob
            return True
        else:
            return False
