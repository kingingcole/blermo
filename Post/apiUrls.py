from django.urls import path
from . import apiViews

urlpatterns = [
    path('posts/', apiViews.PostList.as_view()),
    path('posts/<str:slug>', apiViews.PostDetail.as_view()),

    path('users/', apiViews.UsersList.as_view()),
    path('users/<int:pk>', apiViews.UserDetail.as_view()),
]
