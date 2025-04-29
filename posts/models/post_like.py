from datetime import datetime
from codeleap_careers.firebase_config import db


class PostLike:
    def __init__(self, post_id, username, created_at=None):
        self.post_id = post_id
        self.username = username
        self.created_at = created_at or datetime.now()

    @staticmethod
    def create(post_id, username):
        like = PostLike(post_id, username)
        doc_ref = db.collection('post_likes').document(f"{post_id}_{username}")
        doc_ref.set({
            'post_id': post_id,
            'username': username,
            'created_at': like.created_at
        })
        return like

    @staticmethod
    def get(post_id, username):
        doc_ref = db.collection('post_likes').document(f"{post_id}_{username}")
        doc = doc_ref.get()
        if doc.exists:
            data = doc.to_dict()
            return PostLike(data['post_id'], data['username'], data['created_at'])
        return None

    @staticmethod
    def delete(post_id, username):
        doc_ref = db.collection('post_likes').document(f"{post_id}_{username}")
        doc_ref.delete()

    @staticmethod
    def list_by_post(post_id):
        likes = []
        docs = db.collection('post_likes').where('post_id', '==', post_id).stream()
        
        for doc in docs:
            data = doc.to_dict()
            like = PostLike(
                data['post_id'],
                data['username'],
                data['created_at']
            )
            likes.append(like)
        
        return likes
