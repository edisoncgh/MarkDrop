from django.db import models
from django.utils import timezone
from slugify import slugify  # 使用 python-slugify 支持中文


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

    name = models.CharField("标签名称", max_length=50)
    slug = models.SlugField("URL标识", unique=True, blank=True)

    class Meta:
        verbose_name = "标签"
        verbose_name_plural = "标签"
        ordering = ["name"]

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
        ("draft", "草稿"),
        ("published", "已发布"),
    ]

    title = models.CharField("标题", max_length=200)
    slug = models.SlugField("URL标识", unique=True, blank=True)
    content = models.TextField("内容 (Markdown)")
    content_html = models.TextField("渲染后HTML", blank=True)
    status = models.CharField(
        "状态", max_length=20, choices=STATUS_CHOICES, default="draft"
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="分类",
        related_name="posts",
    )
    tags = models.ManyToManyField(
        Tag, blank=True, verbose_name="标签", related_name="posts"
    )

    created_at = models.DateTimeField("创建时间", auto_now_add=True)
    updated_at = models.DateTimeField("更新时间", auto_now=True)
    published_at = models.DateTimeField("发布时间", null=True, blank=True)
    cover_image = models.ImageField("封面图", upload_to="covers/", blank=True)

    class Meta:
        verbose_name = "博文"
        verbose_name_plural = "博文"
        ordering = ["-published_at", "-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # 使用 python-slugify 生成 slug (支持中文)
        if not self.slug:
            self.slug = slugify(self.title)

        # 自动渲染 Markdown
        if self.content:
            from blog.utils import render_markdown

            self.content_html = render_markdown(self.content)

        # 发布时自动设置发布时间
        if self.status == "published" and not self.published_at:
            self.published_at = timezone.now()

        super().save(*args, **kwargs)

    def tag_list(self):
        return ", ".join([tag.name for tag in self.tags.all()])

    tag_list.short_description = "标签"


class Moment(models.Model):
    """说说 - 简短随笔"""

    content = models.TextField("内容 (Markdown)")
    content_html = models.TextField("渲染后HTML", blank=True)
    images = models.JSONField("图片列表", default=list, blank=True)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)

    class Meta:
        verbose_name = "说说"
        verbose_name_plural = "说说"
        ordering = ["-created_at"]

    def __str__(self):
        return self.content[:50] + "..." if len(self.content) > 50 else self.content

    def save(self, *args, **kwargs):
        from blog.utils import render_markdown

        if self.content:
            self.content_html = render_markdown(self.content)
        super().save(*args, **kwargs)


class FriendLink(models.Model):
    """友情链接"""

    name = models.CharField("名称", max_length=100)
    url = models.URLField("链接地址")
    description = models.TextField("描述", blank=True)
    avatar = models.URLField("头像URL", blank=True)
    order = models.IntegerField("排序", default=0)
    is_active = models.BooleanField("是否显示", default=True)

    class Meta:
        verbose_name = "友链"
        verbose_name_plural = "友链"
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


class SiteConfig(models.Model):
    """站点配置 - 键值对存储"""

    key = models.CharField("配置键", max_length=50, unique=True)
    value = models.TextField("配置值")
    description = models.CharField("说明", max_length=200, blank=True)

    class Meta:
        verbose_name = "站点配置"
        verbose_name_plural = "站点配置"

    def __str__(self):
        return self.key

    @classmethod
    def get(cls, key, default=""):
        """获取配置值"""
        try:
            return cls.objects.get(key=key).value
        except cls.DoesNotExist:
            return default

    @classmethod
    def set(cls, key, value, description=""):
        """设置配置值"""
        obj, _ = cls.objects.update_or_create(
            key=key, defaults={"value": value, "description": description}
        )
        return obj
