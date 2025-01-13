from marshmallow import Schema, fields, validate, ValidationError

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
    created_at = fields.DateTime(dump_only=True)
    due_date = fields.DateTime(missing=None, allow_none=True)
    customs_officer_id = fields.Int(required=True)
    winner_id = fields.Int(missing=None, allow_none=True)

    
class UserSignupSchema(Schema):
    email = fields.Email(required=True, validate=validate.Length(min=1))
    password = fields.Str(required=True, validate=validate.Length(min=6))
    role_id = fields.Int(required=True)
    name = fields.Str(required=True)
    national_id = fields.Str(missing=None, validate=validate.Length(equal=8))
    fiscal_id = fields.Str(missing=None, validate=validate.Regexp(
            r'^\d{7}[A-Z]$', 
            error="Fiscal ID must be 7 digits followed by an uppercase letter (e.g., 0000000A)."
        ))
    fs_uniquifier = fields.Str(dump_only=True)
    
class UserLoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)
    
class BidSchema(Schema):
    value = fields.Float(required=True)