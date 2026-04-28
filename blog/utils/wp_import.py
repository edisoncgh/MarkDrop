"""WordPress XML 导入辅助工具。"""

from __future__ import annotations

from dataclasses import dataclass, field
from html import unescape
from pathlib import Path
import re
import xml.etree.ElementTree as ET

from django.utils import timezone
from slugify import slugify


INVALID_XML_CONTROL_RE = re.compile(r"[\x00-\x08\x0B\x0C\x0E-\x1F]")
WP_COMMENT_RE = re.compile(r"<!--\s*/?wp:[\s\S]*?-->")
ENLIGHTER_RE = re.compile(
    r'<pre[^>]*class="EnlighterJSRAW"[^>]*data-enlighter-language="(?P<lang>[^"]*)"[^>]*>(?P<code>.*?)</pre>',
    re.S,
)
LATEX_CODE_RE = re.compile(r"<code>\s*\$\$(?P<formula>.*?)\$\$\s*</code>", re.S)
ARCHIVE_LINK_RE = re.compile(
    r'https?://www\.edisoncgh\.com/archives/(?P<post_id>\d+)'
)
IMG_RE = re.compile(
    r'<(?:figure[^>]*>\s*)?<img[^>]*src="(?P<src>[^"]+)"[^>]*>(?:\s*</figure>)?',
    re.I,
)


@dataclass
class ParsedWPPost:
    wp_post_id: int
    title: str
    status: str
    slug_source: str
    content_raw: str
    published_at: timezone.datetime | None
    updated_at: timezone.datetime | None
    categories: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)


def clean_wp_xml_text(raw: str) -> str:
    return INVALID_XML_CONTROL_RE.sub("", raw)


def parse_wp_posts(xml_path: Path) -> list[ParsedWPPost]:
    raw = xml_path.read_text(encoding="utf-8", errors="replace")
    clean = clean_wp_xml_text(raw)
    root = ET.fromstring(clean)
    ns = {
        "content": "http://purl.org/rss/1.0/modules/content/",
        "wp": "http://wordpress.org/export/1.2/",
    }
    items = root.find("channel").findall("item")

    posts: list[ParsedWPPost] = []
    for item in items:
        if item.findtext("wp:post_type", default="", namespaces=ns) != "post":
            continue

        categories: list[str] = []
        tags: list[str] = []
        for term in item.findall("category"):
            name = (term.text or "").strip()
            if not name:
                continue
            if term.attrib.get("domain") == "category":
                categories.append(name)
            elif term.attrib.get("domain") == "post_tag":
                tags.append(name)

        posts.append(
            ParsedWPPost(
                wp_post_id=int(
                    item.findtext("wp:post_id", default="0", namespaces=ns)
                ),
                title=item.findtext("title", default="").strip(),
                status=item.findtext("wp:status", default="", namespaces=ns),
                slug_source=item.findtext(
                    "wp:post_name", default="", namespaces=ns
                ),
                content_raw=item.findtext(
                    "content:encoded", default="", namespaces=ns
                )
                or "",
                published_at=_parse_dt(
                    item.findtext("wp:post_date", default="", namespaces=ns)
                ),
                updated_at=_parse_dt(
                    item.findtext("wp:post_modified", default="", namespaces=ns)
                ),
                categories=categories,
                tags=tags,
            )
        )
    return posts


def build_wp_post_url_map(posts: list[ParsedWPPost]) -> dict[int, str]:
    mapping: dict[int, str] = {}
    for post in posts:
        dt = post.published_at or post.updated_at or timezone.now()
        mapping[post.wp_post_id] = (
            f"../../posts/{dt.year}/{slugify(post.title)}.html"
        )
    return mapping


def normalize_wp_post_content(content: str, url_map: dict[int, str]) -> str:
    normalized = WP_COMMENT_RE.sub("", content)
    normalized = normalized.replace("[latexpage]", "")
    normalized = _replace_enlighter_blocks(normalized)
    normalized = _replace_latex_blocks(normalized)
    normalized = _replace_missing_images(normalized)
    normalized = _rewrite_internal_links(normalized, url_map)
    return normalized.strip()


def _parse_dt(value: str) -> timezone.datetime | None:
    value = value.strip()
    if not value:
        return None
    naive = timezone.datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
    return timezone.make_aware(naive, timezone.get_current_timezone())


def _replace_enlighter_blocks(content: str) -> str:
    def repl(match: re.Match[str]) -> str:
        lang = match.group("lang") or ""
        code = unescape(match.group("code")).strip()
        return f"\n```{lang}\n{code}\n```\n"

    return ENLIGHTER_RE.sub(repl, content)


def _replace_latex_blocks(content: str) -> str:
    def repl(match: re.Match[str]) -> str:
        formula = unescape(match.group("formula")).strip()
        return f"\n```latex\n{formula}\n```\n"

    return LATEX_CODE_RE.sub(repl, content)


def _replace_missing_images(content: str) -> str:
    def repl(match: re.Match[str]) -> str:
        src = match.group("src")
        return (
            f'<p><strong>[图片缺失]</strong> 原图：'
            f'<a href="{src}">{src}</a></p>'
        )

    return IMG_RE.sub(repl, content)


def _rewrite_internal_links(content: str, url_map: dict[int, str]) -> str:
    def repl(match: re.Match[str]) -> str:
        post_id = int(match.group("post_id"))
        return url_map.get(post_id, match.group(0))

    return ARCHIVE_LINK_RE.sub(repl, content)
