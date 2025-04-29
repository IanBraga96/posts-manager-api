from codeleap_careers.firebase_config import db
from datetime import datetime


def initialize_collections():
    """
    Initialize collections in Firebase if they don't exist
    """
    collections = ["post_likes", "post_comments"]

    for collection in collections:
        if not db.collection(collection).get():
            db.collection(collection).document("init").set(
                {"initialized": True, "created_at": datetime.now()}
            )
            print(f"collection {collection} initialized.")
