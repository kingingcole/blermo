"""lark URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from Post.views import PostCreate, PostLikeToggle, PostComment
from users import views as usersViews
from main_site import views as ms_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('Post.apiUrls')),
    path('follow/', usersViews.follow_toggle, name='follow_toggle'),
    path('like/', PostLikeToggle, name='post_like_toggle'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('', include('main_site.urls')),
    path('feed/', include('Post.urls')),
    path('', include('users.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = ms_views.handler404
handler500 = ms_views.handler500
