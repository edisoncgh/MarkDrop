// EasyMDE 编辑器初始化 + 实时预览
document.addEventListener('DOMContentLoaded', function() {
    var contentTextarea = document.getElementById('id_content');
    if (!contentTextarea || typeof EasyMDE === 'undefined') return;

    function getCSRFToken() {
        var cookie = document.cookie.split('; ').find(function(row) {
            return row.startsWith('csrftoken=');
        });
        return cookie ? cookie.split('=')[1] : '';
    }

    var mermaidButton = {
        name: 'mermaid',
        action: function(editor) {
            var cm = editor.codemirror;
            var cursor = cm.getCursor();
            cm.replaceRange('\n```mermaid\ngraph TD\n    A-->B\n```\n', cursor);
        },
        className: 'fa fa-project-diagram',
        title: '插入 Mermaid 图表'
    };

    var latexButton = {
        name: 'latex',
        action: function(editor) {
            var cm = editor.codemirror;
            var cursor = cm.getCursor();
            cm.replaceRange('\n$$\nx^2 + y^2 = z^2\n$$\n', cursor);
        },
        className: 'fas fa-square-root-variable',
        title: '插入 LaTeX 公式'
    };

    var easyMDE = new EasyMDE({
        element: contentTextarea,
        spellChecker: false,
        autosave: {
            enabled: true,
            uniqueId: 'edgp-post-content',
            delay: 5000
        },
        placeholder: '在此输入 Markdown 内容...',
        status: ['autosave', 'lines', 'words'],
        toolbar: [
            'bold', 'italic', 'heading', '|',
            'quote', 'unordered-list', 'ordered-list', '|',
            'link', 'image', 'code', mermaidButton, latexButton, '|',
            'preview', 'side-by-side', 'fullscreen', '|',
            'guide'
        ],
        previewRender: function(plainText, preview) {
            var xhr = new XMLHttpRequest();
            xhr.open('POST', '/api/markdown-preview/', true);
            xhr.setRequestHeader('Content-Type', 'application/json');
            xhr.setRequestHeader('X-CSRFToken', getCSRFToken());
            xhr.onload = function() {
                if (xhr.status === 200) {
                    try {
                        preview.innerHTML = JSON.parse(xhr.responseText).html;
                    } catch (e) {
                        preview.innerHTML = '<p>预览加载失败</p>';
                    }
                } else {
                    preview.innerHTML = '<p>预览请求失败 (' + xhr.status + ')</p>';
                }
            };
            xhr.onerror = function() {
                preview.innerHTML = '<p>网络错误，无法加载预览</p>';
            };
            xhr.send(JSON.stringify({ content: plainText }));
            return '<p>加载预览中...</p>';
        }
    });

    // ---- 实时预览面板 ----
    var editorContainer = contentTextarea.closest('.EasyMDEContainer') || contentTextarea.parentNode;

    var previewWrapper = document.createElement('div');
    previewWrapper.className = 'live-preview-wrapper';

    var previewHeader = document.createElement('div');
    previewHeader.className = 'live-preview-header';

    var previewTitle = document.createElement('span');
    previewTitle.textContent = '实时预览';

    var previewToggle = document.createElement('span');
    previewToggle.className = 'live-preview-toggle';
    previewToggle.textContent = '收起';

    previewHeader.appendChild(previewTitle);
    previewHeader.appendChild(previewToggle);

    var previewBody = document.createElement('div');
    previewBody.className = 'live-preview-body';

    previewWrapper.appendChild(previewHeader);
    previewWrapper.appendChild(previewBody);

    editorContainer.parentNode.insertBefore(previewWrapper, editorContainer.nextSibling);

    var previewVisible = true;

    previewToggle.addEventListener('click', function() {
        previewVisible = !previewVisible;
        previewBody.style.display = previewVisible ? '' : 'none';
        previewToggle.textContent = previewVisible ? '收起' : '展开';
    });

    // 防抖渲染
    var renderTimer = null;

    function renderLivePreview() {
        clearTimeout(renderTimer);
        renderTimer = setTimeout(function() {
            var content = easyMDE.value();
            if (!content.trim()) {
                previewBody.innerHTML = '';
                return;
            }
            previewBody.classList.add('loading');
            var xhr = new XMLHttpRequest();
            xhr.open('POST', '/api/markdown-preview/', true);
            xhr.setRequestHeader('Content-Type', 'application/json');
            xhr.setRequestHeader('X-CSRFToken', getCSRFToken());
            xhr.onload = function() {
                previewBody.classList.remove('loading');
                if (xhr.status === 200) {
                    try {
                        previewBody.innerHTML = JSON.parse(xhr.responseText).html;
                    } catch (e) {
                        // ignore parse error
                    }
                }
            };
            xhr.onerror = function() {
                previewBody.classList.remove('loading');
            };
            xhr.send(JSON.stringify({ content: content }));
        }, 300);
    }

    easyMDE.codemirror.on('change', renderLivePreview);

    // 首次加载时渲染已有内容
    if (easyMDE.value().trim()) {
        renderLivePreview();
    }
});
