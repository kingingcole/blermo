from rest_framework import serializers
from .models import Post
from django.contrib.auth.models import User

class PostsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }

class UsersSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
