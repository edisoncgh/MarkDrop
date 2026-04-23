// 在文章编辑页添加"保存并生成静态页面"按钮
document.addEventListener('DOMContentLoaded', function() {
    // 找到 Django admin 的提交按钮行
    var submitRow = document.querySelector('.submit-row');
    if (!submitRow) return;

    // 仅在 Post 编辑页生效
    var isPostPage = document.getElementById('id_content');
    if (!isPostPage) return;

    var saveBtn = submitRow.querySelector('input[name="_save"]');
    if (!saveBtn) return;

    // 创建"保存并生成"按钮
    var saveAndGenBtn = document.createElement('input');
    saveAndGenBtn.type = 'submit';
    saveAndGenBtn.name = '_save_and_generate';
    saveAndGenBtn.value = '保存并生成静态页面';
    saveAndGenBtn.className = 'default';
    saveAndGenBtn.style.cssText = 'background:#67c23a; border-color:#67c23a; color:#fff; margin-left:8px; cursor:pointer; padding:6px 16px; border-radius:4px;';

    saveBtn.parentNode.insertBefore(saveAndGenBtn, saveBtn.nextSibling);
});
