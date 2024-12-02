from flask import Blueprint, request, jsonify
from bson.objectid import ObjectId
from app import mongo

list_routes = Blueprint('list_routes', __name__)

# Create a new list in a board
@list_routes.post('/<board_id>/lists')
def create_list(board_id):
    data = request.json
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
@list_routes.get('/<board_id>/lists')
def get_lists_in_board(board_id):
    board = mongo.db.boards.find_one({'_id': ObjectId(board_id)})
    if not board:
        return jsonify({'error': 'Board not found'}), 404
    
    list_ids = board.get('lists', [])
    lists = list(mongo.db.lists.find({'_id': {'$in': [ObjectId(id) for id in list_ids]}}))
    for l in lists:
        l['_id'] = str(l['_id'])
    return jsonify(lists)

# Update a list's name
@list_routes.put('/<list_id>')
def update_list(list_id):
    data = request.json
    mongo.db.lists.update_one({'_id': ObjectId(list_id)}, {'$set': {'name': data['name']}})
    return jsonify({'message': 'List updated successfully'})

# Delete a list
@list_routes.delete('/<list_id>')
def delete_list(list_id):
    list_to_delete = mongo.db.lists.find_one({'_id': ObjectId(list_id)})
    if not list_to_delete:
        return jsonify({'error': 'List not found'}), 404
    
    # Remove list from its board
    mongo.db.boards.update_one(
        {'lists': str(list_id)},
        {'$pull': {'lists': str(list_id)}}
    )
    # Delete the list
    mongo.db.lists.delete_one({'_id': ObjectId(list_id)})
    return jsonify({'message': 'List deleted successfully'})
