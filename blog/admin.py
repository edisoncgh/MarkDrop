from django.contrib import admin
from django.contrib import messages
from django.utils.html import format_html
from .models import Post, Category, Tag, Moment, FriendLink, SiteConfig


def regenerate_static(modeladmin, request, queryset):
    """重新生成静态页面"""
    try:
        from blog.utils.generator import StaticSiteGenerator
        generator = StaticSiteGenerator()
        generator.generate_all()
        messages.success(request, '静态页面生成成功！')
    except Exception as e:
        messages.error(request, f'生成失败: {str(e)}')


regenerate_static.short_description = '重新生成静态页面'


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
    
    actions = [regenerate_static]

@admin.register(Moment)
class MomentAdmin(admin.ModelAdmin):
    list_display = ['id', 'content_preview', 'created_at']
    list_filter = ['created_at']
    
    def content_preview(self, obj):
        return obj.content[:100] + '...' if len(obj.content) > 100 else obj.content
    content_preview.short_description = '内容预览'


@admin.register(FriendLink)
class FriendLinkAdmin(admin.ModelAdmin):
    list_display = ['name', 'url', 'order', 'is_active', 'avatar_preview']
    list_editable = ['order', 'is_active']
    search_fields = ['name', 'url']
    
    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html('<img src="{}" width="40" height="40" style="border-radius:50%;">', obj.avatar)
        return '-'
    avatar_preview.short_description = '头像'


@admin.register(SiteConfig)
class SiteConfigAdmin(admin.ModelAdmin):
    list_display = ['key', 'value_preview', 'description']
    search_fields = ['key', 'description']
    
    def value_preview(self, obj):
        return obj.value[:50] + '...' if len(obj.value) > 50 else obj.value
    value_preview.short_description = '值'
