from marshmallow import Schema, fields, validate


class RegisterSchema(Schema):
    email = fields.Email(required=True, validate=validate.Email())
    password = fields.Str(required=True, validate=validate.Length(min=6))
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    phone_number = fields.Str(required=True)
    space_type = fields.Str(required=True, validate=validate.OneOf(['executor', 'customer']))
