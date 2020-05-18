from django import template
from ..forms import CommentForm
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

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

    p = Paginator(comment_list, 10)

    try:
        page = context['request'].GET.get('page', 1)
        p.page(page)
    except PageNotAnInteger:
        page = 1
    except EmptyPage:
        page = p.num_pages
    except KeyError:
        page = 1

    comment_list = p.page(page)
    page_len = p.num_pages

    return {
        'comment_list': comment_list,
        'comment_cont': comment_cont,
        'is_paginated': None if page_len <= 1 else True,
    }
