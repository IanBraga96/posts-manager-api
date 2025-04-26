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