"""
生成静态站点命令
用法: python manage.py generate
"""

from django.core.management.base import BaseCommand
from blog.utils.generator import StaticSiteGenerator


class Command(BaseCommand):
    help = "生成静态博客站点"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clean",
            action="store_true",
            help="清理输出目录后重新生成",
        )

    def handle(self, *args, **options):
        try:
            generator = StaticSiteGenerator()
            generator.generate_all()
            self.stdout.write(self.style.SUCCESS("[SUCCESS] 静态站点生成成功！"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"[ERROR] 生成失败: {str(e)}"))
            raise
