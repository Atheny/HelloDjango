from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Comment
        fields = [
            'name',
            'email',
            'url',
            'text',
            'created_time',
            'post',
        ]

        read_only_fields = [
            'created_time',
        ]

        extra_kwargs = {'post': {'write_only': True}}