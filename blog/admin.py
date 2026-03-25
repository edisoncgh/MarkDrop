from django.contrib import admin
from .models import Post, Category, Tag


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "order", "post_count"]
    list_editable = ["order"]
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ["name"]

    def post_count(self, obj):
        return obj.post_count

    post_count.short_description = "文章数"


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "post_count"]
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ["name"]

    def post_count(self, obj):
        return obj.post_count

    post_count.short_description = "文章数"


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "status", "published_at", "tag_list"]
    list_filter = ["status", "category", "tags", "created_at"]
    search_fields = ["title", "content"]
    filter_horizontal = ["tags"]
    date_hierarchy = "published_at"
    prepopulated_fields = {"slug": ("title",)}

    fieldsets = (
        ("基本信息", {"fields": ("title", "slug", "status", "category", "tags")}),
        ("内容", {"fields": ("content", "cover_image")}),
        ("时间", {"fields": ("published_at",), "classes": ("collapse",)}),
    )

    class Media:
        css = {
            'all': ('/static/vendor/easymde/easymde.min.css',)
        }
        js = (
            '/static/vendor/easymde/easymde.min.js',
            '/static/js/admin-post.js',
        )
