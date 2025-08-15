import uuid
from app.app_factory import create_app
from app.extensions import db
from app.models.api_user import APIUser

app = create_app()

with app.app_context():
    admin_api_key = str(uuid.uuid4())
    admin_user = APIUser(
        name="adminuser",
        api_key=admin_api_key,
        role="admin"
    )
    db.session.add(admin_user)
    db.session.commit()
    print(f"Created admin user with API key: {admin_api_key}")