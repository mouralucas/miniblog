from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):
    PUBLISHED = 'published'
    DRAFT = 'draft'

    STATUS = (
        (PUBLISHED, 'Published'),
        (DRAFT, 'Draft')
    )

    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=10, choices=STATUS, default=DRAFT)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'post'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    content = models.TextField(max_length=500)  # Limit the length of comment
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'post_comment'
