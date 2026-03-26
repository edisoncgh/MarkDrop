# EDGP 静态博客系统 - 实现设计

> 基于 DESIGN.md 的实现计划，采用 MVP 优先 + 分层构建策略

## 决策摘要

| 决策点 | 选择 | 理由 |
|--------|------|------|
| 实现方式 | MVP 优先 | 先验证流程可行，再扩展功能 |
| 前端框架 | Bootstrap 本地化 | 解决 CDN 加载失败问题 |
| Markdown | 全功能 (mermaid + LaTeX + 代码高亮) | 符合原始设计目标 |
| 实现方案 | 分层构建 (Phase 1→2→3) | 每阶段可独立验证，风险可控 |

---

## Phase 1: 骨架搭建 (MVP)

**目标**: 创建可运行的博客骨架，通过 Admin 管理 Post/Category/Tag

### 项目结构

```
edgp/
├── edgp/                     # Django 项目配置
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── blog/                     # 核心应用
│   ├── models.py             # Post, Category, Tag
│   ├── admin.py              # SimpleUI Admin
│   └── utils/
│       └── markdown.py       # Markdown 渲染
│
├── local_templates/          # 本地端模板 (极简入口页)
│   └── portal.html           # "进入后台"入口页
│
├── site_templates/           # 静态站点模板 (生成用)
│   ├── base.html
│   ├── components/
│   └── pages/
│
├── static/                   # Admin 静态资源
│   └── vendor/
│       ├── bootstrap/
│       └── easymde/
│
├── output/                   # 静态输出 (独立 git 仓库)
├── media/                    # 上传文件
├── manage.py
└── requirements.txt
```

### 任务清单

```yaml
1. 项目初始化
   □ 创建 Django 项目结构
   □ 配置 settings.py (数据库、模板、静态文件)
   □ 安装依赖 (requirements.txt)
   
2. 数据模型 (MVP)
   □ Category 模型 (name, slug, order)
   □ Tag 模型 (name, slug)
   □ Post 模型 (title, slug, content, content_html, status, category, tags)
   
3. Admin 配置
   □ 安装 django-simpleui
   □ 配置 CategoryAdmin, TagAdmin, PostAdmin
   □ EasyMDE 编辑器集成 (前端)
   
4. 前端资源
   □ 下载 Bootstrap 5 (CSS + JS) 到 static/vendor/
   □ 下载 EasyMDE 到 static/vendor/
   □ 下载 highlight.js
   
5. 模板系统 (基础)
   □ base.html (布局框架)
   □ navbar.html, footer.html (组件)
   □ index.html (首页)
   □ post.html (文章详情)
   
6. 验证
   □ python manage.py migrate
   □ 创建测试数据
   □ Admin 可正常 CRUD
```

**完成标志**: Admin 可正常管理博文、分类、标签

### ⚠️ 重要修正：本地入口页

> **核心理念**: "本地撰写、生成页面，在线仓库展示页面"

本地端 **不需要** "好看"的博客网站页面，只需要：
- 极简入口页：标题 + "进入后台" 按钮
- 直接跳转到 `/admin/` 开始撰写博文

**重构任务** (Phase 1 补充):
```yaml
7. 本地入口页重构
   □ 创建 local_templates/portal.html (极简入口)
   □ 修改 blog/views.py 的 index 视图
   □ 更新 settings.py 模板路径配置
   □ site_templates/ 保留为静态生成专用模板
```

---

## Phase 2: 核心功能

**目标**: 实现静态页面生成器 + 完整 Markdown 渲染

### 任务清单

```yaml
1. Markdown 渲染器
   □ 配置 markdown-it-py + plugins
   □ mermaid 支持 (前端渲染)
   □ LaTeX/KaTeX 支持
   □ 代码高亮 (pygments)
   
2. 静态生成器
   □ StaticSiteGenerator 类
   □ _generate_index()
   □ _generate_posts()
   □ _copy_static()
   
3. 完整模型
   □ Moment 模型 (说说)
   □ FriendLink 模型 (友链)
   □ SiteConfig 模型 (配置)
   
4. Management Commands
   □ python manage.py generate
   □ 基础测试
```

**完成标志**: `python manage.py generate` 可生成完整静态站点

---

## Phase 3: 完善与部署

**目标**: 完整模板系统 + Git 推送

### 任务清单

```yaml
1. 完整模板系统
   □ archive.html (归档)
   □ tags/index.html (标签列表)
   □ moments.html (说说)
   □ friends.html (友链)
   □ about.html (关于)
   
2. Admin 增强
   □ 自定义 Action: regenerate_static
   □ 自定义 Action: push_to_github
   □ 保存时自动渲染 Markdown
   
3. Git 部署
   □ output/ 目录初始化
   □ python manage.py push 命令
   □ 重试机制 (3 次)
```

**完成标志**: 可一键生成 + 推送到 GitHub Pages

---

## Phase 2.5: 前端 UI 设计 (新增)

> **用户反馈**: "设计一个美观、简洁、科技的网页UI" 应作为独立阶段

**目标**: 设计静态博客站点的完整 UI 体系

### 设计原则

| 原则 | 描述 |
|------|------|
| 美观 | 视觉协调，配色舒适，有设计感 |
| 简洁 | 信息层次清晰，无冗余元素 |
| 科技感 | 适合技术博客，代码高亮突出 |

### 任务清单

```yaml
1. 设计系统
   □ 配色方案 (主色、辅色、强调色)
   □ 字体选择 (中文/英文/代码)
   □ 间距与网格系统
   □ 组件设计语言

2. 页面设计
   □ 首页布局 (文章列表 + 侧边栏)
   □ 文章详情页 (阅读体验优化)
   □ 归档页 (时间线样式)
   □ 标签/分类页
   □ 说说页 (卡片流)
   □ 友链页
   □ 关于页

3. 组件设计
   □ 导航栏 (响应式)
   □ 文章卡片
   □ 分页组件
   □ 上一篇/下一篇导航
   □ 页脚

4. 样式实现
   □ 重构 site_templates/base.html
   □ 更新 all 组件模板
   □ 编写 custom.css
   □ 响应式适配 (移动端)
```

**完成标志**: 静态站点生成后，页面美观、简洁、有科技感
---

## 依赖清单

```txt
# requirements.txt
Django>=5.0
django-simpleui>=2024.1
Pillow>=10.0
markdown-it-py>=3.0
mdit-py-plugins>=0.4
pygments>=2.17
pyyaml>=6.0
python-slugify>=8.0
```

---

## 风险与缓解

| 风险 | 缓解措施 |
|------|----------|
| EasyMDE 集成复杂 | Phase 1 先用 textarea，Phase 2 再升级 |
| mermaid 渲染性能 | 前端渲染，仅加载必要页面 |
| Git 推送失败 | 提供重试机制 + 手动推送指引 |

---
- [ ] 国际化

---

## 阶段依赖关系

```
Phase 1 (骨架) ──→ Phase 2 (核心功能) ──→ Phase 2.5 (UI设计) ──→ Phase 3 (完善部署)
     │                   │                      │                    │
     └── Admin可用 ──────┴── 生成器可用 ─────────┴── 模板美观 ─────────┴── 可部署
```

---

## 关键决策记录

### 2026-03-25: 本地端入口页简化

**问题**: Phase 1 实现了完整的博客首页模板，但本地端不需要"好看"的页面。

**决策**: 
1. 本地端改为极简入口页 (portal.html)，仅提供"进入后台"按钮
2. site_templates/ 作为静态生成专用模板，不用于本地预览
3. 前端 UI 设计作为 Phase 2.5 独立阶段

**理由**: 核心定位是"本地撰写、生成页面、在线展示"，本地端只负责内容管理。
