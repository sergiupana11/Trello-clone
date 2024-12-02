from marshmallow import Schema, fields, validate

class ListSchema(Schema):
    name = fields.String(required=True, validate=validate.Length(min=1, max=100))