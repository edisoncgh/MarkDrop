from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path("", views.index, name="index"),
    path("api/markdown-preview/", views.markdown_preview, name="markdown_preview"),
    path("api/category-quick-create/", views.category_quick_create, name="category_quick_create"),
    path("api/tag-search/", views.tag_search, name="tag_search"),
    path("api/tag-quick-create/", views.tag_quick_create, name="tag_quick_create"),
]
