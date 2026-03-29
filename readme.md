# MarkDrop

> **Mark**down 写完，**Drop** 上线。

MarkDrop 是一个基于 Django 的静态博客生成器。在本地 WebUI 用 Markdown 自由地写博文，一键生成为纯静态 HTML 页面，然后推送到任意静态托管服务——当然也包括免费开放的 GitHub Pages。

## 功能特性

- **Markdown 撰写** — 支持 GFM 语法、代码高亮（Pygments）、Mermaid 图表、KaTeX 数学公式
- **深色/浅色主题** — 一键切换，状态持久化到 localStorage
- **响应式布局** — 桌面端与移动端自适应
- **静态生成** — `python manage.py generate` 输出纯 HTML，无服务端依赖
- **一键部署** — `python manage.py push` 推送到 GitHub Pages
- **内容管理** — Django Admin 后台，SimpleUI 美化界面

## 内容模型

| 模型 | 用途 |
|------|------|
| Post | 博文，支持分类/标签/Markdown 渲染/自动 slug |
| Moment | 说说，短内容随笔 |
| Category | 分类，自动生成分类归档页 |
| Tag | 标签，自动生成标签云和标签归档页 |
| FriendLink | 友情链接，支持排序和启用/禁用 |
| SiteConfig | 站点配置，键值对存储（标题、描述、作者等） |

## 页面结构

```
output/
├── index.html              # 首页（说说 + 最新博文）
├── posts.html              # 博文列表
├── archive.html            # 归档页（按时间排列）
├── moments.html            # 说说页
├── friends.html            # 友链页
├── about.html              # 关于页（含统计信息）
├── tags/index.html         # 标签云
├── tags/{slug}.html        # 单个标签归档
├── categories/{slug}.html  # 单个分类归档
├── posts/{year}/{slug}.html # 博文详情
└── static/                 # CSS / JS / vendor 资源
```

## 快速开始

### 环境要求

- Python 3.10+
- Git

### 安装

```bash
git clone https://github.com/<your-username>/EDGP.git
cd EDGP
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
```

### 本地运行

```bash
python manage.py runserver
```

访问 `http://127.0.0.1:8000/` 进入管理入口页，点击进入后台撰写内容。

### 生成静态站点

```bash
python manage.py generate
```

生成的文件位于 `output/` 目录。

### 部署到 GitHub Pages

```bash
# 首次：初始化 output 目录为独立 git 仓库
python manage.py init_output
cd output
git remote add origin <your-github-pages-repo-url>
git branch -M main
git push -u origin main
cd ..

# 后续：生成 + 推送
python manage.py generate
python manage.py push
```

## 项目结构

```
EDGP/
├── blog/                   # Django 博客应用
│   ├── models.py           # 内容模型（Post, Moment, FriendLink 等）
│   ├── admin.py            # Admin 后台配置
│   ├── views.py            # 本地端入口视图
│   ├── utils/
│   │   ├── generator.py    # 静态站点生成器
│   │   └── markdown.py     # Markdown 渲染器（支持 Mermaid/KaTeX）
│   ├── management/commands/
│   │   ├── generate.py     # python manage.py generate
│   │   ├── push.py         # python manage.py push
│   │   └── init_output.py  # python manage.py init_output
│   └── migrations/         # 数据库迁移
├── site_templates/         # 静态站点模板（用于生成）
│   ├── base.html
│   ├── components/         # 导航栏、页脚、上下篇等
│   └── pages/              # 各页面模板
├── local_templates/        # 本地管理端模板（入口页）
├── static_src/             # 静态站点资源
│   ├── css/main.css        # 设计系统（深色/浅色主题变量）
│   └── js/main.js          # 交互功能（主题切换、菜单、进度条等）
├── static/                 # 本地管理端静态资源 + vendor 库
├── edgp/                   # Django 项目配置
│   ├── settings.py
│   └── urls.py
├── output/                 # 生成的静态站点（独立 git 仓库）
└── docs/                   # 设计文档与评审记录
```

## 技术栈

| 层级 | 技术 |
|------|------|
| 后端 | Django 5.x, SQLite |
| 渲染 | markdown-it-py, Pygments, mdit-py-plugins |
| 前端 | 原生 CSS 变量系统, 原生 JavaScript |
| 数学 | KaTeX |
| 图表 | Mermaid |
| 后台 | django-simpleui |
| 部署 | GitHub Pages |

## 管理命令

| 命令 | 说明 |
|------|------|
| `python manage.py generate` | 生成全部静态页面 |
| `python manage.py push` | 提交并推送到 GitHub Pages（带重试） |
| `python manage.py init_output` | 初始化 output 目录为独立 git 仓库 |

## License

MIT