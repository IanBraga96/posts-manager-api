from django.db import models


class PostComment(models.Model):
    post_id = models.IntegerField()
    username = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    mentioned_users = models.JSONField(default=list)

    class Meta:
        ordering = ["-created_at"]
