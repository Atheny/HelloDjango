"""HelloDjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from blog.feeds import AllPostsRssFeed

from django.views.generic.base import RedirectView
from rest_framework import routers
from blog.views import PostViewSet, CategoryViewSet, TagViewSet, AuthorViewSet

router = routers.DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'categorys', CategoryViewSet, basename='category')
router.register(r'tags', TagViewSet, basename='tag')
router.register(r'authors', AuthorViewSet, basename='user')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('', include('comments.urls')),
    path('all/rss/', AllPostsRssFeed(), name='rss'),
    path('search/', include('haystack.urls')),

    # 添加favicon.ico图标
    path('favicon.ico', RedirectView.as_view(url=r'/static/favicon.ico')),

    # 添加polls(投票url)
    path('polls/', include('polls.urls')),

    # 添加rest-framework提供的api交互后台和登录认证
    path('api/', include(router.urls)),
    path('api/auth/', include("rest_framework.urls", namespace="rest_framework")),
]


