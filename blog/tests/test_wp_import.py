"""WordPress 文章导入测试"""

from io import StringIO
from pathlib import Path

from django.core.management import call_command
from django.test import TestCase

from blog.models import Category, Post, Tag
from blog.utils.wp_import import (
    build_wp_post_url_map,
    clean_wp_xml_text,
    normalize_wp_post_content,
    parse_wp_posts,
)


FIXTURE = Path("blog/tests/fixtures/wp_sample_posts.xml")


class WordPressImportUtilsTest(TestCase):
    def test_clean_wp_xml_text_removes_invalid_controls(self):
        raw = "ok\x08still-ok"
        self.assertEqual(clean_wp_xml_text(raw), "okstill-ok")

    def test_parse_wp_posts_extracts_posts_only(self):
        posts = parse_wp_posts(FIXTURE)
        self.assertEqual(len(posts), 2)
        self.assertEqual(posts[0].title, "数论之素数筛")
        self.assertEqual(posts[0].categories, ["做题"])
        self.assertEqual(posts[0].tags, ["数论", "算法学习"])

    def test_build_wp_post_url_map_uses_slugify(self):
        posts = parse_wp_posts(FIXTURE)
        mapping = build_wp_post_url_map(posts)
        self.assertEqual(mapping[36], "../../posts/2020/shu-lun-zhi-su-shu-shai.html")
        self.assertEqual(
            mapping[88],
            "../../posts/2020/2020-lan-qiao-bei-sheng-sai-mo-ni-sai-bzu.html",
        )

    def test_normalize_wp_post_content_removes_comments_and_converts_code(self):
        posts = parse_wp_posts(FIXTURE)
        url_map = build_wp_post_url_map(posts)
        normalized = normalize_wp_post_content(posts[0].content_raw, url_map)
        self.assertNotIn("<!-- wp:", normalized)
        self.assertIn("```cpp", normalized)
        self.assertIn("int main(){return 0;}", normalized)
        self.assertIn("../../posts/2020/2020-lan-qiao-bei-sheng-sai-mo-ni-sai-bzu.html", normalized)

    def test_normalize_wp_post_content_handles_latex_and_missing_images(self):
        posts = parse_wp_posts(FIXTURE)
        url_map = build_wp_post_url_map(posts)
        normalized = normalize_wp_post_content(posts[1].content_raw, url_map)
        self.assertNotIn("[latexpage]", normalized)
        self.assertIn("```latex", normalized)
        self.assertIn(r"\frac{n*(n-1)}{2}+1", normalized)
        self.assertIn("[图片缺失]", normalized)
        self.assertIn("sample.png", normalized)


class ImportWordPressPostsCommandTest(TestCase):
    def test_dry_run_does_not_write_database(self):
        out = StringIO()
        call_command(
            "import_wordpress_posts",
            "--xml",
            str(FIXTURE),
            "--title",
            "数论之素数筛",
            "--dry-run",
            stdout=out,
        )
        self.assertEqual(Post.objects.count(), 0)
        self.assertIn("DRY RUN", out.getvalue())
        self.assertIn("数论之素数筛", out.getvalue())

    def test_apply_import_creates_single_selected_post(self):
        call_command(
            "import_wordpress_posts",
            "--xml",
            str(FIXTURE),
            "--title",
            "数论之素数筛",
            "--apply",
        )
        self.assertEqual(Post.objects.count(), 1)
        post = Post.objects.get()
        self.assertEqual(post.title, "数论之素数筛")
        self.assertEqual(post.slug, "shu-lun-zhi-su-shu-shai")
        self.assertEqual(post.status, "published")
        self.assertEqual(post.category.name, "做题")
        self.assertEqual(post.tags.count(), 2)
        self.assertTrue(Tag.objects.filter(name="数论").exists())
        self.assertTrue(Category.objects.filter(name="做题").exists())
        self.assertIn("```cpp", post.content)
        self.assertNotIn("<!-- wp:", post.content)


class WordPressBackupFactTest(TestCase):
    def test_real_backup_counts_match_expected(self):
        # 旧备份目录包含两个 XML 文件，取不含"页面"的那个（即文章备份）
        candidates = sorted(Path("old_blog_backup").glob("*.xml"))
        post_xmls = [f for f in candidates if "页面" not in f.name]
        self.assertTrue(post_xmls, "找不到 WordPress 文章备份 XML")
        xml_path = post_xmls[0]
        posts = parse_wp_posts(xml_path)
        self.assertEqual(len(posts), 121)
        self.assertEqual(
            sum(p.status == "publish" for p in posts), 117
        )
        self.assertEqual(
            sum(p.status == "draft" for p in posts), 4
        )
