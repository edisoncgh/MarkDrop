// EasyMDE 编辑器初始化
document.addEventListener('DOMContentLoaded', function() {
    const contentTextarea = document.getElementById('id_content');
    if (contentTextarea && typeof EasyMDE !== 'undefined') {
        const easyMDE = new EasyMDE({
            element: contentTextarea,
            spellChecker: false,
            autosave: {
                enabled: true,
                uniqueId: 'edgp-post-content',
                delay: 5000,
            },
            placeholder: '在此输入 Markdown 内容...',
            status: ['autosave', 'lines', 'words'],
            toolbar: [
                'bold', 'italic', 'heading', '|',
                'quote', 'unordered-list', 'ordered-list', '|',
                'link', 'image', 'code', '|',
                'preview', 'side-by-side', 'fullscreen', '|',
                'guide'
            ],
            previewRender: function(plainText) {
                return plainText; // Phase 2: 使用后端渲染 API
            }
        });
    }
});