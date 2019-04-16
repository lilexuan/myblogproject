from django.db import models
from django.contrib.auth.models import User
from django.utils.six import python_2_unicode_compatible
from django.urls import reverse

# Create your models here.
@python_2_unicode_compatible
class Category(models.Model):
    """
    这是一个分类类
    只需要一个属性, 即name
    CharField 指定了分类名name的数据类型, CharField是字符型
    CharField 的 max_length 参数指定了其最大长度, 超过这个长度的分类名就不能存入数据库
    Django 的其他内置类型可查看文档
    https://docs.djangoproject.com/en/1.10/ref/models/fields/#field-types
    """
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

# 装饰器@python_2_unicode_compatible, 用于兼容python2
@python_2_unicode_compatible
class Tag(models.Model):
    """
    这是一个标签类
    """
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    
    # 自定义 get_absolute_url 方法
    # 记得从 django.urls 中导入reverse函数

@python_2_unicode_compatible
class Post(models.Model):
    """
    这是一个文章类
    """

    # 文章标题
    title = models.CharField(max_length=70)

    # 文章正文, 我们使用 TextField
    body = models.TextField()

    # 文章的创建时间和最后一次修改时间, 存储时间的字段用 DateTimeField 类型
    created_time = models.DateTimeField()
    modified_time = models.DateTimeField()

    # 文章摘要
    # 文章摘要可以为空, 设置blank=True即可以允许参数值为空
    excerpt = models.CharField(max_length=200, blank=True)

    # 这是分类与标签，分类与标签的模型我们已经定义在上面。
    # 我们在这里把文章对应的数据库表和分类、标签对应的数据库表关联了起来，但是关联形式稍微有点不同。
    # 我们规定一篇文章只能对应一个分类，但是一个分类下可以有多篇文章，所以我们使用的是 ForeignKey，即一对多的关联关系。
    # 而对于标签来说，一篇文章可以有多个标签，同一个标签下也可能有多篇文章，所以我们使用 ManyToManyField，表明这是多对多的关联关系。
    # 同时我们规定文章可以没有标签，因此为标签 tags 指定了 blank=True。
    # 如果你对 ForeignKey、ManyToManyField 不了解，请看教程中的解释，亦可参考官方文档：
    # https://docs.djangoproject.com/en/1.10/topics/db/models/#relationships

    category = models.ForeignKey(Category);
    tags = models.ManyToManyField(Tag, blank=True)

    # 文章作者，这里 User 是从 django.contrib.auth.models 导入的。
    # django.contrib.auth 是 Django 内置的应用，专门用于处理网站用户的注册、登录等流程，User 是 Django 为我们已经写好的用户模型。
    # 这里我们通过 ForeignKey 把文章和 User 关联了起来。
    # 因为我们规定一篇文章只能有一个作者，而一个作者可能会写多篇文章，因此这是一对多的关联关系，和 Category 类似

    author = models.ForeignKey(User)
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-created_time']