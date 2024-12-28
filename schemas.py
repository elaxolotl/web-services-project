from marshmallow import Schema, fields
class PlainGoodschema(Schema):
    good_id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    opening_price = fields.Int(required=True)