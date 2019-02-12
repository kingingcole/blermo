from rest_framework import generics
from .serializers import PostsSerializers, UsersSerializers
from .models import Post
from django.contrib.auth.models import User

class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostsSerializers
    lookup_field = 'slug'


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostsSerializers
    lookup_field = 'slug'

class UsersList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UsersSerializers

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UsersSerializers

