"""Markdown 预览 API 测试"""

import json

from django.test import TestCase, Client
from django.contrib.auth.models import User


class MarkdownPreviewAPITest(TestCase):
    """测试 Markdown 预览 API"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_superuser(
            username="admin", password="admin123", email="admin@test.com"
        )
        self.client.login(username="admin", password="admin123")

    def test_renders_basic_markdown(self):
        response = self.client.post(
            "/api/markdown-preview/",
            json.dumps({"content": "# Hello\n\n**bold** text"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn("<h1>", data["html"])
        self.assertIn("<strong>", data["html"])

    def test_renders_code_block(self):
        response = self.client.post(
            "/api/markdown-preview/",
            json.dumps({"content": "```python\nprint('hello')\n```"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn("highlight", data["html"])

    def test_renders_mermaid_block(self):
        response = self.client.post(
            "/api/markdown-preview/",
            json.dumps({"content": "```mermaid\ngraph TD\nA-->B\n```"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('class="mermaid"', data["html"])

    def test_empty_content_returns_empty(self):
        response = self.client.post(
            "/api/markdown-preview/",
            json.dumps({"content": ""}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data["html"], "")

    def test_rejects_get_request(self):
        response = self.client.get("/api/markdown-preview/")
        self.assertEqual(response.status_code, 405)

    def test_rejects_unauthenticated(self):
        self.client.logout()
        response = self.client.post(
            "/api/markdown-preview/",
            json.dumps({"content": "test"}),
            content_type="application/json",
        )
        self.assertNotEqual(response.status_code, 200)
