from django.urls import path, include
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='detail'),
    path('archives/<int:year>/<int:month>/', views.ArchiveView.as_view(), name='archive'),
    path('category/<int:pk>/', views.CategoryView.as_view(), name='category'),
    path('tag/<int:pk>/', views.TagView.as_view(), name='tag'),
    path('author/<int:pk>/', views.AuthorView.as_view(), name='author'),
    # path('search/', views.search, name='search'),
    # path('api/index/', views.index),
    # path('api/index/', views.IndexPostListAPIView.as_view()),
    # path('api/index/', views.PostViewSet.as_view({'get': 'list'})),   # 可省略

    # path('api/tag/<int:tags>/', views.tag_post_list),
    # path('api/category/<int:category>/', views.category_post_list),
    # path('api/author/<int:author>/', views.author_post_list),


]