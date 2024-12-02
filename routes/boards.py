from flask import Blueprint, request, jsonify
from bson.objectid import ObjectId
from app import mongo

board_routes = Blueprint('board_routes', __name__)

@board_routes.post('/')
def create_board():
    data = request.json
    result = mongo.db.boards.insert_one({'name': data['name'], 'lists': []})
    return jsonify({'id': str(result.inserted_id)})

@board_routes.get('/')
def get_all_boards():
    boards = list(mongo.db.boards.find())
    for board in boards:
        board['_id'] = str(board['_id'])
    return jsonify(boards)

@board_routes.get('/<board_id>')
def get_board(board_id):
    board = mongo.db.boards.find_one({'_id': ObjectId(board_id)})
    if not board:
        return jsonify({'error': 'Board not found'}), 404
    board['_id'] = str(board['_id'])
    return jsonify(board)

@board_routes.put('/<board_id>')
def update_board(board_id):
    data = request.json
    mongo.db.boards.update_one({'_id': ObjectId(board_id)}, {'$set': {'name': data['name']}})
    return jsonify({'message': 'Board updated successfully'})

@board_routes.delete('/<board_id>')
def delete_board(board_id):
    mongo.db.boards.delete_one({'_id': ObjectId(board_id)})
    return jsonify({'message': 'Board deleted successfully'})
