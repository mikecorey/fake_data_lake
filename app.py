from io import BytesIO
import datetime
from functools import wraps

from flask import Flask, request, jsonify, send_file, make_response
import jwt

from fake_data_lake import FakeDataLake

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mah_seekrit'

fdl = FakeDataLake()


def require_auth(role=None):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = request.headers.get('Authorization').split()[1]
            if not token:
                return jsonify({'error': 'Missing authorization header.'}), 401
            try:
                payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
                if role and role not in payload['roles']:
                    return jsonify({'error': 'Not Authorized. (lacking role.)'}), 401
            except Exception as e:
                print(e)
                return jsonify({'error': 'Invalid token.'}), 401
            return f(*args, **kwargs)
        return wrapper
    return decorator


@app.route('/')
def index():
    s = "<HTML><BODY>"
    s += "<h1>Fake Data Lake</h1>"
    for key in fdl.list():
        s += "<a href='/d/" + key + "'>" + key + "</a><br>"
    s += "</BODY></HTML>"
    return s

@app.route('/login')
def login():
    auth = request.authorization
    if auth and auth.username == 'admin' and auth.password == 'secret':
        print(app.config['SECRET_KEY'])
        payload = {
            'user': auth.username,
            'roles': ['king', 'space_janitor'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
        }
        token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({'token': token})
    return make_response('Bad username or password.', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})


@app.route('/seekrit')
@require_auth(None)
def seekrit():
    return "You are in the seekrit area."


@app.route('/space_janitors_only')
@require_auth('space_janitor')
def space_janitors_only():
    return "Roger Wilco."


@app.route('/create', methods=['POST'])
def create():
    id = fdl.create(request.json)
    return jsonify({'result': 'ok', 'id': id})

@app.route('/upload/<id>', methods=['PUT'])
def upload(id):
    fdl.put_blob(id, request.files['file'].read())
    return jsonify({'result': 'ok', 'id': id})

@app.route('/d/<id>')
def read(id):
    data = fdl.read(id)
    if data is None:
        return jsonify({'result': 'not found', 'id': id}), 404
    else:
        return jsonify({'result': 'ok', 'data': data})

@app.route('/download/<id>')
def download(id):
    dat = fdl.get_blob(id)
    return send_file(BytesIO(dat), download_name=id, as_attachment=True )

@app.route('/update/<id>', methods=['POST'])
def update(id):
    res = fdl.update(id, request.json)
    if res:
        return jsonify({'result': 'ok'})
    else:
        return jsonify({'result': 'not found'}), 404

@app.route('/delete/<id>', methods=['DELETE'])
def delete(id):
    res = fdl.delete(id)
    if res:
        return jsonify({'result': 'ok'})
    else:
        return jsonify({'result': 'not found'}), 404

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

