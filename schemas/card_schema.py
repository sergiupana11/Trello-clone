from marshmallow import Schema, fields, validate

class CardSchema(Schema):
    title = fields.String(required=True, validate=validate.Length(min=1, max=100))
    description = fields.String(required=False, allow_none=True, validate=validate.Length(max=500))