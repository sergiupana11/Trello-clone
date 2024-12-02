from flask import Blueprint, request, jsonify
from bson.objectid import ObjectId
from extensions import mongo
from schemas.card_schema import CardSchema
from marshmallow import ValidationError

card_routes = Blueprint('card_routes', __name__)
card_schema = CardSchema()

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
