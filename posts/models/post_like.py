from datetime import datetime
from codeleap_careers.firebase_config import db


class PostLike:
    def __init__(self, post_id, user_id, created_at=None):
        self.post_id = post_id
        self.user_id = user_id
        self.created_at = created_at or datetime.now()

    @staticmethod
    def create(post_id, user_id):
        like = PostLike(post_id, user_id)
        doc_ref = db.collection("post_likes").document(f"{post_id}_{user_id}")
        doc_ref.set(
            {"post_id": post_id, "user_id": user_id, "created_at": like.created_at}
        )
        return like

    @staticmethod
    def get(post_id, user_id):
        doc_ref = db.collection("post_likes").document(f"{post_id}_{user_id}")
        doc = doc_ref.get()
        if doc.exists:
            data = doc.to_dict()
            return PostLike(data["post_id"], data["user_id"], data["created_at"])
        return None

    @staticmethod
    def delete(post_id, user_id):
        doc_ref = db.collection("post_likes").document(f"{post_id}_{user_id}")
        doc_ref.delete()

    @staticmethod
    def list_by_post(post_id):
        likes = []
        docs = db.collection("post_likes").where("post_id", "==", post_id).stream()

        for doc in docs:
            data = doc.to_dict()
            like = PostLike(data["post_id"], data["user_id"], data["created_at"])
            likes.append(like)

        return likes
