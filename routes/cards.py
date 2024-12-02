from flask import Blueprint, request, jsonify
from bson.objectid import ObjectId
from marshmallow import ValidationError
from app import mongo
from schemas.card_schema import CardSchema

card_routes = Blueprint('card_routes', __name__)
card_schema = CardSchema()

@card_routes.post('/<list_id>/cards')
def create_card(list_id):
    try:
        data = card_schema.load(request.json)
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400
    
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
