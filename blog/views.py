import json

from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST

from blog.models import Category, Tag
from blog.utils import render_markdown

MAX_PREVIEW_LENGTH = 100_000


def index(request):
    """本地端入口页 - 跳转到 Admin 后台"""
    return render(request, "portal.html")


@require_POST
@staff_member_required
def markdown_preview(request: HttpRequest) -> JsonResponse:
    """Markdown 预览 API — 接收 Markdown 文本，返回渲染后的 HTML"""
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        data = {}

    content = data.get("content", "")
    if len(content) > MAX_PREVIEW_LENGTH:
        return JsonResponse(
            {"html": "<p>内容过长，预览已限制</p>"},
            status=400,
        )
    html = render_markdown(content)
    return JsonResponse({"html": html})


@require_POST
@staff_member_required
def category_quick_create(request: HttpRequest) -> JsonResponse:
    """Category 快速创建 API — 在文章编辑页内联创建分类"""
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        data = {}

    name = data.get("name", "").strip()
    if not name:
        return JsonResponse({"success": False, "error": "分类名称不能为空"})

    if Category.objects.filter(name=name).exists():
        return JsonResponse({"success": False, "error": "该分类已存在"})

    description = data.get("description", "").strip()
    category = Category.objects.create(name=name, description=description)
    return JsonResponse({
        "success": True,
        "category": {
            "id": category.pk,
            "name": category.name,
            "slug": category.slug,
        },
    })


@require_GET
@staff_member_required
def tag_search(request: HttpRequest) -> JsonResponse:
    """Tag 搜索 API — 支持 autocomplete"""
    query = request.GET.get("q", "").strip()
    tags = Tag.objects.all()
    if query:
        tags = tags.filter(name__icontains=query)

    tags = tags[:20]
    results = [
        {"id": tag.pk, "name": tag.name, "slug": tag.slug, "post_count": tag.post_count}
        for tag in tags
    ]
    return JsonResponse({"tags": results})


@require_POST
@staff_member_required
def tag_quick_create(request: HttpRequest) -> JsonResponse:
    """Tag 快速创建 API — 在文章编辑页内联创建标签"""
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        data = {}

    name = data.get("name", "").strip()
    if not name:
        return JsonResponse({"success": False, "error": "标签名称不能为空"})

    if Tag.objects.filter(name=name).exists():
        return JsonResponse({"success": False, "error": "该标签已存在"})

    tag = Tag.objects.create(name=name)
    return JsonResponse({
        "success": True,
        "tag": {
            "id": tag.pk,
            "name": tag.name,
            "slug": tag.slug,
        },
    })
