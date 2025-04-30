from firebase_admin import auth
from codeleap_careers.firebase_config import db
from datetime import datetime


class User:
    def __init__(self, uid, name, email):
        self.uid = uid
        self.name = name
        self.email = email
        self.created_at = datetime.now()

    @staticmethod
    def create(name, email, password):
        try:
            user = auth.create_user(email=email, password=password, display_name=name)

            user_data = {"name": name, "email": email, "created_at": datetime.now()}

            db.collection("users").document(user.uid).set(user_data)

            return User(user.uid, name, email)
        except Exception as e:
            raise Exception(f"Error creating user: {str(e)}")

    @staticmethod
    def get_by_uid(uid):
        try:
            doc = db.collection("users").document(uid).get()
            if doc.exists:
                data = doc.to_dict()
                return User(uid, data["name"], data["email"])
            return None
        except Exception as e:
            raise Exception(f"Error fetching user: {str(e)}")
