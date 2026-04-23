// Category 内联创建组件
document.addEventListener('DOMContentLoaded', function() {
    var categorySelect = document.getElementById('id_category');
    if (!categorySelect) return;

    // 在 select 旁边添加 + 按钮
    var wrapper = document.createElement('div');
    wrapper.style.display = 'inline-block';
    wrapper.style.marginLeft = '8px';
    wrapper.style.verticalAlign = 'middle';

    var addBtn = document.createElement('button');
    addBtn.type = 'button';
    addBtn.className = 'btn btn-sm btn-default';
    addBtn.textContent = '+ 新建分类';
    addBtn.style.padding = '4px 12px';
    addBtn.style.fontSize = '13px';
    addBtn.style.cursor = 'pointer';
    addBtn.onclick = showCreateDialog;
    wrapper.appendChild(addBtn);

    categorySelect.parentNode.insertBefore(wrapper, categorySelect.nextSibling);

    function showCreateDialog() {
        var name = prompt('请输入新分类名称：');
        if (!name || !name.trim()) return;

        var description = prompt('分类描述（可选）：') || '';

        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/api/category-quick-create/', true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.setRequestHeader('X-CSRFToken', getCSRFToken());
        xhr.onload = function() {
            if (xhr.status === 200) {
                var data = JSON.parse(xhr.responseText);
                if (data.success) {
                    // 添加新选项并选中
                    var option = document.createElement('option');
                    option.value = data.category.id;
                    option.textContent = data.category.name;
                    categorySelect.appendChild(option);
                    categorySelect.value = data.category.id;
                    alert('分类「' + data.category.name + '」创建成功！');
                } else {
                    alert('创建失败：' + data.error);
                }
            } else {
                alert('请求失败，请重试');
            }
        };
        xhr.send(JSON.stringify({ name: name.trim(), description: description.trim() }));
    }

    function getCSRFToken() {
        var cookie = document.cookie.split('; ').find(function(row) {
            return row.startsWith('csrftoken=');
        });
        return cookie ? cookie.split('=')[1] : '';
    }
});
