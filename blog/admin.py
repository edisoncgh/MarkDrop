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


def publish_posts(modeladmin, request, queryset):
    """批量发布文章"""
    count = queryset.filter(status='draft').update(status='published')
    messages.success(request, f'已发布 {count} 篇文章')


publish_posts.short_description = '发布选中的文章'


def unpublish_posts(modeladmin, request, queryset):
    """批量取消发布"""
    count = queryset.filter(status='published').update(status='draft')
    messages.success(request, f'已将 {count} 篇文章设为草稿')


unpublish_posts.short_description = '将选中的文章设为草稿'


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
    list_display = ["title", "category", "status_colored", "published_at", "tag_list"]
    list_filter = ["status", "category", "tags", "created_at"]
    list_editable = ["category"]
    search_fields = ["title", "content"]
    filter_horizontal = []  # 使用自定义 tag-input 组件替代
    date_hierarchy = "published_at"

    fieldsets = (
        ("基本信息", {"fields": ("title", "status", "category", "tags")}),
        ("内容", {"fields": ("content", "cover_image")}),
        ("时间", {"fields": ("published_at",), "classes": ("collapse",)}),
    )

    def status_colored(self, obj):
        if obj.status == 'published':
            return format_html('<span style="color:#67c23a; font-weight:bold;">已发布</span>')
        return format_html('<span style="color:#909399;">草稿</span>')
    status_colored.short_description = '状态'

    def response_add(self, request, obj, post_url_continue=None):
        """新建文章后，如果点了"保存并生成"则触发静态生成"""
        if '_save_and_generate' in request.POST:
            self._try_generate(request)
        return super().response_add(request, obj, post_url_continue)

    def response_change(self, request, obj):
        """编辑文章后，如果点了"保存并生成"则触发静态生成"""
        if '_save_and_generate' in request.POST:
            self._try_generate(request)
        return super().response_change(request, obj)

    def _try_generate(self, request):
        try:
            from blog.utils.generator import StaticSiteGenerator
            generator = StaticSiteGenerator()
            generator.generate_all()
            messages.success(request, '文章已保存，静态页面生成成功！')
        except Exception as e:
            messages.warning(request, f'文章已保存，但静态页面生成失败: {str(e)}')

    class Media:
        css = {
            'all': (
                '/static/vendor/easymde/easymde.min.css',
                '/static/css/admin-post.css',
            )
        }
        js = (
            '/static/vendor/easymde/easymde.min.js',
            '/static/js/admin-post.js',
            '/static/js/admin-category-inline.js',
            '/static/js/admin-tag-input.js',
            '/static/js/admin-status-toggle.js',
            '/static/js/admin-save-generate.js',
        )

    actions = [regenerate_static, publish_posts, unpublish_posts]


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
