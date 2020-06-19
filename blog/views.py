# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Category, Tag, User
from django.views.generic import ListView, DetailView
from pure_pagination.mixins import PaginationMixin
from django.contrib import messages
from django.db.models import Q
from pure_pagination import Paginator, PageNotAnInteger, EmptyPage

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


def search(request):
    q = request.GET.get('q')

    if not q:
        error_msg = "请输入搜索关键词"
        messages.add_message(request, messages.ERROR, error_msg, extra_tags='danger')
        return redirect('blog:index')

    post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))

    # 增加翻页功能
    p = Paginator(post_list, 10)
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1
    except EmptyPage:
        page = p.num_pages

    post_list = p.page(page)
    page_len = p.num_pages
    return render(request, 'blog/search_index.html', context={
        'post_list': post_list.object_list, 'page_obj': post_list, 'q': q, 'is_paginated': None if page_len <= 1 else True,
    })



from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.permissions import AllowAny
from .pagination import BlogPageNumberPagination

from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import views

from .serializers import PostListSerializer, PostRetrieveSerializer
from .serializers import CategorySerializer, TagSerializer, UserSerializer
from comments.serializers import CommentSerializer

from collections import OrderedDict
from rest_framework.serializers import DateField
from rest_framework.decorators import action

from django_filters.rest_framework import DjangoFilterBackend
from .filters import PostFilter




'''
实现index API视图函数
'''
@api_view(http_method_names=['GET'])
def index(request):
    post_list = Post.objects.all().order_by('-created_time')
    serializer = PostListSerializer(post_list, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


'''
用类视图实现首页API
'''
class IndexPostListAPIView(ListAPIView):
    serializer_class = PostListSerializer
    queryset = Post.objects.all().order_by('-created_time')
    pagination_class = PageNumberPagination
    permission_classes = [AllowAny]

'''
使用视图集
实现首页和详情页查看
'''
class PostViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = PostListSerializer
    queryset = Post.objects.all().order_by('-created_time')
    pagination_class = PageNumberPagination
    permission_classes = [AllowAny]
    lookup_field = 'pk'

    filter_backends = [DjangoFilterBackend]
    filterset_class = PostFilter

    serializer_class_table = {
        'list': PostListSerializer,
        'retrieve': PostRetrieveSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_class_table.get(self.action, super().get_serializer_class())


    @action(methods=['GET'], detail=False, url_path='archive/dates', url_name='archive-date')
    def list_archive_dates(self, request, *args, **kwargs):
        dates = Post.objects.dates('created_time', 'month', order='DESC')
        date_field = DateField()
        data = [date_field.to_representation(date) for date in dates]
        return Response(data=data, status=status.HTTP_200_OK)


    @action(methods=['GET'], detail=True, url_path='comments', url_name='comment', pagination_class=LimitOffsetPagination, serializer_class=CommentSerializer)
    def list_comments(self, request, *args, **kwargs):
        # 根据 URL 传入的参数值（文章 id）获取到博客文章记录
        post = self.get_object()
        # 获取文章下关联的全部评论
        queryset = post.comment_set.all().order_by('-created_time')
        # 对评论列表进行分页，根据 URL 传入的参数获取指定页的评论
        page = self.paginate_queryset(queryset)
        # 序列化评论
        serializer = self.get_serializer(page, many=True)
        # 返回分页后的评论列表
        return self.get_paginated_response(serializer.data)




########################################################################################################################
########################################################################################################################
########################################################################################################################
'''
按分类查看
'''
@api_view(http_method_names=['GET'])
def category_post_list(request, category):
    # 获取所有按标签分类的post数据
    post_list = Post.objects.filter(category=category).order_by('-created_time')
    # 实例化分页类
    pg = BlogPageNumberPagination()
    page = pg.paginate_queryset(queryset=post_list, request=request, view=mixins.ListModelMixin)
    serializer = PostListSerializer(instance=page, many=True, context={'request': request})

    return Response(OrderedDict([
        ('count', len(post_list)),
        ('next', pg.get_next_link()),
        ('previous', pg.get_previous_link()),
        ('results', serializer.data)
    ]), status=status.HTTP_200_OK)


class CategoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all().order_by('-pk')
    pagination_class = PageNumberPagination
    permission_classes = [AllowAny]
    lookup_field = 'pk'



'''
按标签查看
'''

@api_view(http_method_names=['GET'])
def tag_post_list(request, tags):
    # 获取所有按标签分类的post数据
    post_list = Post.objects.filter(tags=tags).order_by('-created_time')
    # 实例化分页类
    pg = BlogPageNumberPagination()

    # 调用paginate_queryset方法对数据进行分页处理，参数有三个：
    # 1. queryset是我们从数据库中取出的所有数据
    # 2.request=request
    # 3.view是处理分页的视图
    page = pg.paginate_queryset(queryset=post_list, request=request, view=mixins.ListModelMixin)
    serializer = PostListSerializer(instance=page, many=True, context={'request': request})

    # return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(OrderedDict([
        ('count', len(post_list)),
        ('next', pg.get_next_link()),
        ('previous', pg.get_previous_link()),
        ('results', serializer.data)
    ]), status=status.HTTP_200_OK)


class TagViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all().order_by('-pk')
    pagination_class = PageNumberPagination
    permission_classes = [AllowAny]
    lookup_field = 'pk'



'''
按作者查看
'''
@api_view(http_method_names=['GET'])
def author_post_list(request, author):
    post_list = Post.objects.filter(author=author).order_by('-created_time')
    pg = BlogPageNumberPagination()
    page = pg.paginate_queryset(queryset=post_list, request=request, view=mixins.ListModelMixin)
    serializer = PostListSerializer(instance=page, many=True, context={'request': request})
    return Response(OrderedDict([
        ('count', len(post_list)),
        ('next', pg.get_next_link()),
        ('previous', pg.get_previous_link()),
        ('results', serializer.data)
    ]), status=status.HTTP_200_OK)


class AuthorViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all().order_by('-pk')
    pagination_class = PageNumberPagination
    permission_classes = [AllowAny]
    lookup_field = 'pk'

########################################################################################################################
########################################################################################################################
########################################################################################################################