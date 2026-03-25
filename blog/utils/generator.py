"""
静态站点生成器
将数据库内容渲染为静态 HTML 文件
"""

import os
import shutil
from pathlib import Path
from django.conf import settings
from django.template.loader import render_to_string
from django.utils import timezone


class StaticSiteGenerator:
    """静态站点生成器"""

    def __init__(self):
        self.output_dir = Path(settings.OUTPUT_DIR)
        self.templates_dir = Path(settings.SITE_TEMPLATES_DIR)
        self.static_src_dir = Path(settings.STATIC_SRC_DIR)
        self.site_config = self._load_site_config()

    def _load_site_config(self):
        """加载站点配置"""
        from ..models import SiteConfig

        return {
            "title": SiteConfig.get("site.title", "我的博客"),
            "description": SiteConfig.get("site.description", ""),
            "author": SiteConfig.get("author.name", ""),
            "url": SiteConfig.get("site.url", ""),
        }

    def _get_context(self, extra=None, static_prefix="static", url_prefix=""):
        """获取通用模板上下文

        Args:
            extra: 额外的上下文变量
            static_prefix: 静态资源路径前缀 (相对于当前页面)
            url_prefix: URL路径前缀 (用于链接跳转)
        """
        context = {
            "site": self.site_config,
            "static_prefix": static_prefix,
            "url_prefix": url_prefix,
        }
        if extra:
            context.update(extra)
        return context

    def _write_page(self, relative_path, content):
        """写入页面文件"""
        file_path = self.output_dir / relative_path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding="utf-8")
        print(f"  生成: {relative_path}")

    def _clean_output(self):
        """清理输出目录（保留 .git）"""
        print("[CLEAN] 清理输出目录...")
        for item in self.output_dir.iterdir():
            if item.name != ".git":
                if item.is_dir():
                    shutil.rmtree(item)
                else:
                    item.unlink()

    def _copy_static(self):
        """复制静态资源到输出目录"""
        print("[STATIC] 复制静态资源...")

        # 复制 static_src 到 output/static
        dest = self.output_dir / "static"
        if dest.exists():
            shutil.rmtree(dest)

        if self.static_src_dir.exists():
            shutil.copytree(self.static_src_dir, dest)

        # 复制 vendor 资源
        vendor_src = Path(settings.STATICFILES_DIRS[0]) / "vendor"
        vendor_dest = dest / "vendor"
        if vendor_src.exists():
            if vendor_dest.exists():
                shutil.rmtree(vendor_dest)
            shutil.copytree(vendor_src, vendor_dest)

        print("  静态资源复制完成")

    def generate_all(self):
        """生成全部静态页面"""
        print("[START] 开始生成静态站点...")

        self._clean_output()
        self._copy_static()

        self._generate_index()
        self._generate_posts()
        self._generate_archive()
        self._generate_tags()
        self._generate_moments()
        self._generate_friends()
        self._generate_about()

        print("[DONE] 静态站点生成完成！")

    def _generate_index(self):
        """生成首页"""
        from ..models import Post, Category, Tag

        print("[PAGE] 生成首页...")
        posts = Post.objects.filter(status="published").order_by("-published_at")[:10]
        categories = Category.objects.all()
        tags = Tag.objects.all()

        context = self._get_context(
            {
                "posts": posts,
                "categories": categories,
                "tags": tags,
            },
            static_prefix="static",
            url_prefix="",
        )

        html = render_to_string("pages/index.html", context)
        self._write_page("index.html", html)

    def _generate_posts(self):
        """生成所有博文页面"""
        from ..models import Post

        print("[POSTS] 生成博文页面...")
        posts = list(Post.objects.filter(status="published").order_by("-published_at"))

        for i, post in enumerate(posts):
            prev_post = posts[i - 1] if i > 0 else None
            next_post = posts[i + 1] if i < len(posts) - 1 else None

            year = post.published_at.year if post.published_at else post.created_at.year

            # 计算相对路径前缀: posts/2026/slug.html 需要回到根目录
            static_prefix = "../../static"  # 从 posts/2026/ 回到 static
            url_prefix = "../../"  # 从 posts/2026/ 回到根目录 (含尾部斜杠)
            context = self._get_context(
                {
                    "post": post,
                    "prev_post": prev_post,
                    "next_post": next_post,
                },
                static_prefix=static_prefix,
                url_prefix=url_prefix,
            )

            html = render_to_string("pages/post.html", context)
            path = f"posts/{year}/{post.slug}.html"
            self._write_page(path, html)

    def _generate_archive(self):
        """生成归档页"""
        from ..models import Post

        print("[ARCHIVE] 生成归档页...")
        posts = Post.objects.filter(status="published").order_by("-published_at")

        context = self._get_context(
            {"posts": posts},
            static_prefix="static",
            url_prefix="",  # 首页在根目录，无需前缀
        )
        html = render_to_string("pages/archive.html", context)
        self._write_page("archive.html", html)

    def _generate_tags(self):
        """生成标签页"""
        from ..models import Tag, Post

        print("[TAGS] 生成标签页...")

        # 生成标签列表页
        tags = Tag.objects.all()
        context = self._get_context(
            {"tags": tags},
            static_prefix="static",
            url_prefix="",  # 标签列表页在根目录
        )
        html = render_to_string("pages/tags.html", context)
        self._write_page("tags/index.html", html)

        # 生成每个标签页
        for tag in tags:
            posts = Post.objects.filter(status="published", tags=tag)
            context = self._get_context(
                {"tag": tag, "posts": posts},
                static_prefix="../static",  # 从 tags/ 回到 static
                url_prefix="../",  # 从 tags/ 回到根目录 (含尾部斜杠)
            html = render_to_string("pages/tag.html", context)
            self._write_page(f"tags/{tag.slug}.html", html)

    def _generate_categories(self):
        """生成分类页"""
        from ..models import Category, Post

        print("[CATEGORIES] 生成分类页...")

        for cat in Category.objects.all():
            posts = Post.objects.filter(status="published", category=cat)
            context = self._get_context(
                {"category": cat, "posts": posts},
                static_prefix="../static",  # 从 categories/ 回到 static
                url_prefix="../",  # 从 categories/ 回到根目录 (含尾部斜杠)
            )
            html = render_to_string("pages/category.html", context)
            self._write_page(f"categories/{cat.slug}.html", html)

    def _generate_moments(self):
        """生成说说页"""
        from ..models import Moment

        print("[MOMENTS] 生成说说页...")
        moments = Moment.objects.all().order_by("-created_at")

        context = self._get_context(
            {"moments": moments},
            static_prefix="static",
            url_prefix="",
        )
        html = render_to_string("pages/moments.html", context)
        self._write_page("moments.html", html)

    def _generate_friends(self):
        """生成友链页"""
        from ..models import FriendLink

        print("[FRIENDS] 生成友链页...")
        links = FriendLink.objects.filter(is_active=True).order_by("order", "name")

        context = self._get_context(
            {"links": links},
            static_prefix="static",
            url_prefix="",
        )
        html = render_to_string("pages/friends.html", context)
        self._write_page("friends.html", html)

    def _generate_about(self):
        """生成关于页"""
        from ..models import SiteConfig

        print("[ABOUT] 生成关于页...")
        about_content = SiteConfig.get("about.content", "")

        context = self._get_context(
            {"about_content": about_content},
            static_prefix="static",
            url_prefix="",
        )
        html = render_to_string("pages/about.html", context)
        self._write_page("about.html", html)

