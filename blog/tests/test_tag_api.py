"""Tag 搜索和创建 API 测试"""

import json

from django.test import TestCase, Client
from django.contrib.auth.models import User
from blog.models import Tag


class TagSearchAPITest(TestCase):
    """测试 Tag 搜索 API"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_superuser(
            username="admin", password="admin123", email="admin@test.com"
        )
        self.client.login(username="admin", password="admin123")
        Tag.objects.create(name="Python", slug="python")
        Tag.objects.create(name="PyTorch", slug="pytorch")
        Tag.objects.create(name="生活", slug="sheng-huo")

    def test_search_returns_matching_tags(self):
        response = self.client.get("/api/tag-search/?q=Py")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        names = [t["name"] for t in data["tags"]]
        self.assertIn("Python", names)
        self.assertIn("PyTorch", names)
        self.assertNotIn("生活", names)

    def test_search_returns_all_when_no_query(self):
        response = self.client.get("/api/tag-search/")
        data = json.loads(response.content)
        self.assertEqual(len(data["tags"]), 3)

    def test_search_empty_result(self):
        response = self.client.get("/api/tag-search/?q=nonexistent")
        data = json.loads(response.content)
        self.assertEqual(data["tags"], [])

    def test_search_includes_post_count(self):
        response = self.client.get("/api/tag-search/")
        data = json.loads(response.content)
        for tag in data["tags"]:
            self.assertIn("post_count", tag)

    def test_search_rejects_unauthenticated(self):
        self.client.logout()
        response = self.client.get("/api/tag-search/")
        self.assertNotEqual(response.status_code, 200)


class TagQuickCreateAPITest(TestCase):
    """测试 Tag 快速创建 API"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_superuser(
            username="admin", password="admin123", email="admin@test.com"
        )
        self.client.login(username="admin", password="admin123")

    def test_creates_tag(self):
        response = self.client.post(
            "/api/tag-quick-create/",
            json.dumps({"name": "Django"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data["success"])
        self.assertEqual(data["tag"]["name"], "Django")

    def test_rejects_duplicate(self):
        Tag.objects.create(name="已存在", slug="exists")
        response = self.client.post(
            "/api/tag-quick-create/",
            json.dumps({"name": "已存在"}),
            content_type="application/json",
        )
        data = json.loads(response.content)
        self.assertFalse(data["success"])

    def test_rejects_empty_name(self):
        response = self.client.post(
            "/api/tag-quick-create/",
            json.dumps({"name": ""}),
            content_type="application/json",
        )
        data = json.loads(response.content)
        self.assertFalse(data["success"])

    def test_rejects_get(self):
        response = self.client.get("/api/tag-quick-create/")
        self.assertEqual(response.status_code, 405)

    def test_rejects_unauthenticated(self):
        self.client.logout()
        response = self.client.post(
            "/api/tag-quick-create/",
            json.dumps({"name": "test"}),
            content_type="application/json",
        )
        self.assertNotEqual(response.status_code, 200)
