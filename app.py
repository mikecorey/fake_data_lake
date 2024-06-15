from io import BytesIO
from flask import Flask, request, jsonify, send_file

from fake_data_lake import FakeDataLake

app = Flask(__name__)

fdl = FakeDataLake()


@app.route('/')
def index():
    s = "<HTML><BODY>"
    s += "<h1>Fake Data Lake</h1>"
    for key in fdl.list():
        s += "<a href='/d/" + key + "'>" + key + "</a><br>"
    s += "</BODY></HTML>"
    return s


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
