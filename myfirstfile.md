# 一级标题
## 二级标题
### 三级标题
#### 四级标题
##### 五级标题
###### 六级标题

[百度](https://www.baidu.com)

1. 有序列表效果
2. 有序列表效果
3. 有序列表效果
4. 有序列表效果
6. 有序列表效果

缩进效果：

        缩进两个缩进两个缩进两个缩进两个缩进两个缩进两个缩进两个缩进两个缩进
    两个缩进两个缩进两个缩进两个缩进两个缩进两个缩进两个缩进两个

- 无序列表第一项
- 无序列表第二项
* 无序效果
* 无序效果
* 无序效果

>这里是引用

![图片下方文字1](http://upload-images.jianshu.io/upload_images/1343547-13d325fdbb097530.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


![图片下方文字2](https://www.baidu.com/img/bd_logo1.png)


** 加粗字体**
*斜体*
~~删除线~~

* #### 分割线

---
  
或者

***

* #### 使用三个 ` 将代码包含起来即可，如下：

``` 
def fun():
    print('Hello Python!')
```
* #### 表格
| Tables        | Are           | Cool  |
| ------------- |:-------------:| -----:|
| col 3 is      | right-aligned | $187980890600 |
| col 2 is      | centered      |   $12 |
| zebra stripes | are neat      |    $1 |

| 编号 | 姓名 | address |
| ------ |:------:| ---------- |
|ddc|cs|xsc fbfgbgbbfgbgdbggb| 

---

# 一级标题

## 二级标题

### 三级标题

- 列表项1
- 列表项2
- 列表项3

> 这是引用部分（下面是代码段）

```
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from blog.models import Post
import markdown

def index(request):
    post_list = Post.objects.all().order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})

def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.body = markdown.markdown(post.body,
                                  extensions=[
                                      'markdown.extensions.extra',
                                      # 'markdown.extensions.codehilite',
                                      'markdown.extensions.fenced_code',
                                      'markdown.extensions.toc',
                                  ])
    return render(request, 'blog/detail.html', context={'post': post})
```