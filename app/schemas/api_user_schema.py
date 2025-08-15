from marshmallow import Schema, fields, validate

class APIUserSchema(Schema):
    id = fields.String(dump_only=True)
    name = fields.String(required=True)
    api_key = fields.String(dump_only=True)
    role = fields.String(validate=validate.OneOf(["user", "admin"]))
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True) 