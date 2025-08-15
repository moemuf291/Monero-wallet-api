from marshmallow import Schema, fields

class EscrowTransactionSchema(Schema):
    id = fields.String(dump_only=True)
    buyer_id = fields.String(required=True)
    seller_id = fields.String(required=True)
    subaddress = fields.String(dump_only=True)
    amount = fields.Decimal(required=True, as_string=True)
    status = fields.String(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)