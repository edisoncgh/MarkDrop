# Current Context

> Active working state — updated each turn.

## Active Task
博文编辑器优化 — 已完成

## Phase Progress
- [x] Phase 1: 编辑器升级 (EasyMDE 增强 + 异步预览 API)
- [x] Phase 2: Category 内联创建 (API + 前端组件)
- [x] Phase 3: Tag 选择器重构 (自定义 tag-input 组件 + API)
- [x] Phase 4: 工作流优化 (保存并生成 + 批量状态切换)
- [x] 安全修复: @staff_member_required、异步XHR、内容长度限制

## Modified Files
- `blog/views.py` — 新增 4 个 API 视图，全部加 @staff_member_required
- `blog/urls.py` — 新增 4 个 API 路由
- `blog/admin.py` — 移除 filter_horizontal, 新增 actions, status_colored, save_and_generate
- `static/js/admin-post.js` — 重写，异步预览 API，mermaid/latex 按钮
- `static/js/admin-category-inline.js` — 新增，Category 内联创建
- `static/js/admin-tag-input.js` — 新增，自定义 Tag 选择器
- `static/js/admin-save-generate.js` — 新增，保存并生成按钮

## Test Files (22 tests, all passing)
- `blog/tests/test_preview_api.py` — 6 tests (含认证测试)
- `blog/tests/test_category_api.py` — 6 tests (含认证测试)
- `blog/tests/test_tag_api.py` — 10 tests (含认证测试)

## Blockers
- None

## Next Steps
- 在浏览器中测试实际效果
- 可选：验证 SimpleUI 下各组件的渲染效果
