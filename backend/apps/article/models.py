from django.db import models
from apps.accounts.models import CustomUser


class Article(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    is_public = models.BooleanField(default=True)
    author = models.ForeignKey(
        CustomUser, 
        on_delete=models.CASCADE,
        related_name='articles'
        )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title
    
    