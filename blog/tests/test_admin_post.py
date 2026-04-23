"""Post 模型和管理员配置测试 — 验证 slug 自动生成和 admin fieldsets"""

from django.test import TestCase
from django.contrib.admin.sites import AdminSite
from blog.models import Post, Category
from blog.admin import PostAdmin


class PostModelSlugTest(TestCase):
    """测试 Post 模型的 slug 自动生成逻辑"""

    def test_auto_generates_slug_from_title(self):
        post = Post.objects.create(title="测试文章标题", content="hello")
        self.assertNotEqual(post.slug, "")
        self.assertNotEqual(post.slug, None)

    def test_slug_generated_by_python_slugify(self):
        post = Post.objects.create(title="Hello World", content="hello")
        self.assertEqual(post.slug, "hello-world")

    def test_keeps_explicit_slug(self):
        post = Post.objects.create(
            title="随便", slug="my-custom-slug", content="hello"
        )
        self.assertEqual(post.slug, "my-custom-slug")

    def test_generates_slug_for_chinese_title(self):
        post = Post.objects.create(title="中文标题测试", content="hello")
        self.assertNotEqual(post.slug, "")
        self.assertTrue(len(post.slug) > 0)

    def test_different_titles_produce_different_slugs(self):
        p1 = Post.objects.create(title="文章一", content="a")
        p2 = Post.objects.create(title="文章二", content="b")
        self.assertNotEqual(p1.slug, p2.slug)


class PostAdminConfigTest(TestCase):
    """测试 PostAdmin 配置 — slug 不应出现在表单中"""

    def setUp(self):
        self.site = AdminSite()
        self.admin = PostAdmin(Post, self.site)

    def test_fieldsets_exclude_slug(self):
        """slug 不应出现在 admin 表单的 fieldsets 中"""
        all_fields = []
        for name, opts in self.admin.fieldsets:
            all_fields.extend(opts["fields"])
        self.assertNotIn("slug", all_fields)

    def test_no_prepopulated_fields(self):
        """不应有 prepopulated_fields（slug 不再由前端填充）"""
        self.assertEqual(self.admin.prepopulated_fields, {})

    def test_status_in_fieldsets(self):
        """status 字段应保留在 fieldsets 中"""
        all_fields = []
        for name, opts in self.admin.fieldsets:
            all_fields.extend(opts["fields"])
        self.assertIn("status", all_fields)

    def test_title_in_first_fieldset(self):
        """title 应在第一个 fieldset 中"""
        first_fields = self.admin.fieldsets[0][1]["fields"]
        self.assertIn("title", first_fields)


class PostStatusTest(TestCase):
    """测试 Post 状态行为"""

    def test_default_status_is_draft(self):
        post = Post.objects.create(title="test", content="hello")
        self.assertEqual(post.status, "draft")

    def test_publishing_sets_published_at(self):
        post = Post.objects.create(
            title="test", content="hello", status="published"
        )
        self.assertIsNotNone(post.published_at)

    def test_draft_has_no_published_at(self):
        post = Post.objects.create(title="test", content="hello", status="draft")
        self.assertIsNone(post.published_at)
