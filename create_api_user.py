import uuid
import sys
from app.app_factory import create_app
from app.extensions import db
from app.models.api_user import APIUser

def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("user", "admin"):
        print("Usage: python create_api_user.py [user|admin] [optional: name]")
        sys.exit(1)

    role = sys.argv[1]
    name = sys.argv[2] if len(sys.argv) > 2 else f"{role}user"

    app = create_app()
    with app.app_context():
        api_key = str(uuid.uuid4())
        user = APIUser(
            name=name,
            api_key=api_key,
            role=role
        )
        db.session.add(user)
        db.session.commit()
        print(f"Created {role} user '{name}' with API key: {api_key}")

if __name__ == "__main__":
    main()