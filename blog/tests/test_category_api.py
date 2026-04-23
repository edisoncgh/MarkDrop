"""Category 快速创建 API 测试"""

import json

from django.test import TestCase, Client
from django.contrib.auth.models import User
from blog.models import Category


class CategoryQuickCreateAPITest(TestCase):
    """测试 Category 快速创建 API"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_superuser(
            username="admin", password="admin123", email="admin@test.com"
        )
        self.client.login(username="admin", password="admin123")

    def test_creates_category(self):
        response = self.client.post(
            "/api/category-quick-create/",
            json.dumps({"name": "技术", "description": "技术文章"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data["success"])
        self.assertEqual(data["category"]["name"], "技术")
        self.assertTrue(Category.objects.filter(name="技术").exists())

    def test_auto_generates_slug(self):
        response = self.client.post(
            "/api/category-quick-create/",
            json.dumps({"name": "生活随笔"}),
            content_type="application/json",
        )
        data = json.loads(response.content)
        self.assertTrue(data["success"])
        self.assertNotEqual(data["category"]["slug"], "")

    def test_rejects_duplicate_name(self):
        Category.objects.create(name="已存在", slug="exists")
        response = self.client.post(
            "/api/category-quick-create/",
            json.dumps({"name": "已存在"}),
            content_type="application/json",
        )
        data = json.loads(response.content)
        self.assertFalse(data["success"])
        self.assertIn("error", data)

    def test_rejects_get(self):
        response = self.client.get("/api/category-quick-create/")
        self.assertEqual(response.status_code, 405)

    def test_rejects_empty_name(self):
        response = self.client.post(
            "/api/category-quick-create/",
            json.dumps({"name": ""}),
            content_type="application/json",
        )
        data = json.loads(response.content)
        self.assertFalse(data["success"])

    def test_rejects_unauthenticated(self):
        self.client.logout()
        response = self.client.post(
            "/api/category-quick-create/",
            json.dumps({"name": "test"}),
            content_type="application/json",
        )
        self.assertNotEqual(response.status_code, 200)
