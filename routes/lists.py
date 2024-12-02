from flask import Blueprint, request, jsonify
from bson.objectid import ObjectId
from marshmallow import ValidationError
from app import mongo
from schemas.list_schema import ListSchema

list_routes = Blueprint('list_routes', __name__)
list_schema = ListSchema()

@list_routes.post('/<board_id>/lists')
def create_list(board_id):
    try:
        data = list_schema.load(request.json)
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400
    
    board = mongo.db.boards.find_one({'_id': ObjectId(board_id)})
    if not board:
        return jsonify({'error': 'Board not found'}), 404
    
    new_list = {'name': data['name'], 'cards': []}
    result = mongo.db.lists.insert_one(new_list)
    list_id = str(result.inserted_id)
    
    mongo.db.boards.update_one(
        {'_id': ObjectId(board_id)},
        {'$push': {'lists': list_id}}
    )
    return jsonify({'id': list_id, 'name': data['name']})
