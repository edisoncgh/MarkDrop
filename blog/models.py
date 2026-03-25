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
