from flask import Blueprint, request, jsonify
from bson.objectid import ObjectId
from extensions import mongo
from schemas.board_schema import BoardSchema
from schemas.list_schema import ListSchema
from marshmallow import ValidationError

board_routes = Blueprint('board_routes', __name__)
board_schema = BoardSchema()
list_schema = ListSchema()

@board_routes.post('/')
def create_board():
    try:
        data = board_schema.load(request.json)
    except ValidationError as err:
        return jsonify({'errors': err.message})
    result = mongo.db.boards.insert_one({'name': data['name'], 'lists': []})
    return jsonify({'id': str(result.inserted_id)})

@board_routes.get('/')
def get_all_boards():
    boards = list(mongo.db.boards.find())
    for board in boards:
        board['_id'] = str(board['_id'])
        # Retrieve list names for the current board
        list_ids = board.get('lists', [])
        lists = list(mongo.db.lists.find({'_id': {'$in': [ObjectId(list_id) for list_id in list_ids]}}))
        for lst in lists:
            lst['_id'] = str(lst['_id'])  # Convert ObjectId to string
        board['lists'] = [{'id': lst['_id'], 'name': lst['name']} for lst in lists]  # Include names and IDs
    return jsonify(boards)

@board_routes.get('/<board_id>')
def get_board(board_id):
    # Find the board by ID
    board = mongo.db.boards.find_one({'_id': ObjectId(board_id)})
    if not board:
        return jsonify({'error': 'Board not found'}), 404

    # Convert board ID to string
    board['_id'] = str(board['_id'])

    # Retrieve associated lists
    list_ids = board.get('lists', [])
    lists = list(mongo.db.lists.find({'_id': {'$in': [ObjectId(list_id) for list_id in list_ids]}}))
    for lst in lists:
        lst['_id'] = str(lst['_id'])  # Convert ObjectId to string

    # Replace list IDs with list details
    board['lists'] = [{'id': lst['_id'], 'name': lst['name']} for lst in lists]

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

# Create a new list in a board
@board_routes.post('/<board_id>/lists')
def create_list(board_id):
    try:
        data = list_schema.load(request.json)
    except ValidationError as err:
        return jsonify({'errors': err.message})
    
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

# Get all lists in a board
@board_routes.get('/<board_id>/lists')
def get_lists_in_board(board_id):
    board = mongo.db.boards.find_one({'_id': ObjectId(board_id)})
    if not board:
        return jsonify({'error': 'Board not found'}), 404
    
    list_ids = board.get('lists', [])
    lists = list(mongo.db.lists.find({'_id': {'$in': [ObjectId(id) for id in list_ids]}}))
    for l in lists:
        l['_id'] = str(l['_id'])
    return jsonify(lists)
