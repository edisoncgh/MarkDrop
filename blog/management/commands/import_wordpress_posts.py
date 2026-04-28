"""一次性导入 WordPress 旧博客文章。"""

from __future__ import annotations

from collections import Counter
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from slugify import slugify

from blog.models import Category, Post, Tag
from blog.utils.wp_import import (
    build_wp_post_url_map,
    normalize_wp_post_content,
    parse_wp_posts,
)


class Command(BaseCommand):
    help = "从 WordPress XML 一次性导入博文"

    def add_arguments(self, parser):
        parser.add_argument("--xml", required=True, help="WordPress 文章 XML 文件路径")
        parser.add_argument("--title", help="只导入指定标题的文章")
        parser.add_argument("--dry-run", action="store_true", help="只解析并输出结果")
        parser.add_argument("--apply", action="store_true", help="正式写入数据库")

    def handle(self, *args, **options):
        xml_path = Path(options["xml"])
        if not xml_path.exists():
            raise CommandError(f"XML 文件不存在: {xml_path}")

        if not options["dry_run"] and not options["apply"]:
            options["dry_run"] = True

        posts = parse_wp_posts(xml_path)
        title = options.get("title")
        if title:
            posts = [post for post in posts if post.title == title]

        if not posts:
            raise CommandError("没有找到符合条件的文章")

        if options["dry_run"]:
            self._print_summary(posts)
            return

        self._ensure_no_slug_conflicts(posts)
        self._apply_import(posts)
        self.stdout.write(self.style.SUCCESS(f"已导入 {len(posts)} 篇文章"))

    def _print_summary(self, posts):
        statuses = Counter(post.status for post in posts)
        titles = ", ".join(post.title for post in posts[:5])
        self.stdout.write(f"总文章数: {len(posts)}")
        self.stdout.write(f"状态统计: {dict(statuses)}")
        self.stdout.write(f"文章样本: {titles}")
        self.stdout.write("DRY RUN: 未写入数据库")

    def _ensure_no_slug_conflicts(self, posts):
        existing_slugs = set(Post.objects.values_list("slug", flat=True))
        incoming_slugs = [slugify(post.title) for post in posts]
        duplicates = sorted({slug for slug in incoming_slugs if slug in existing_slugs})
        if duplicates:
            raise CommandError(f"检测到 slug 冲突: {duplicates}")

    @transaction.atomic
    def _apply_import(self, posts):
        url_map = build_wp_post_url_map(posts)
        for parsed in posts:
            category = None
            tag_names = list(parsed.tags)
            if parsed.categories:
                category, _ = Category.objects.get_or_create(name=parsed.categories[0])
                for extra in parsed.categories[1:]:
                    if extra not in tag_names:
                        tag_names.append(extra)

            content = normalize_wp_post_content(parsed.content_raw, url_map)
            post = Post.objects.create(
                title=parsed.title,
                slug=slugify(parsed.title),
                content=content,
                status="published" if parsed.status == "publish" else "draft",
                category=category,
                published_at=parsed.published_at,
            )
            tags = [Tag.objects.get_or_create(name=name)[0] for name in tag_names]
            post.tags.set(tags)

            created_at = parsed.published_at or parsed.updated_at
            updated_at = parsed.updated_at or parsed.published_at
            if created_at or updated_at:
                Post.objects.filter(pk=post.pk).update(
                    created_at=created_at or post.created_at,
                    updated_at=updated_at or post.updated_at,
                )
