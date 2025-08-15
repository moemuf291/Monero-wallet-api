import uuid
from datetime import datetime
from ..extensions import db

class EscrowTransaction(db.Model):
    __tablename__ = 'escrow_transactions'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    buyer_id = db.Column(db.String(128), nullable=False)
    seller_id = db.Column(db.String(128), nullable=False)
    subaddress = db.Column(db.String(128), nullable=False)
    amount = db.Column(db.Numeric(18, 12), nullable=False)
    status = db.Column(db.Enum('waiting_payment', 'funded', 'completed', 'refunded', name='escrow_status'), nullable=False, default='waiting_payment')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)