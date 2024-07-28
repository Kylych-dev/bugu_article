# serializers.py

from rest_framework import serializers
from apps.article.models import Article

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = [
            'id', 
            'title', 
            'content', 
            'is_public', 
            'author', 
            'created_at', 
            'updated_at'
            ]
        read_only_fields = [
            'author', 
            'created_at', 
            'updated_at'
            ]



