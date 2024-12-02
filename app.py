from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.config['MONGO_URI'] = "mongodb://localhost:27017/myDatabase"
mongo = PyMongo(app)

@app.post('/boards')
def create_board():
    request_body = request.json
    id = mongo.db.boards.insert_one({'name': request_body['name'], 'card_lists': []})
    return jsonify({'id': str(id.inserted_id)})

@app.get('/boards/<id>')
def get_board(id):
    board = mongo.db.boards.find_one({'_id': ObjectId(id)})
    if board is None:
        return jsonify({'error': 'Board not found'}), 404
    board['_id'] = str(board['_id'])
    return jsonify(board)

@app.get('/boards')
def get_all_boards():
    boards = mongo.db.boards.find()
    result = []
    for board in boards:
        board['_id'] = str(board['_id'])
        result.append(board)
    return result

@app.post('/boards/<board_id>/lists')
def create_card_for_board(board_id):
    board = mongo.db.boards.find_one({'_id': ObjectId(board_id)})
    if board is None:
        return jsonify({'errror': 'Board not found'}), 404
    request_body = request.json
    list = {'title': request_body['name'], 'card_lists': []}
    

if __name__ == '__main__':
    app.run(debug=True)