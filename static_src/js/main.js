/**
 * EDGP Blog - Main JavaScript
 * 简洁的交互脚本，确保零外部依赖
 */

// 移动端菜单切换
function toggleMenu() {
  const menu = document.getElementById('navMenu');
  if (menu) {
    menu.classList.toggle('active');
  }
}

// ========================================
// 主题切换功能
// ========================================

// 获取当前主题
function getCurrentTheme() {
  return localStorage.getItem('theme') || 'dark';
}

// 设置主题
function setTheme(theme) {
  document.documentElement.setAttribute('data-theme', theme);
  localStorage.setItem('theme', theme);
}

// 切换主题
function toggleTheme() {
  const currentTheme = getCurrentTheme();
  const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
  setTheme(newTheme);
}

// 初始化主题
function initTheme() {
  const savedTheme = localStorage.getItem('theme');
  if (savedTheme) {
    setTheme(savedTheme);
  } else {
    // 默认使用深色主题
    setTheme('dark');
  }
}

// 点击菜单项后关闭菜单（移动端）
document.addEventListener('DOMContentLoaded', function() {
  const menuLinks = document.querySelectorAll('.navbar-menu a');
  menuLinks.forEach(link => {
    link.addEventListener('click', function() {
      const menu = document.getElementById('navMenu');
      if (menu && window.innerWidth <= 768) {
        menu.classList.remove('active');
      }
    });
  });
});

// 平滑滚动到锚点
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function(e) {
    const href = this.getAttribute('href');
    if (href !== '#') {
      e.preventDefault();
      const target = document.querySelector(href);
      if (target) {
        target.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
      }
    }
  });
});

// 图片懒加载（可选）
function lazyLoadImages() {
  const images = document.querySelectorAll('img[data-src]');
  const observer = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const img = entry.target;
        img.src = img.dataset.src;
        img.removeAttribute('data-src');
        observer.unobserve(img);
      }
    });
  });

  images.forEach(img => observer.observe(img));
}

// 代码块复制功能（可选）
function addCopyButtons() {
  const codeBlocks = document.querySelectorAll('pre code');
  codeBlocks.forEach(block => {
    const pre = block.parentElement;
    const button = document.createElement('button');
    button.className = 'copy-btn';
    button.textContent = '复制';
    button.style.cssText = `
      position: absolute;
      top: 8px;
      right: 8px;
      padding: 4px 8px;
      font-size: 12px;
      background: var(--color-bg-tertiary);
      color: var(--color-text-secondary);
      border: 1px solid var(--color-border);
      border-radius: 4px;
      cursor: pointer;
      opacity: 0;
      transition: opacity 0.2s;
    `;

    pre.style.position = 'relative';
    pre.appendChild(button);

    pre.addEventListener('mouseenter', () => button.style.opacity = '1');
    pre.addEventListener('mouseleave', () => button.style.opacity = '0');

    button.addEventListener('click', async () => {
      try {
        await navigator.clipboard.writeText(block.textContent);
        button.textContent = '已复制';
        setTimeout(() => button.textContent = '复制', 2000);
      } catch (err) {
        console.error('复制失败:', err);
      }
    });
  });
}

// 返回顶部按钮（可选）
function addBackToTop() {
  const button = document.createElement('button');
  button.innerHTML = '↑';
  button.className = 'back-to-top';
  button.style.cssText = `
    position: fixed;
    bottom: 30px;
    right: 30px;
    width: 44px;
    height: 44px;
    border-radius: 50%;
    background: var(--color-bg-secondary);
    color: var(--color-text);
    border: 1px solid var(--color-border);
    font-size: 20px;
    cursor: pointer;
    opacity: 0;
    visibility: hidden;
    transition: all 0.3s;
    z-index: 99;
  `;

  document.body.appendChild(button);

  window.addEventListener('scroll', () => {
    if (window.scrollY > 300) {
      button.style.opacity = '1';
      button.style.visibility = 'visible';
    } else {
      button.style.opacity = '0';
      button.style.visibility = 'hidden';
    }
  });

  button.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
}

// 阅读进度条（可选）
function addReadingProgress() {
  const progressBar = document.createElement('div');
  progressBar.style.cssText = `
    position: fixed;
    top: 0;
    left: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--color-accent), var(--color-success));
    z-index: 1000;
    transition: width 0.1s;
  `;
  document.body.appendChild(progressBar);

  window.addEventListener('scroll', () => {
    const scrollTop = window.scrollY;
    const docHeight = document.documentElement.scrollHeight - window.innerHeight;
    const progress = (scrollTop / docHeight) * 100;
    progressBar.style.width = progress + '%';
  });
}

// 初始化
document.addEventListener('DOMContentLoaded', function() {
  // 检查是否在博文页面
  const isPostPage = document.querySelector('.post-content');
  
  if (isPostPage) {
    // 博文页面添加额外功能
    addCopyButtons();
    addReadingProgress();
  }

  // 全局功能
  addBackToTop();

  // 初始化主题
  initTheme();

  // 如果有懒加载图片
  if (document.querySelector('img[data-src]')) {
    lazyLoadImages();
  }
});

// 导出函数供全局使用
window.toggleMenu = toggleMenu;
window.toggleTheme = toggleTheme;
