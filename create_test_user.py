import uuid
from app.app_factory import create_app
from app.extensions import db
from app.models.api_user import APIUser
from app.models.escrow_transaction import EscrowTransaction  # Ensure all models are imported

app = create_app()

with app.app_context():
    # Create all tables if they don't exist
    db.create_all()

    # Change these values as needed
    test_api_key = str(uuid.uuid4())
    test_user = APIUser(
        name="testuser",
        api_key=test_api_key,
        role="admin"  # or "user"
    )
    db.session.add(test_user)
    db.session.commit()
    print(f"Created test user with API key: {test_api_key}")