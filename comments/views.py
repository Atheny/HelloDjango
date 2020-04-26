from django.shortcuts import render, get_object_or_404, redirect
from blog.views import Post
from django.views.decorators.http import require_POST
from django.contrib import messages

from .forms import CommentForm

# 评论视图
@require_POST
def comment(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        # 检查到数据是合法的，调用表单的 save 方法保存数据到数据库，
        # commit=False 的作用是仅仅利用表单的数据生成 Comment 模型类的实例，但还不保存评论数据到数据库
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
        messages.add_message(request, messages.SUCCESS, '评论发表成功！', extra_tags='success')

        # 重定向到 post 的详情页，实际上当 redirect 函数接收一个模型的实例时，它会调用这个模型实例的 get_absolute_url 方法，
        # 然后重定向到 get_absolute_url 方法返回的 URL。
        # redirect 既可以接收一个 URL 作为参数，也可以接收一个模型的实例作为参数（例如这里的 post）。
        #  如果接收一个模型的实例，那么这个实例必须实现了 get_absolute_url 方法，这样 redirect 会根据 get_absolute_url 方法返回的 URL 值进行重定向。
        # return redirect(post)  # 接收一个模型的实例
        return redirect('blog:detail', post.pk)

    # 检查到数据不合法，我们渲染一个预览页面，用于展示表单的错误。
    # 注意这里被评论的文章 post 也传给了模板，因为我们需要根据 post 来生成表单的提交地址。
    context = {
        'post': post,
        'form': form,
    }

    messages.add_message(request, messages.ERROR, '评论发表失败！请修改表单中的错误后重新提交。', extra_tags='danger')
    return render(request, 'comments/preview.html', context=context)
