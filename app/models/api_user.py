import uuid
from datetime import datetime
from ..extensions import db

class APIUser(db.Model):
    __tablename__ = 'api_users'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(128), nullable=False)
    api_key = db.Column(db.String(128), unique=True, nullable=False)
    role = db.Column(db.Enum('user', 'admin', name='user_role'), nullable=False, default='user')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow) 