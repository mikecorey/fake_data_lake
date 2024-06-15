import requests
import random
import os

server = "http://127.0.0.1:5000"

# Create object
data = [
    {'name': 'mike', 'emoji': '🤡'},
    {'name': 'john', 'emoji': '😎', 'number': 44},
    {'name': 'bob', 'emoji': '👻', 'car': 'volvo'}
]

# Create tests
print("Testing Create")
created_docs = {}
for d in data:
    Response = requests.post(server + '/create', json=d)
    response_data = Response.json()
    created_docs[response_data['id']] = {'json': d}
    assert Response.status_code == 200
    assert response_data['result'] == 'ok'

assert len(created_docs.items()) == len(data)

print("success")


# Read tests
print("Testing Read")
for id in created_docs:
    Response = requests.get(server + '/d/' + str(id))
    response_data = Response.json()
    assert Response.status_code == 200
    assert response_data['result'] == 'ok'
    assert response_data['data'] == created_docs[id]['json']

print("Success")

# Test Put
print("Testing Put blob")
for id in created_docs:
    b = os.urandom(random.randint(1024, 4096))
    created_docs[id]['blob'] = b
    Response = requests.put(server + '/upload/' + str(id), files={'file' : b})
    response_data = Response.json()
    assert Response.status_code == 200
    assert response_data['result'] == 'ok'

print("Success")

# Test Get blob
print("Testing Get blob")
for id in created_docs:
    Response = requests.get(server + '/download/' + str(id))
    response_data = Response.content
    assert Response.status_code == 200
    assert response_data == created_docs[id]['blob']

print('Success')

# Test Delete

print("Testing Update")

delete_me = {'name': 'deleteme', 'emoji': '🔥', 'car': 'bike'}
updated_me = {'name': 'updated', 'emoji': '🌴'}

Response = requests.post(server + '/create', json=delete_me)
response_data = Response.json()
id = response_data['id']


Response = requests.post(server + '/update/' + str(id), json=updated_me)
assert Response.status_code == 200
assert Response.json()['result'] == 'ok'
Response = requests.get(server + '/d/' + str(id))
response_data = Response.json()
assert Response.status_code == 200
assert response_data['data'] == updated_me

print("success")

print('Testing delete')

Response = requests.delete(server + '/delete/' + str(id))
response_data = Response.json()
assert Response.status_code == 200
assert response_data['result'] == 'ok'

Response = requests.get(server + '/d/' + str(id))
response_data = Response.json()
assert Response.status_code == 404

print('Success')
