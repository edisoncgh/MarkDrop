"""归档页面生成测试 — 验证年份分组功能"""

import re
import tempfile
from datetime import datetime
from pathlib import Path

from django.conf import settings
from django.test import TestCase, override_settings
from django.utils import timezone

from blog.models import Post
from blog.utils.generator import StaticSiteGenerator


class ArchiveYearGroupingTest(TestCase):
    """测试归档页面按年份分组"""

    def setUp(self):
        # 创建跨越多个年份的文章
        self.p1 = Post.objects.create(
            title="2026年文章",
            slug="2026-post",
            content="2026 content",
            status="published",
            published_at=timezone.make_aware(datetime(2026, 3, 25, 10, 0, 0)),
        )
        self.p2 = Post.objects.create(
            title="2022年文章",
            slug="2022-post",
            content="2022 content",
            status="published",
            published_at=timezone.make_aware(datetime(2022, 4, 4, 10, 0, 0)),
        )
        self.p3 = Post.objects.create(
            title="2020年文章",
            slug="2020-post",
            content="2020 content",
            status="published",
            published_at=timezone.make_aware(datetime(2020, 3, 5, 10, 0, 0)),
        )
        self.p4 = Post.objects.create(
            title="草稿文章",
            slug="draft-post",
            content="draft content",
            status="draft",
            published_at=timezone.make_aware(datetime(2026, 1, 1, 10, 0, 0)),
        )

    @override_settings(OUTPUT_DIR=None)
    def test_archive_contains_year_headers(self):
        """归档页应为每个年份生成标题分割"""
        with tempfile.TemporaryDirectory() as tmpdir:
            custom_path = Path(tmpdir) / "output"
            with override_settings(OUTPUT_DIR=str(custom_path)):
                gen = StaticSiteGenerator()
                gen._generate_archive()

            html = (custom_path / "archive.html").read_text(encoding="utf-8")

            # 应该包含年份标题
            self.assertIn('class="archive-year-title"', html,
                          "归档页应包含年份标题")

    @override_settings(OUTPUT_DIR=None)
    def test_archive_groups_posts_by_year_with_headers(self):
        """归档页应在每个年份组之前有对应的年份标题"""
        with tempfile.TemporaryDirectory() as tmpdir:
            custom_path = Path(tmpdir) / "output"
            with override_settings(OUTPUT_DIR=str(custom_path)):
                gen = StaticSiteGenerator()
                gen._generate_archive()

            html = (custom_path / "archive.html").read_text(encoding="utf-8")

            # 验证所有三个年份标题存在（应作为 year header 而非仅 URL 出现）
            for year in ["2026", "2022", "2020"]:
                self.assertIn(
                    f'archive-year-title">{year}',
                    html,
                    f"归档页应包含年份 {year} 的标题",
                )

    @override_settings(OUTPUT_DIR=None)
    def test_archive_year_order_is_descending(self):
        """年份应按降序排列（新的在前）"""
        with tempfile.TemporaryDirectory() as tmpdir:
            custom_path = Path(tmpdir) / "output"
            with override_settings(OUTPUT_DIR=str(custom_path)):
                gen = StaticSiteGenerator()
                gen._generate_archive()

            html = (custom_path / "archive.html").read_text(encoding="utf-8")

            # 提取年份标题出现的顺序
            year_titles = re.findall(r'archive-year-title[^>]*>(\d{4})', html)
            self.assertGreater(len(year_titles), 0, "应有年份标题")
            # 按时间倒序：2026 > 2022 > 2020
            years_int = [int(y) for y in year_titles]
            self.assertEqual(
                years_int,
                sorted(years_int, reverse=True),
                "年份应按降序排列",
            )

    @override_settings(OUTPUT_DIR=None)
    def test_archive_excludes_draft_posts(self):
        """草稿文章不应出现在归档页"""
        with tempfile.TemporaryDirectory() as tmpdir:
            custom_path = Path(tmpdir) / "output"
            with override_settings(OUTPUT_DIR=str(custom_path)):
                gen = StaticSiteGenerator()
                gen._generate_archive()

            html = (custom_path / "archive.html").read_text(encoding="utf-8")
            self.assertNotIn("草稿文章", html, "草稿不应出现在归档页")

    @override_settings(OUTPUT_DIR=None)
    def test_archive_posts_under_correct_year_header(self):
        """每篇文章应出现在对应年份标题下方"""
        with tempfile.TemporaryDirectory() as tmpdir:
            custom_path = Path(tmpdir) / "output"
            with override_settings(OUTPUT_DIR=str(custom_path)):
                gen = StaticSiteGenerator()
                gen._generate_archive()

            html = (custom_path / "archive.html").read_text(encoding="utf-8")

            # 2026 年标题应在 2026年文章 之前
            pos_2026_header = html.find("archive-year-title")
            self.assertGreater(pos_2026_header, 0)
            pos_2026_post = html.find("2026-post")
            self.assertGreater(pos_2026_post, pos_2026_header)
