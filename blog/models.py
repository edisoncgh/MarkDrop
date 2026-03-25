from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    """分类"""

    name = models.CharField("分类名称", max_length=50)
    slug = models.SlugField("URL标识", unique=True, blank=True)
    description = models.TextField("分类描述", blank=True)
    order = models.IntegerField("排序", default=0)

    class Meta:
        verbose_name = "分类"
        verbose_name_plural = "分类"
        ordering = ["order", "name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def post_count(self):
        return self.posts.count()
class Tag(models.Model):
    """标签"""
    name = models.CharField('标签名称', max_length=50)
    slug = models.SlugField('URL标识', unique=True, blank=True)
    
    class Meta:
        verbose_name = '标签'
        verbose_name_plural = '标签'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    @property
    def post_count(self):
        return self.posts.count()


class Post(models.Model):
    """博文"""
    STATUS_CHOICES = [
        ('draft', '草稿'),
        ('published', '已发布'),
    ]
    
    title = models.CharField('标题', max_length=200)
    slug = models.SlugField('URL标识', unique=True, blank=True)
    content = models.TextField('内容 (Markdown)')
    content_html = models.TextField('渲染后HTML', blank=True)
    status = models.CharField('状态', max_length=20, choices=STATUS_CHOICES, default='draft')
    
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name='分类',
        related_name='posts'
    )
    tags = models.ManyToManyField(Tag, blank=True, verbose_name='标签', related_name='posts')
    
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    published_at = models.DateTimeField('发布时间', null=True, blank=True)
    cover_image = models.ImageField('封面图', upload_to='covers/', blank=True)
    
    class Meta:
        verbose_name = '博文'
        verbose_name_plural = '博文'
        ordering = ['-published_at', '-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        # TODO: 在 Phase 2 添加 Markdown 渲染
        super().save(*args, **kwargs)
    
    def tag_list(self):
        return ', '.join([tag.name for tag in self.tags.all()])
    tag_list.short_description = '标签'
