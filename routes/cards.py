from flask import Blueprint, request, jsonify
from bson.objectid import ObjectId
from app import mongo

card_routes = Blueprint('card_routes', __name__)

# Create a new card in a list
@card_routes.post('/<list_id>/cards')
def create_card(list_id):
    data = request.json
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
@card_routes.get('/<list_id>/cards')
def get_cards_in_list(list_id):
    card_list = mongo.db.lists.find_one({'_id': ObjectId(list_id)})
    if not card_list:
        return jsonify({'error': 'List not found'}), 404
    
    card_ids = card_list.get('cards', [])
    cards = list(mongo.db.cards.find({'_id': {'$in': [ObjectId(id) for id in card_ids]}}))
    for card in cards:
        card['_id'] = str(card['_id'])
    return jsonify(cards)

# Get details of a card
@card_routes.get('/<card_id>')
def get_card(card_id):
    card = mongo.db.cards.find_one({'_id': ObjectId(card_id)})
    if not card:
        return jsonify({'error': 'Card not found'}), 404
    card['_id'] = str(card['_id'])
    return jsonify(card)

# Update a card's title and/or description
@card_routes.put('/<card_id>')
def update_card(card_id):
    data = request.json
    updates = {}
    if 'title' in data:
        updates['title'] = data['title']
    if 'description' in data:
        updates['description'] = data['description']
    
    mongo.db.cards.update_one({'_id': ObjectId(card_id)}, {'$set': updates})
    return jsonify({'message': 'Card updated successfully'})

# Delete a card
@card_routes.delete('/<card_id>')
def delete_card(card_id):
    card = mongo.db.cards.find_one({'_id': ObjectId(card_id)})
    if not card:
        return jsonify({'error': 'Card not found'}), 404
    
    # Remove card from its list
    mongo.db.lists.update_one(
        {'cards': str(card_id)},
        {'$pull': {'cards': str(card_id)}}
    )
    # Delete the card
    mongo.db.cards.delete_one({'_id': ObjectId(card_id)})
    return jsonify({'message': 'Card deleted successfully'})
