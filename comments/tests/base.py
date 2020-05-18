from django.test import TestCase
from blog.models import Post, User, Category, Tag
from django.apps import apps


class CommentDataTestCase(TestCase):
    def setUp(self):
        # 断开 haystack 的 signal，测试生成的文章无需生成索引
        apps.get_app_config("haystack").signal_processor.teardown()
        self.user = User.objects.create_superuser(
            username='admin',
            email='admin@hellogithub.com',
            password='admin'
        )
        self.cate = Category.objects.create(name='测试')
        self.post = Post.objects.create(
            title='测试标题',
            body='测试内容',
            category=self.cate,
            author=self.user,
        )