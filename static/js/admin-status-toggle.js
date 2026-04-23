// Status Toggle Switch — 将 Django admin 的 <select id="id_status"> 替换为 toggle switch
document.addEventListener('DOMContentLoaded', function() {
    var statusSelect = document.getElementById('id_status');
    if (!statusSelect) return;

    var options = statusSelect.querySelectorAll('option');
    if (options.length < 2) return;

    // 创建容器
    var wrapper = document.createElement('div');
    wrapper.className = 'status-toggle-wrapper';

    // 创建 toggle label
    var label = document.createElement('label');
    label.className = 'status-toggle';

    // 创建 checkbox
    var checkbox = document.createElement('input');
    checkbox.type = 'checkbox';
    checkbox.className = 'status-toggle-input';

    // 初始状态：published = checked
    if (statusSelect.value === 'published') {
        checkbox.checked = true;
    }

    // 创建 slider
    var slider = document.createElement('span');
    slider.className = 'status-toggle-slider';

    // 创建状态文字
    var statusText = document.createElement('span');
    statusText.className = 'status-toggle-text';
    statusText.textContent = checkbox.checked ? '已发布' : '草稿';

    label.appendChild(checkbox);
    label.appendChild(slider);

    wrapper.appendChild(label);
    wrapper.appendChild(statusText);

    // 隐藏原始 select，插入 toggle
    statusSelect.style.display = 'none';
    statusSelect.parentNode.insertBefore(wrapper, statusSelect.nextSibling);

    // 双向同步
    checkbox.addEventListener('change', function() {
        if (checkbox.checked) {
            statusSelect.value = 'published';
            statusText.textContent = '已发布';
        } else {
            statusSelect.value = 'draft';
            statusText.textContent = '草稿';
        }
        var event = new Event('change', { bubbles: true });
        statusSelect.dispatchEvent(event);
    });
});
