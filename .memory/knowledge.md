# Project Knowledge

> Long-lived facts extracted from session memories. Updated incrementally.

## Architecture
- Django 5.x + SQLite 静态博客系统
- Admin 后台使用 django-simpleui (Element UI 风格)
- Markdown 编辑器: EasyMDE (static/vendor/easymde/)
- Markdown 渲染: markdown-it-py + pygments (blog/utils/markdown.py)
- 静态页面生成器: blog/utils/generator.py → output/
- 前端静态资源本地化，零 CDN 依赖
- 博客 API 路由前缀: /blog/api/

## Conventions
- 中文为主的工作语言
- Git 提交格式: `<type>: <description>`
- 博文内容用 Markdown 编写，保存时自动渲染为 content_html
- 静态生成需手动触发 (admin action 或 manage.py generate)
- 测试文件组织: blog/tests/test_<feature>.py
- API 视图使用 @require_POST / @require_GET 装饰器

## User Preferences
- 用户偏好简体中文沟通
- 倾向于渐进式优化而非大规模重写
- 重视管理后台的操作体验

## Decisions Log
- **2026-04-22**: 博文编辑器优化方案确定 — 保留 EasyMDE 但大幅增强，不替换为其他编辑器
- **2026-04-22**: Category/Tag 管理改为内联创建模式，不跳转页面
- **2026-04-22**: Tag 选择器用原生 JS 实现自定义组件，不引入 Select2 额外依赖
- **2026-04-22**: 工作流优化：新增"保存并生成"按钮 + 批量状态切换 actions
