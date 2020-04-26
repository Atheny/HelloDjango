from django import template
from ..forms import CommentForm

register = template.Library()


@register.inclusion_tag('comments/inclusions/_form.html', takes_context=True)
def show_comment_form(context, post, form=None):
    if form is None:
        form = CommentForm()
    return {
        'form': form,
        'post': post,
    }

@register.inclusion_tag('comments/inclusions/_list.html', takes_context=True)
def show_comments(context, post):
    # 等价于 Comment.objects.filter(post=post).order_by('-created_time')
    comment_list = post.comment_set.all()
    comment_cont = comment_list.count()
    return {
        'comment_list': comment_list,
        'comment_cont': comment_cont,
    }
