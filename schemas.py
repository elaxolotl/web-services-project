from marshmallow import Schema, fields, validate, ValidationError, pre_load

def validate_status(value):
    allowed_statuses = ["detained","on_sale", "sold", "no_commercial_value"]
    if value not in allowed_statuses:
        raise ValidationError(f"Invalid status. Allowed values are: {', '.join(allowed_statuses)}.")

class GoodSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    container_id = fields.Str(required=True)
    opening_price = fields.Float(required=True)
    status = fields.Str(required=True, validate=validate_status)
    guarantee = fields.Float(required=True)
    description = fields.Str(missing=None)
    category = fields.Str(missing=None)
    manufacturer_details = fields.Str(missing=None)
    reason_for_detention = fields.Str(missing=None)
    store = fields.Str(missing=None)
    perishable = fields.Bool(required=True)
    expiry_date = fields.Date(missing=None, allow_none=True)
    created_at = fields.DateTime(dump_only=True, timezone=True)
    due_date = fields.DateTime(missing=None, allow_none=True, timezone=True)
    customs_officer_id = fields.Int()
    winner_id = fields.Int(missing=None, allow_none=True)

    
class UserSignupSchema(Schema):
    email = fields.Email(required=True, validate=validate.Length(min=1))
    password = fields.Str(required=True, validate=validate.Length(min=6))
    role_id = fields.Int(required=True, validate=validate.OneOf([1, 2, 3]))
    name = fields.Str(required=True)
    buyer_type = fields.Str(missing=None, validate=validate.OneOf(["individual", "company"]))
    id_value = fields.Str(missing=None, validate=validate.Length(equal=8))
    fs_uniquifier = fields.Str(dump_only=True)
    
    @pre_load
    def validate_id_for_role(self, data, **kwargs):
        if data.get("role_id") == 2:
            if not data.get("id_value"):
                raise ValidationError("Please provide a national ID or a fiscal ID for role_id 2.", field_name="id_value")
            if not data.get("buyer_type"):
                raise ValidationError("Please provide a buyer type for role_id 2.", field_name="buyer_type")
        return data
    
class UserLoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)
    
class BidSchema(Schema):
    value = fields.Float(required=True)