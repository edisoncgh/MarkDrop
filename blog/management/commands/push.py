"""
推送静态站点到 GitHub Pages
用法: python manage.py push
"""

import subprocess
from django.core.management.base import BaseCommand
from django.conf import settings
from pathlib import Path


class Command(BaseCommand):
    help = "推送静态站点到 GitHub Pages"

    def add_arguments(self, parser):
        parser.add_argument(
            "--message",
            "-m",
            default="Update blog content",
            help="提交消息",
        )
        parser.add_argument(
            "--no-push",
            action="store_true",
            help="只提交，不推送",
        )

    def handle(self, *args, **options):
        output_dir = Path(settings.OUTPUT_DIR)

        if not (output_dir / ".git").exists():
            self.stdout.write(
                self.style.ERROR(
                    "❌ output 目录不是 git 仓库，请先运行: python manage.py init_output"
                )
            )
            return

        try:
            # 检查是否有变更
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=output_dir,
                capture_output=True,
                text=True,
            )

            if not result.stdout.strip():
                self.stdout.write(self.style.WARNING("没有变更需要提交"))
                return

            # 添加所有变更
            self.stdout.write("📦 添加变更...")
            subprocess.run(["git", "add", "."], cwd=output_dir, check=True)

            # 提交
            message = options["message"]
            self.stdout.write(f"💾 提交: {message}")
            subprocess.run(
                ["git", "commit", "-m", message],
                cwd=output_dir,
                check=True,
            )

            if options["no_push"]:
                self.stdout.write(self.style.SUCCESS("✅ 已提交，未推送"))
                return

            # 推送（带重试）
            for attempt in range(3):
                try:
                    self.stdout.write(f"🚀 推送中... (尝试 {attempt + 1}/3)")
                    subprocess.run(
                        ["git", "push"],
                        cwd=output_dir,
                        check=True,
                    )
                    self.stdout.write(self.style.SUCCESS("✅ 推送成功！"))
                    return
                except subprocess.CalledProcessError as e:
                    if attempt < 2:
                        self.stdout.write(self.style.WARNING(f"推送失败，正在重试..."))
                    else:
                        raise

        except subprocess.CalledProcessError as e:
            self.stdout.write(self.style.ERROR(f"❌ 操作失败: {e}"))
            self.stdout.write("你可以稍后手动执行:")
            self.stdout.write("  cd output")
            self.stdout.write("  git add .")
            self.stdout.write(f'  git commit -m "{options["message"]}"')
            self.stdout.write("  git push")
