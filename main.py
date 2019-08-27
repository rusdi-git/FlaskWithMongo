from .app import app,mongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify,request

@app.route('/artist')
def artist():
    artist = mongo.artist.find()
    resp = dumps(artist)
    return resp

@app.route('/add-artist',methods=['POST'])
def add_artist():
    _json = request.json
    id = _json['name']
    name = _json['name']
    tanggal_lahir = _json['tanggal_lahir']
    genre = _json['genre']

    if name and tanggal_lahir and genre and request.method=='POST':
        mongo.artist.insert({'_id':id,'name':name,'tanggal_lahir':tanggal_lahir,'genre':genre})
        resp = jsonify('Artist added successfully!')
        resp.status_code = 200
        return resp
    else:
        return not_found()

@app.route('/artist/<id>')
def artist_detail(id):
    art = mongo.artist.find_one({'_id':id})
    resp = dumps(art)
    return resp

@app.route('/update-artist', methods=['PUT'])
def update_artist():
    _json = request.json
    _id = _json['_id']
    data = {}
    try:
        data['name'] = _json['name']
    except KeyError:
        pass
    try:
        data['tanggal_lahir'] = _json['tanggal_lahir']
    except KeyError:
        pass
    try:
        data['genre'] = _json['genre']
    except KeyError:
        pass
    if _id and data and request.method=='PUT':
        mongo.artist.update_one({'_id':_id},{'$set':{**data}})
        resp = jsonify('Artist updated successfully!')
        resp.status_code = 200
        return resp
    else:
        return not_found()

@app.route('/delete-artist',methods=['DELETE'])
def delete_artist():
    _json = request.json
    _id = _json['_id']
    if _id and request.method=='DELETE':
        mongo.artist.delete_one({'_id':_id})
        resp = jsonify('Artist deleted successfully!')
        resp.status_code = 200
        return resp
    else:
        return not_found()

@app.route('/album')
def album():
    album = mongo.album.find()
    resp = dumps(album)
    return resp

@app.route('/add-album', methods=['POST'])
def add_album():
    _json = request.json
    _id = _json['_id']
    name = _json['name']
    rilis = _json['rilis']
    tracks = _json['tracks']
    artist_id = _json['artist_id']
    if _id and name and rilis and tracks and artist_id and request.method=='DELETE':
        mongo.album.insert({'_id':_id,'name':name,'rilis':rilis,'tracks':tracks,'artist_id':artist_id})
        resp = jsonify('Album added successfully')
        resp.status_code = 200
        return resp
    else:
        return not_found()

@app.route('/update-album',methods=['PUT'])
def update_albm():
    _json = request.json
    _id = _json['_id']
    data = {}
    try:
        data['name'] = _json['name']
    except KeyError:
        pass
    try:
        data['rilis'] = _json['rilis']
    except KeyError:
        pass
    try:
        data['genre'] = _json['genre']
    except KeyError:
        pass


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status':404,
        'message':'Not Found:'+request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp