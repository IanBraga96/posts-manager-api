from django.db import models


class PostLike(models.Model):
    post_id = models.IntegerField()
    username = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["post_id", "username"]
