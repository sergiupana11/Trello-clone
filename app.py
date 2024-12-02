from flask import Flask, jsonify
from flask_pymongo import PyMongo
from marshmallow import ValidationError
from routes.boards import board_routes
from routes.lists import list_routes
from routes.cards import card_routes

app = Flask(__name__)
app.config['MONGO_URI'] = "mongodb://localhost:27017/trello_clone"
mongo = PyMongo(app)

# Register blueprints
app.register_blueprint(board_routes, url_prefix='/boards')
app.register_blueprint(list_routes, url_prefix='/lists')
app.register_blueprint(card_routes, url_prefix='/cards')

# Global error handler for Marshmallow validation errors
@app.errorhandler(ValidationError)
def handle_validation_error(err):
    return jsonify({'errors': err.messages}), 400

if __name__ == '__main__':
    app.run(debug=True)
