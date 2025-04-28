from django.db import models

# Create your models here.


class Post:
    """
    Class to represent a post.
    Just a representation of the data from the external API.
    """

    def __init__(
        self, id=None, username="", title="", content="", created_datetime=None
    ):
        self.id = id
        self.username = username
        self.title = title
        self.content = content
        self.created_datetime = created_datetime


class PostLike(models.Model):
    post_id = models.IntegerField()
    username = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['post_id', 'username']