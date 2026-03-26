from django.shortcuts import render


def index(request):
    """本地端入口页 - 跳转到 Admin 后台"""
    return render(request, 'portal.html')

