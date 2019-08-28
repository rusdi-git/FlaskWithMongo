from . import app,mongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify,request
import re

def check_date(date):
    date_format = '^[\d]{4}-[\d]{2}-[\d]{2} [\d]{2}:[\d]{2}$'
    return bool(re.match(date_format,date))

def post_artist(json):
    try:
        name = json['name']
        tanggal_lahir = json['tanggal_lahir']
        genre = json['genre']
        if not check_date(tanggal_lahir):
            resp = jsonify('Format {} salah, seharusnya, YYYY-MM-DD HH:MM'.format(tanggal_lahir))
            resp.status_code = 500
            return resp
        mongo.artist.insert({'name':name,'tanggal_lahir':tanggal_lahir,'genre':genre})
        resp = jsonify('Artist {} added successfully!'.format(name))
        resp.status_code = 200
        return resp
    except:
        resp = jsonify('Add Artist Process Failed')
        resp.status_code=500
        return resp

def put_artist(json):
    data = {}
    try:
        data['name'] = json['name']
    except KeyError:
        pass
    try:
        data['tanggal_lahir'] = json['tanggal_lahir']
    except KeyError:
        pass
    try:
        data['genre'] = json['genre']
    except KeyError:
        pass   
    if 'tanggal_lahir' in data.keys() and not check_date(data['tanggal_lahir']):
        resp = jsonify('Format {} salah, seharusnya, YYYY-MM-DD HH:MM'.format(data['tanggal_lahir']))
        resp.status_code = 500
        return resp
    elif data:
        id = json['_id']
        mongo.artist.update_one({'_id':ObjectId(id)},{'$set':{**data}})
        resp = jsonify('Artist with id {} updated successfully!'.format(id))
        resp.status_code = 200
        return resp
    else:
        return not_found()

def delete_artist(id):
    album = mongo.album.delete_many({'artist_id':id})
    mongo.artist.delete_one({'_id':ObjectId(id)})
    resp = jsonify('Artist with id {} and its album deleted successfully!'.format(id))
    resp.status_code = 200
    return resp

@app.route('/artist',methods=['GET','POST','PUT','DELETE'])
def artist(id=None):
    _json = request.json
    if _json and '_id' in _json.keys():
        if request.method=='DELETE':
            return delete_artist(_json['id'])
        elif request.method=='PUT':
            return put_artist(_json)
        else:
            artist = mongo.artist.find_one({'_id':ObjectId(_json['_id'])})
            resp = dumps(artist)
            return resp
    else:
        if request.method=='POST':
            return post_artist(_json)
        else:
            artist = mongo.artist.find()
            resp = dumps(artist)
            return resp

@app.route('/album')
@app.route('/artist/<id>/album')
def album(id=None):
    if id:
        album = mongo.album.find({'artist_id':id})
    else:
        album = mongo.album.find()
    resp = dumps(album)
    return resp

@app.route('/artist/<id>/add-album', methods=['POST'])
def add_album(id):
    _json = request.json
    name = _json['name']
    rilis = _json['rilis']
    tracks = _json['tracks']
    if name and rilis and tracks and request.method=='POST':
        mongo.album.insert({'name':name,'rilis':rilis,'tracks':tracks,'artist_id':id})
        resp = jsonify('Album {} added successfully to artist with id {}'.format(name,id))
        resp.status_code = 200
        return resp
    else:
        return not_found()

@app.route('/album/<id>/update',methods=['PUT'])
def update_album(id):
    _json = request.json
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
        data['tracks'] = _json['tracks']
    except KeyError:
        pass
    try:
        data['artist_id'] = _json['artist_id']
    except KeyError:
        pass
    if data and request.method=='PUT':
        mongo.album.update_one({'_id':ObjectId(id)},{'$set':{**data}})
        resp = jsonify('Album with id {} updated successfully!'.format(id))
        resp.status_code = 200
        return resp
    else:
        return not_found()

@app.route('/album/<id>/delete', methods=['DELETE'])
def delete_album(id):
    if request.method=='DELETE':
        mongo.album.delete_one({'_id':ObjectId(id)})
        resp = jsonify('Album with id {} deleted successfully!'.format(id))
        resp.status_code = 200
        return resp
    else:
        return not_found()

@app.route('/album/<id>')
def album_detail(id):
    album = mongo.album.find_one({'_id':ObjectId(id)})
    resp = dumps(album)
    return resp

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status':404,
        'message':'Not Found:'+request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp