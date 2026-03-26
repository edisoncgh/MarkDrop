"""
初始化 output 目录为独立的 git 仓库
用于 GitHub Pages 部署
"""

from django.core.management.base import BaseCommand
from django.conf import settings
from pathlib import Path
import subprocess


class Command(BaseCommand):
    help = "初始化 output 目录为独立的 git 仓库"

    def handle(self, *args, **options):
        output_dir = Path(settings.OUTPUT_DIR)

        if not output_dir.exists():
            output_dir.mkdir(parents=True)
            self.stdout.write(f"创建目录: {output_dir}")

        git_dir = output_dir / ".git"

        if git_dir.exists():
            self.stdout.write(self.style.WARNING(f"output 目录已初始化: {output_dir}"))
            return

        # 初始化 git 仓库
        try:
            subprocess.run(["git", "init"], cwd=output_dir, check=True)
            self.stdout.write(
                self.style.SUCCESS(f"[OK] Git 仓库初始化成功: {output_dir}")
            )

            # 创建 .gitkeep
            (output_dir / ".gitkeep").touch()

            # 提示后续操作
            self.stdout.write("\n后续步骤:")
            self.stdout.write("  1. cd output")
            self.stdout.write("  2. git remote add origin <your-github-pages-repo-url>")
            self.stdout.write("  3. git branch -M main")
            self.stdout.write("  4. git push -u origin main")
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"[ERROR] 初始化失败: {e}"))
