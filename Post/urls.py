from django.urls import path
from .views import Feed, PostDetail, PostUpdate, PostDelete, PostComment

urlpatterns = [
    path('', Feed, name='feed'),

    path('article/<str:slug>/', PostDetail.as_view(), name='post_detail'),
    path('article/<str:slug>/edit/', PostUpdate.as_view(), name='post_update'),
    path('article/<str:slug>/comment/',  PostComment, name='post_comment'),
    path('article/<str:slug>/delete/', PostDelete.as_view(), name='post_delete')
]
