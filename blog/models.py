from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.utils.html import strip_tags
import markdown
from markdown.extensions.toc import TocExtension
from django.utils.text import slugify
import re
from django.utils.functional import cached_property

# Create your models here.

class Category(models.Model):
    name = models.CharField('分类名称', max_length=100)

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField('标签名称', max_length=100)

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Post(models.Model):
    # 文章标题
    title = models.CharField('标题', max_length=70)

    # 文章正文
    body = models.TextField('正文')
    created_time = models.DateTimeField('创建时间', default=timezone.now)
    modified_time = models.DateTimeField('修改时间')

    # 文章摘要(可以为空)
    excerpt = models.CharField('摘要', max_length=200, blank=True)

    # 一对多关联  # 使用 models.CASCADE 参数，意为级联删除
    category = models.ForeignKey(Category, related_name='post', verbose_name='分类', on_delete=models.CASCADE)

    # 多对多关联  # 文章可以没有标签，因此为标签 tags 指定了 blank=True
    tags = models.ManyToManyField(Tag, related_name='post', verbose_name='标签', blank=True)

    # 文章作者.  这里 User 是从 django.contrib.auth.models 导入的。
    # django.contrib.auth 是 django 内置的应用，专门用于处理网站用户的注册、登录等流程，
    # User 是 django 为我们已经写好的用户模型。
    author = models.ForeignKey(User, related_name='posts', verbose_name='作者', on_delete=models.CASCADE)

    # 新增统计阅读量字段
    view = models.PositiveIntegerField(default=0, editable=False)

    def save(self, *args, **kwargs):
        self.modified_time = timezone.now()
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])
        self.excerpt = strip_tags(md.convert(self.body))[:54]
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']


    def __str__(self):
        return self.title

    # 返回文章详情视图对应的url
    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    # 将views字段的值+1
    def increase_views(self):
        self.view += 1
        self.save(update_fields=['view'])

    @cached_property
    def rich_content(self):
        return generate_rich_content(self.body)

    @property
    def toc(self):
        return self.rich_content.get("toc", "")

    @property
    def body_html(self):
        return self.rich_content.get("content", "")






def generate_rich_content(value):
    md = markdown.Markdown(
        extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            TocExtension(slugify=slugify),
        ]
    )
    content = md.convert(value)
    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    toc = m.group(1) if m is not None else ''
    return {"content": content, "toc": toc}
