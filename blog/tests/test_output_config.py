"""OUTPUT_DIR 配置测试 — 验证静态输出路径可通过环境变量配置"""

import os
import tempfile
from pathlib import Path

from django.conf import settings
from django.test import TestCase, override_settings


class OutputDirSettingsTest(TestCase):
    """测试 OUTPUT_DIR 配置行为"""

    def test_output_dir_is_path_instance(self):
        self.assertIsInstance(settings.OUTPUT_DIR, Path)

    def test_default_output_dir_inside_project(self):
        """未设置环境变量时，OUTPUT_DIR 应在项目目录内"""
        expected_default = settings.BASE_DIR / "output"
        # 如果 EDGP_OUTPUT_DIR 未设置，应等于默认值
        if "EDGP_OUTPUT_DIR" not in os.environ:
            self.assertEqual(settings.OUTPUT_DIR, expected_default)

    def test_generator_reads_settings_output_dir(self):
        """StaticSiteGenerator 应从 settings.OUTPUT_DIR 读取路径"""
        from blog.utils.generator import StaticSiteGenerator

        gen = StaticSiteGenerator()
        self.assertEqual(gen.output_dir, Path(settings.OUTPUT_DIR))

    @override_settings(OUTPUT_DIR="/tmp/edgp_test_output")
    def test_generator_respects_overridden_output_dir(self):
        """当 OUTPUT_DIR 被覆盖时，生成器应使用新路径"""
        from blog.utils.generator import StaticSiteGenerator

        gen = StaticSiteGenerator()
        self.assertEqual(gen.output_dir, Path("/tmp/edgp_test_output"))


class GeneratorWriteToCustomDirTest(TestCase):
    """测试生成器可以写入到自定义外部目录"""

    @override_settings(OUTPUT_DIR=None)
    def test_generator_writes_to_custom_temp_dir(self):
        """生成器应能写入到任意外部目录"""
        from blog.utils.generator import StaticSiteGenerator

        with tempfile.TemporaryDirectory() as tmpdir:
            custom_path = Path(tmpdir) / "site_output"
            with override_settings(OUTPUT_DIR=str(custom_path)):
                gen = StaticSiteGenerator()
                gen.output_dir = custom_path
                custom_path.mkdir(parents=True, exist_ok=True)

                # 模拟写入一个页面
                gen._write_page("test.html", "<h1>Hello</h1>")

                written_file = custom_path / "test.html"
                self.assertTrue(written_file.exists())
                self.assertIn("<h1>Hello</h1>", written_file.read_text(encoding="utf-8"))

    def test_clean_output_preserves_git_directory(self):
        """清理输出目录时应保留 .git 目录"""
        from blog.utils.generator import StaticSiteGenerator

        with tempfile.TemporaryDirectory() as tmpdir:
            custom_path = Path(tmpdir) / "site_output"
            custom_path.mkdir()

            # 模拟 .git 目录和普通文件
            git_dir = custom_path / ".git"
            git_dir.mkdir()
            (git_dir / "HEAD").write_text("ref: refs/heads/main")

            (custom_path / "index.html").write_text("<html></html>")
            other_dir = custom_path / "static"
            other_dir.mkdir()
            (other_dir / "style.css").write_text("body{}")

            with override_settings(OUTPUT_DIR=str(custom_path)):
                gen = StaticSiteGenerator()
                gen.output_dir = custom_path
                gen._clean_output()

            # .git 应保留
            self.assertTrue(git_dir.exists())
            self.assertTrue((git_dir / "HEAD").exists())

            # 其他文件应被清除
            self.assertFalse((custom_path / "index.html").exists())
            self.assertFalse(other_dir.exists())
