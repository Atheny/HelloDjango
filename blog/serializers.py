from rest_framework import serializers
from .models import Post, Category, Tag, User

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'url',
        ]


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'url',
        ]


class TagSerializer(serializers.HyperlinkedModelSerializer):
    # url = serializers.HyperlinkedIdentityField(view_name='tag-detail')
    class Meta:
        model = Tag
        fields = [
            'id',
            'name',
            'url',
        ]


class PostListSerializer(serializers.HyperlinkedModelSerializer):
    category = CategorySerializer()
    author = UserSerializer()
    # url = serializers.HyperlinkedIdentityField(view_name='post-detail')

    class Meta:
        model = Post
        fields = [
            'id',
            'url',
            'title',
            'created_time',
            'excerpt',
            'category',
            'author',
            'view',

        ]


class PostRetrieveSerializer(serializers.HyperlinkedModelSerializer):
    category = CategorySerializer()
    author = UserSerializer()
    tags = TagSerializer(many=True)
    toc = serializers.CharField()
    body_html = serializers.CharField()

    class Meta:
        model = Post
        fields = [
            'id',
            'url',
            'title',
            'body',
            'created_time',
            'modified_time',
            'excerpt',
            'category',
            'tags',
            'author',
            'view',
            'toc',
            'body_html',
        ]


class CategoryPostRetrieveSerializer(serializers.ModelSerializer):
    post = PostListSerializer(many=True)

    class Meta:
        model = Category
        fields = [
            'id',
            'url',
            'name',
            'post',
        ]


class UserPostRetrieveSerializer(serializers.HyperlinkedModelSerializer):
    posts = PostListSerializer(many=True)

    class Meta:
        model = User
        fields = [
            'id',
            'url',
            'username',
            'posts',
        ]

