# EDGP UI 重构设计文档 - 基于原型迁移

**日期**: 2026-03-26
**原型路径**: `E:\EDGP\prototype\`
**目标**: 将高完成度的原型设计迁移到 EDGP_new 的 Django 模板系统

---

## 设计决策

### 1. 主题切换功能
**决策**: 完整实现深色/浅色主题切换
- 深色主题为默认
- 用户可通过按钮自由切换
- 主题状态存储在 localStorage

### 2. 首页布局
**决策**: 完全采用原型布局
- 顶部：最新说说区域（2-3条）
- 下部：最新博文区域（文章卡片列表）
- 移除现有侧边栏

### 3. 博文列表页
**决策**: 新建独立博文列表页
- 创建 `posts.html`
- 导航栏添加"博文"链接

### 4. JavaScript 功能
**决策**: 全部迁移
- 主题切换
- 移动端菜单
- 返回顶部按钮
- 阅读进度条（博文页）
- 代码块复制按钮

---

## 文件结构

### CSS 文件
```
static_src/css/
├── main.css          # 原型完整样式（从 prototype/css/main.css 复制）
└── highlight.css     # 代码高亮（保留现有）
```

### JavaScript 文件
```
static_src/js/
└── main.js           # 交互功能（从 prototype/js/main.js 复制）
```

### 模板文件
```
site_templates/
├── base.html         # 更新：样式和脚本引用
├── components/
│   ├── navbar.html   # 更新：添加主题切换按钮
│   ├── footer.html   # 更新：原型样式
│   ├── friend_link.html
│   └── prev_next.html
└── pages/
    ├── index.html    # 重构：说说+博文布局
    ├── posts.html    # 新建：博文列表页
    ├── archive.html  # 重构：原型样式
    ├── moments.html  # 重构：原型样式
    ├── friends.html  # 重构：原型样式
    ├── about.html    # 重构：原型样式
    ├── tags.html     # 重构：标签云
    ├── tag.html      # 更新样式
    ├── category.html # 更新样式
    └── post.html     # 重构：博文详情页
```

---

## 关键注意事项

### URL 路由问题
- 首页链接使用 `index.html` 而非空字符串
- 注意各页面的相对路径层级
- 使用 `{{ url_prefix }}` 处理路径前缀

### 样式加载问题
- CSS 路径：`{{ static_prefix }}/css/main.css`
- JS 路径：`{{ static_prefix }}/js/main.js`
- 验证生成后文件复制到 output 目录

### 不引入新问题
- 每个文件修改后立即运行 `python manage.py generate` 验证
- 保持 Django 模板语法正确
- 确保 CSS/JS 变量引用正确

---

## 原型设计特点

### CSS 变量系统
- 完整的颜色变量（深色/浅色两套）
- 间距、圆角、阴影变量
- 响应式断点

### 组件样式
- 导航栏：sticky 定位、毛玻璃效果
- 博文卡片：边框悬停效果
- 说说卡片：左侧渐变边条
- 友链卡片：头像+信息网格
- 标签：圆角徽章样式

### 交互功能
- 主题切换：零外部依赖
- 返回顶部：滚动显示/隐藏
- 阅读进度：顶部渐变进度条
- 代码复制：悬停显示按钮