from . import app,mongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify,request
import re

date_format = '^[\d]{4}-[\d]{2}-[\d]{2} [\d]{2}:[\d]{2}$'

@app.route('/artist')
@app.route('/artist/<id>')
def artist(id=None, methods=['GET','POST','PUT','DELETE']):
    # genre = request.args.get('genre')
    # if genre:
    #     artist = mongo.artist.find({'genre':genre})
    # elif id:
    #     artist = mongo.artist.find_one({'_id':ObjectId(id)})
    # else:
    #     artist = mongo.artist.find()
    if id:
        artist_id = ObjectId(id)
        if request.method!='GET':
            _json = request.json
            data = {}
            try:
                data['name'] = _json['name']
            except KeyError:
                pass
            try:
                data['tanggal_lahir'] = _json['tanggal_lahir']
                if not re.match(date_format,data['tanggal_lahir']):
                    resp = jsonify('Format {} salah, seharusnya, YYYY-MM-DD HH:MM'.format(data['tanggal_lahir']))
                    resp.status_code = 500
                    return resp
            except KeyError:
                pass
            try:
                data['genre'] = _json['genre']
            except KeyError:
                pass
        else:
            mongo.artist.find_one({'_id':artist_id})
    else:
        if request.method=='POST':
            _json = request.json
            name = _json['name']
            tanggal_lahir = _json['tanggal_lahir']
            genre = _json['genre']
            mongo.artist.insert({'name':name,'tanggal_lahir':tanggal_lahir,'genre':genre})
            resp = jsonify('Artist {} added successfully!'.format(name))
            resp.status_code = 200
            return resp
        else:
            artist = mongo.artist.find()
    resp = dumps(artist)
    return resp

@app.route('/add-artist',methods=['POST'])
def add_artist():
    _json = request.json
    name = _json['name']
    tanggal_lahir = _json['tanggal_lahir']
    genre = _json['genre']

    #validate date format
    if not re.match(date_format,tanggal_lahir):
        resp = jsonify('Format {} salah, seharusnya, YYYY-MM-DD HH:MM'.format(tanggal_lahir))
        resp.status_code = 500
        return resp

    if name and tanggal_lahir and genre and request.method=='POST':
        mongo.artist.insert({'name':name,'tanggal_lahir':tanggal_lahir,'genre':genre})
        resp = jsonify('Artist {} added successfully!'.format(name))
        resp.status_code = 200
        return resp
    else:
        return not_found()

@app.route('/artist/<id>/update', methods=['PUT'])
def update_artist(id):
    _json = request.json
    data = {}
    try:
        data['name'] = _json['name']
    except KeyError:
        pass
    try:
        data['tanggal_lahir'] = _json['tanggal_lahir']
        if not re.match(date_format,data['tanggal_lahir']):
            resp = jsonify('Format {} salah, seharusnya, YYYY-MM-DD HH:MM'.format(data['tanggal_lahir']))
            resp.status_code = 500
            return resp
    except KeyError:
        pass
    try:
        data['genre'] = _json['genre']
    except KeyError:
        pass
    if data and request.method=='PUT':
        mongo.artist.update_one({'_id':ObjectId(id)},{'$set':{**data}})
        resp = jsonify('Artist with id {} updated successfully!'.format(id))
        resp.status_code = 200
        return resp
    else:
        return not_found()

@app.route('/artist/<id>/delete',methods=['DELETE'])
def delete_artist(id):
    if request.method=='DELETE':
        album = mongo.album.delete_many({'artist_id':ObjectId(id)})
        mongo.artist.delete_one({'_id':ObjectId(id)})
        resp = jsonify('Artist with id {} and its album deleted successfully!'.format(id))
        resp.status_code = 200
        return resp
    else:
        return not_found()

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