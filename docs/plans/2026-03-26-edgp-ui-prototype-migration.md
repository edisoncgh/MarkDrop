# EDGP UI 原型迁移实施计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 将 `E:\EDGP\prototype\` 的原型设计完整迁移到 EDGP_new 的 Django 模板系统，实现深色/浅色主题切换。

**Architecture:** 直接复制原型 CSS/JS 文件，重构 Django 模板使用原型 HTML 结构，保持 Django 模板语法。

**Tech Stack:** CSS3 (Custom Properties), Vanilla JavaScript, Django Templates

---

## 任务清单

### Task 1: CSS 样式迁移

**Files:**
- Delete: `static_src/css/variables.css`
- Delete: `static_src/css/base.css`
- Delete: `static_src/css/components.css`
- Delete: `static_src/css/layout.css`
- Delete: `static_src/css/responsive.css`
- Replace: `static_src/css/main.css` (用原型文件替换)
- Keep: `static_src/css/highlight.css` (保留现有)

**Step 1: 删除现有 CSS 文件（除 highlight.css）**

```bash
rm E:/EDGP_new/static_src/css/variables.css
rm E:/EDGP_new/static_src/css/base.css
rm E:/EDGP_new/static_src/css/components.css
rm E:/EDGP_new/static_src/css/layout.css
rm E:/EDGP_new/static_src/css/responsive.css
```

**Step 2: 复制原型 CSS 到项目**

复制 `E:\EDGP\prototype\css\main.css` 内容到 `E:\EDGP_new\static_src\css\main.css`

**Step 3: 添加 highlight.css 导入**

在 `main.css` 末尾添加：
```css
/* 代码高亮 */
@import url('highlight.css');
```

**Step 4: 验证**

运行：`python manage.py generate`
检查：output/static/css/main.css 是否正确复制

**Step 5: 提交**

```bash
git add static_src/css/
git commit -m "feat(ui): 迁移原型 CSS 设计系统，支持深色/浅色主题"
```

---

### Task 2: JavaScript 功能迁移

**Files:**
- Create: `static_src/js/main.js`

**Step 1: 创建 js 目录**

```bash
mkdir -p E:/EDGP_new/static_src/js
```

**Step 2: 复制原型 JS 到项目**

复制 `E:\EDGP\prototype\js\main.js` 内容到 `E:\EDGP_new\static_src\js\main.js`

**Step 3: 验证**

运行：`python manage.py generate`
检查：output/static/js/main.js 是否正确复制

**Step 4: 提交**

```bash
git add static_src/js/
git commit -m "feat(ui): 迁移原型 JavaScript 交互功能"
```

---

### Task 3: 更新 base.html 模板

**Files:**
- Modify: `site_templates/base.html`

**Step 1: 更新 base.html**

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{% block meta_description %}{{ site.description|default:'' }}{% endblock %}">
    {% include 'components/header.html' %}
    <title>{% block title %}{{ site.title|default:'EDGP Blog' }}{% endblock %}</title>
    <link rel="stylesheet" href="{{ static_prefix }}/css/main.css">
    {% block extra_head %}{% endblock %}
</head>
<body>
    {% include 'components/navbar.html' %}
    
    <main class="container">
        {% block content %}{% endblock %}
    </main>
    
    {% include 'components/footer.html' %}
    
    <script src="{{ static_prefix }}/js/main.js"></script>
    {% block extra_scripts %}{% endblock %}
</body>
</html>
```

**Step 2: 验证**

运行：`python manage.py generate`
检查：页面是否正确加载 CSS 和 JS

**Step 3: 提交**

```bash
git add site_templates/base.html
git commit -m "feat(ui): 更新 base.html，引用新样式和脚本"
```

---

### Task 4: 重构导航栏组件

**Files:**
- Modify: `site_templates/components/navbar.html`

**Step 1: 重构 navbar.html**

```html
<!-- site_templates/components/navbar.html -->
<nav class="navbar">
    <div class="container navbar-inner">
        <a href="{{ url_prefix }}index.html" class="navbar-brand">{{ site.title|default:'EDGP Blog' }}</a>
        <div class="navbar-actions">
            <button class="theme-toggle" onclick="toggleTheme()" title="切换主题">
                <svg class="icon-moon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
                </svg>
                <svg class="icon-sun" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="12" r="5"></circle>
                    <line x1="12" y1="1" x2="12" y2="3"></line>
                    <line x1="12" y1="21" x2="12" y2="23"></line>
                    <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>
                    <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>
                    <line x1="1" y1="12" x2="3" y2="12"></line>
                    <line x1="21" y1="12" x2="23" y2="12"></line>
                    <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>
                    <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>
                </svg>
            </button>
            <button class="navbar-toggle" onclick="toggleMenu()">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M3 12h18M3 6h18M3 18h18"></path>
                </svg>
            </button>
        </div>
        <ul class="navbar-menu" id="navMenu">
            <li><a href="{{ url_prefix }}index.html">首页</a></li>
            <li><a href="{{ url_prefix }}posts.html">博文</a></li>
            <li><a href="{{ url_prefix }}archive.html">归档</a></li>
            <li><a href="{{ url_prefix }}tags/">标签</a></li>
            <li><a href="{{ url_prefix }}moments.html">说说</a></li>
            <li><a href="{{ url_prefix }}friends.html">友链</a></li>
            <li><a href="{{ url_prefix }}about.html">关于</a></li>
        </ul>
    </div>
</nav>
```

**Step 2: 验证**

运行：`python manage.py generate`
检查：导航栏显示正确，主题切换按钮可见

**Step 3: 提交**

```bash
git add site_templates/components/navbar.html
git commit -m "feat(ui): 重构导航栏，添加主题切换按钮"
```

---

### Task 5: 重构页脚组件

**Files:**
- Modify: `site_templates/components/footer.html`

**Step 1: 重构 footer.html**

```html
<!-- site_templates/components/footer.html -->
<footer class="footer">
    <div class="container">
        <div class="footer-links">
            {% if site.url %}
            <a href="{{ site.url }}" target="_blank">网站</a>
            {% endif %}
            {% if site.email %}
            <a href="mailto:{{ site.email }}">邮箱</a>
            {% endif %}
        </div>
        <p>© {{ site.title|default:'EDGP Blog' }}. Powered by Django & GitHub Pages.</p>
    </div>
</footer>
```

**Step 2: 验证**

运行：`python manage.py generate`

**Step 3: 提交**

```bash
git add site_templates/components/footer.html
git commit -m "feat(ui): 重构页脚组件"
```

---

### Task 6: 重构首页

**Files:**
- Modify: `site_templates/pages/index.html`

**Step 1: 重构 index.html**

```html
{% extends 'base.html' %}

{% block title %}{{ site.title|default:'EDGP Blog' }}{% endblock %}

{% block content %}
<main class="container" style="padding-top: 3rem; padding-bottom: 3rem;">
    
    <!-- 说说区域 -->
    <section style="margin-bottom: 3rem;">
        <h2 style="font-size: 1.25rem; margin-bottom: 1.5rem; color: var(--color-text); display: flex; align-items: center; gap: 0.5rem;">
            <span>💭</span> 最新说说
            <a href="{{ url_prefix }}moments.html" style="font-size: 0.85rem; font-weight: normal; margin-left: auto;">查看全部 →</a>
        </h2>
        
        {% for moment in moments|slice:":2" %}
        <article class="moment-card" style="margin-bottom: 1rem;">
            <div class="moment-header">
                <div class="moment-avatar">{{ site.author|first|default:'B' }}</div>
                <div>
                    <div class="moment-author">{{ site.author|default:'博主' }}</div>
                    <time class="moment-time">{{ moment.created_at|date:"Y-m-d H:i" }}</time>
                </div>
            </div>
            <div class="moment-content">
                {{ moment.content_html|safe }}
            </div>
            {% if moment.images %}
            <div class="moment-images">
                {% for image in moment.images %}
                <img src="{{ image }}" alt="图片" class="moment-image">
                {% endfor %}
            </div>
            {% endif %}
        </article>
        {% empty %}
        <p class="empty-state">暂无说说</p>
        {% endfor %}
    </section>

    <!-- 博文区域 -->
    <section>
        <h2 style="font-size: 1.25rem; margin-bottom: 1.5rem; color: var(--color-text); display: flex; align-items: center; gap: 0.5rem;">
            <span>📝</span> 最新博文
            <a href="{{ url_prefix }}posts.html" style="font-size: 0.85rem; font-weight: normal; margin-left: auto;">查看全部 →</a>
        </h2>
        
        <div class="post-list">
            {% for post in posts|slice:":5" %}
            <article class="post-card">
                <h2 class="post-card-title">
                    <a href="{{ url_prefix }}posts/{{ post.published_at.year }}/{{ post.slug }}.html">{{ post.title }}</a>
                </h2>
                <div class="post-card-meta">
                    <span class="post-card-meta-item">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                            <line x1="16" y1="2" x2="16" y2="6"></line>
                            <line x1="8" y1="2" x2="8" y2="6"></line>
                            <line x1="3" y1="10" x2="21" y2="10"></line>
                        </svg>
                        {{ post.published_at|date:"Y-m-d" }}
                    </span>
                    {% if post.category %}
                    <a href="{{ url_prefix }}categories/{{ post.category.slug }}.html" class="category">{{ post.category.name }}</a>
                    {% endif %}
                </div>
                <p class="post-card-excerpt">{{ post.content|truncatewords:50|striptags }}</p>
                <div class="post-card-footer">
                    <div class="tags">
                        {% for tag in post.tags.all|slice:":3" %}
                        <a href="{{ url_prefix }}tags/{{ tag.slug }}.html" class="tag">{{ tag.name }}</a>
                        {% endfor %}
                    </div>
                    <a href="{{ url_prefix }}posts/{{ post.published_at.year }}/{{ post.slug }}.html" class="btn btn-secondary">阅读全文 →</a>
                </div>
            </article>
            {% empty %}
            <p class="empty-state">暂无博文</p>
            {% endfor %}
        </div>
    </section>

</main>
{% endblock %}
```

**Step 2: 验证**

运行：`python manage.py generate`
检查：首页显示说说区域和博文列表

**Step 3: 提交**

```bash
git add site_templates/pages/index.html
git commit -m "feat(ui): 重构首页，采用原型说说+博文布局"
```

---

### Task 7: 新建博文列表页

**Files:**
- Create: `site_templates/pages/posts.html`

**Step 1: 创建 posts.html**

```html
{% extends 'base.html' %}

{% block title %}博文 - {{ site.title|default:'EDGP Blog' }}{% endblock %}

{% block content %}
<main class="container" style="padding-top: 3rem; padding-bottom: 3rem;">
    <header class="page-header">
        <h1 class="page-title">博文</h1>
        <p class="page-description">所有文章列表</p>
    </header>
    
    <div class="post-list">
        {% for post in posts %}
        <article class="post-card">
            <h2 class="post-card-title">
                <a href="{{ url_prefix }}posts/{{ post.published_at.year }}/{{ post.slug }}.html">{{ post.title }}</a>
            </h2>
            <div class="post-card-meta">
                <span class="post-card-meta-item">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                        <line x1="16" y1="2" x2="16" y2="6"></line>
                        <line x1="8" y1="2" x2="8" y2="6"></line>
                        <line x1="3" y1="10" x2="21" y2="10"></line>
                    </svg>
                    {{ post.published_at|date:"Y-m-d" }}
                </span>
                {% if post.category %}
                <a href="{{ url_prefix }}categories/{{ post.category.slug }}.html" class="category">{{ post.category.name }}</a>
                {% endif %}
            </div>
            <p class="post-card-excerpt">{{ post.content|truncatewords:50|striptags }}</p>
            <div class="post-card-footer">
                <div class="tags">
                    {% for tag in post.tags.all|slice:":3" %}
                    <a href="{{ url_prefix }}tags/{{ tag.slug }}.html" class="tag">{{ tag.name }}</a>
                    {% endfor %}
                </div>
                <a href="{{ url_prefix }}posts/{{ post.published_at.year }}/{{ post.slug }}.html" class="btn btn-secondary">阅读全文 →</a>
            </div>
        </article>
        {% empty %}
        <p class="empty-state">暂无博文</p>
        {% endfor %}
    </div>
</main>
{% endblock %}
```

**Step 2: 验证**

运行：`python manage.py generate`
检查：posts.html 正确生成

**Step 3: 提交**

```bash
git add site_templates/pages/posts.html
git commit -m "feat(ui): 新建博文列表页"
```

---

### Task 8: 重构博文详情页

**Files:**
- Modify: `site_templates/pages/post.html`

**Step 1: 重构 post.html**

参照原型 `prototype/posts/*.html` 结构，保持现有 Django 模板语法，更新 HTML 结构和 CSS 类名。

**Step 2: 验证**

运行：`python manage.py generate`
检查：博文详情页显示正确

**Step 3: 提交**

```bash
git add site_templates/pages/post.html
git commit -m "feat(ui): 重构博文详情页"
```

---

### Task 9: 重构归档页

**Files:**
- Modify: `site_templates/pages/archive.html`

**Step 1: 重构 archive.html**

参照原型 `prototype/archive.html` 结构，使用 `.archive-list`, `.archive-year`, `.archive-item` 等类名。

**Step 2: 验证**

运行：`python manage.py generate`

**Step 3: 提交**

```bash
git add site_templates/pages/archive.html
git commit -m "feat(ui): 重构归档页"
```

---

### Task 10: 重构说说页

**Files:**
- Modify: `site_templates/pages/moments.html`

**Step 1: 重构 moments.html**

参照原型 `prototype/moments.html` 结构，使用 `.moments-list`, `.moment-card` 等类名。

**Step 2: 验证**

运行：`python manage.py generate`

**Step 3: 提交**

```bash
git add site_templates/pages/moments.html
git commit -m "feat(ui): 重构说说页"
```

---

### Task 11: 重构友链页

**Files:**
- Modify: `site_templates/pages/friends.html`
- Modify: `site_templates/components/friend_link.html`

**Step 1: 重构 friends.html 和 friend_link.html**

参照原型 `prototype/friends.html` 结构，使用 `.friends-grid`, `.friend-card` 等类名。

**Step 2: 验证**

运行：`python manage.py generate`

**Step 3: 提交**

```bash
git add site_templates/pages/friends.html site_templates/components/friend_link.html
git commit -m "feat(ui): 重构友链页"
```

---

### Task 12: 重构关于页

**Files:**
- Modify: `site_templates/pages/about.html`

**Step 1: 重构 about.html**

参照原型 `prototype/about.html` 结构，使用 `.about-header`, `.about-content`, `.about-stats` 等类名。

**Step 2: 验证**

运行：`python manage.py generate`

**Step 3: 提交**

```bash
git add site_templates/pages/about.html
git commit -m "feat(ui): 重构关于页"
```

---

### Task 13: 重构标签页

**Files:**
- Modify: `site_templates/pages/tags.html`
- Modify: `site_templates/pages/tag.html`

**Step 1: 重构 tags.html**

参照原型 `prototype/tags/index.html` 结构，使用 `.tags-cloud` 类名。

**Step 2: 重构 tag.html**

更新样式类名，保持 Django 模板逻辑。

**Step 3: 验证**

运行：`python manage.py generate`

**Step 4: 提交**

```bash
git add site_templates/pages/tags.html site_templates/pages/tag.html
git commit -m "feat(ui): 重构标签页"
```

---

### Task 14: 重构分类页

**Files:**
- Modify: `site_templates/pages/category.html`

**Step 1: 重构 category.html**

更新样式类名，保持 Django 模板逻辑。

**Step 2: 验证**

运行：`python manage.py generate`

**Step 3: 提交**

```bash
git add site_templates/pages/category.html
git commit -m "feat(ui): 重构分类页"
```

---

### Task 15: 最终验证

**Files:**
- All modified files

**Step 1: 生成完整静态站点**

运行：`python manage.py generate`

**Step 2: 手动验证所有页面**

在浏览器中打开以下页面验证：
- output/index.html - 首页
- output/posts.html - 博文列表
- output/archive.html - 归档页
- output/tags/index.html - 标签页
- output/moments.html - 说说页
- output/friends.html - 友链页
- output/about.html - 关于页
- output/posts/*/*.html - 博文详情页

**Step 3: 验证功能**

- 主题切换是否正常工作
- 导航栏链接是否正确
- 移动端菜单是否正常
- 返回顶部按钮是否显示

**Step 4: 最终提交**

```bash
git add .
git commit -m "feat(ui): 完成原型 UI 迁移，支持深色/浅色主题"
```

---

## 验证清单

```yaml
□ CSS 样式迁移
   □ main.css 包含完整设计系统
   □ highlight.css 保留
   □ 所有页面样式正确

□ JavaScript 功能
   □ main.js 包含所有交互功能
   □ 主题切换正常
   □ 移动端菜单正常
   □ 返回顶部按钮正常

□ 导航栏
   □ 主题切换按钮可见
   □ 移动端折叠菜单正常
   □ 所有链接正确

□ 首页
   □ 说说区域显示
   □ 博文列表显示
   □ 无侧边栏

□ 博文列表页
   □ posts.html 正确生成
   □ 导航栏链接正确

□ 其他页面
   □ 归档页样式正确
   □ 说说页样式正确
   □ 友链页样式正确
   □ 关于页样式正确
   □ 标签页样式正确
   □ 博文详情页样式正确
```

---

## 注意事项

1. **URL 路由问题**：
   - 首页链接使用 `index.html`
   - 注意各页面的相对路径层级

2. **样式加载问题**：
   - 确保 `{{ static_prefix }}/css/main.css` 路径正确
   - 验证生成后 CSS/JS 文件复制到 output 目录

3. **不引入新问题**：
   - 每个 Task 完成后运行 `python manage.py generate`
   - 保持 Django 模板语法正确
   - 频繁提交，便于回滚