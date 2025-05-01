from datetime import datetime
from codeleap_careers.firebase_config import db


class CommentLike:
    def __init__(self, comment_id, user_id, created_at=None):
        self.comment_id = comment_id
        self.user_id = user_id
        self.created_at = created_at or datetime.now()

    @staticmethod
    def create(comment_id, user_id):
        like = CommentLike(comment_id, user_id)
        doc_ref = db.collection("comment_likes").document(f"{comment_id}_{user_id}")
        doc_ref.set(
            {
                "comment_id": comment_id,
                "user_id": user_id,
                "created_at": like.created_at
            }
        )
        return like

    @staticmethod
    def get(comment_id, user_id):
        doc_ref = db.collection("comment_likes").document(f"{comment_id}_{user_id}")
        doc = doc_ref.get()
        if doc.exists:
            data = doc.to_dict()
            return CommentLike(data["comment_id"], data["user_id"], data["created_at"])
        return None

    @staticmethod
    def delete(comment_id, user_id):
        doc_ref = db.collection("comment_likes").document(f"{comment_id}_{user_id}")
        doc_ref.delete()

    @staticmethod
    def list_by_comment(comment_id):
        likes = []
        docs = db.collection("comment_likes").where("comment_id", "==", comment_id).stream()

        for doc in docs:
            data = doc.to_dict()
            like = CommentLike(data["comment_id"], data["user_id"], data["created_at"])
            likes.append(like)

        return likes