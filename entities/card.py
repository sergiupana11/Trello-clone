from marshmallow import Schema, fields

class CardEntity:
    def __init__(self, title, description):
        self.title = title
        self.description = description