from datetime import datetime
from codeleap_careers.firebase_config import db


class PostComment:
    def __init__(
        self, id, post_id, user_id, content, mentioned_users=None, created_at=None
    ):
        self.id = id
        self.post_id = post_id
        self.user_id = user_id
        self.content = content
        self.mentioned_users = mentioned_users or []
        self.created_at = created_at or datetime.now()

    @staticmethod
    def create(post_id, user_id, content, mentioned_users=None):
        doc_ref = db.collection("post_comments").document()
        comment = PostComment(doc_ref.id, post_id, user_id, content, mentioned_users)

        doc_ref.set(
            {
                "post_id": post_id,
                "user_id": user_id,
                "content": content,
                "mentioned_users": mentioned_users or [],
                "created_at": comment.created_at,
            }
        )
        return comment

    @staticmethod
    def get(comment_id):
        doc_ref = db.collection("post_comments").document(comment_id)
        doc = doc_ref.get()
        if doc.exists:
            data = doc.to_dict()
            return PostComment(
                doc.id,
                data["post_id"],
                data["user_id"],
                data["content"],
                data["mentioned_users"],
                data["created_at"],
            )
        return None

    @staticmethod
    def list_by_post(post_id):
        comments = []
        docs = (
            db.collection("post_comments")
            .where("post_id", "==", post_id)
            .order_by("created_at", direction="DESCENDING")
            .stream()
        )

        for doc in docs:
            data = doc.to_dict()
            comment = PostComment(
                doc.id,
                data["post_id"],
                data["user_id"],
                data["content"],
                data["mentioned_users"],
                data["created_at"],
            )
            comments.append(comment)

        return comments

    @staticmethod
    def delete(comment_id):
        doc_ref = db.collection("post_comments").document(comment_id)
        doc_ref.delete()

    def update(self, content, mentioned_users):
        doc_ref = db.collection("post_comments").document(self.id)
        doc_ref.update({"content": content, "mentioned_users": mentioned_users})
        self.content = content
        self.mentioned_users = mentioned_users
        return self
