from marshmallow import Schema, fields

class BoardEntity:
    def __init__(self, name, card_lists=None):
        self.name = name
        self.card_lists = card_lists

