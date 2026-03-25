from django.shortcuts import render
from .models import Post, Category, Tag


def index(request):
    """首页视图"""
    posts = Post.objects.filter(status='published').order_by('-published_at')[:10]
    categories = Category.objects.all()
    tags = Tag.objects.all()
    return render(request, 'pages/index.html', {
        'posts': posts,
        'categories': categories,
        'tags': tags,
        'site': {'title': 'EDGP 博客', 'description': '基于 Django 的静态博客生成器'}
    })
