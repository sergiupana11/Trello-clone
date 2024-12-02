from flask import Blueprint, request, jsonify
from bson.objectid import ObjectId
from extensions import mongo
from schemas.list_schema import ListSchema
from schemas.card_schema import CardSchema
from marshmallow import ValidationError

list_routes = Blueprint('list_routes', __name__)
list_schema = ListSchema()
card_schema = CardSchema()

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

# Create a new card in a list
@list_routes.post('/<list_id>/cards')
def create_card(list_id):
    data = request.json
    try:
        data = card_schema.load(request.json)
    except ValidationError as err:
        return jsonify({'errors': err.message})
    
    card_list = mongo.db.lists.find_one({'_id': ObjectId(list_id)})
    if not card_list:
        return jsonify({'error': 'List not found'}), 404
    
    new_card = {'title': data['title'], 'description': data.get('description', ''), 'list_id': list_id}
    result = mongo.db.cards.insert_one(new_card)
    card_id = str(result.inserted_id)
    
    mongo.db.lists.update_one(
        {'_id': ObjectId(list_id)},
        {'$push': {'cards': card_id}}
    )
    return jsonify({'id': card_id, 'title': data['title'], 'description': data.get('description', '')})

# Get all cards in a list
@list_routes.get('/<list_id>/cards')
def get_cards_in_list(list_id):
    card_list = mongo.db.lists.find_one({'_id': ObjectId(list_id)})
    if not card_list:
        return jsonify({'error': 'List not found'}), 404
    
    card_ids = card_list.get('cards', [])
    cards = list(mongo.db.cards.find({'_id': {'$in': [ObjectId(id) for id in card_ids]}}))
    for card in cards:
        card['_id'] = str(card['_id'])
    return jsonify(cards)
