from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.utils.text import slugify
from .models import Post, Category, Tag, User
import markdown
from markdown.extensions.toc import TocExtension
import re
from django.views.generic import ListView, DetailView
from pure_pagination.mixins import PaginationMixin

# 类视图(博客首页)
class IndexView(PaginationMixin, ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    # 指定 paginate_by 属性后开启分页功能，其值代表每一页包含多少篇文章
    paginate_by = 10



# 博客按时间显示类视图(直接复用了index.html模板)
class ArchiveView(IndexView):
    def get_queryset(self):
        return super(ArchiveView, self).get_queryset().filter(created_time__year=self.kwargs.get('year'),
                                                              created_time__month=self.kwargs.get('month')
                                                              )


# 博客按分类显示类视图(直接复用了index.html模板)
class CategoryView(IndexView):
    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)


# 博客按标签显示类视图(直接复用了index.html模板)
class TagView(IndexView):
    def get_queryset(self):
        t = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tags=t)


# 博客按作者显示类视图(直接复用了index.html模板)
class AuthorView(IndexView):
    def get_queryset(self):
        u = get_object_or_404(User, pk=self.kwargs.get('pk'))
        return super(AuthorView, self).get_queryset().filter(author=u)


# 博客详情页类视图
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        # 覆写 get 方法的目的是因为每当文章被访问一次，就得将文章阅读量 +1
        # get 方法返回的是一个 HttpResponse 实例
        # 之所以需要先调用父类的 get 方法，是因为只有当 get 方法被调用后，
        # 才有 self.object 属性，其值为 Post 模型实例，即被访问的文章 post
        response = super(PostDetailView, self).get(request, *args, **kwargs)

        # 将文章阅读量 +1
        # 注意 self.object 的值就是被访问的文章 post
        self.object.increase_views()

        # 视图必须返回一个 HttpResponse 对象
        return response
    
    def get_object(self, queryset=None):
        # 覆写 get_object 方法的目的是因为需要对 post 的 body 值进行渲染
        post = super(PostDetailView, self).get_object(queryset=None)
        return post