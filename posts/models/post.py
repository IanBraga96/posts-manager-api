class Post:
    """
    Class to represent a post from external API.
    Not stored in database.
    """

    def __init__(
        self, id=None, username="", title="", content="", created_datetime=None
    ):
        self.id = id
        self.username = username
        self.title = title
        self.content = content
        self.created_datetime = created_datetime
