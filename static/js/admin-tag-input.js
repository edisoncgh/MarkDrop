// Tag 选择器组件 — 替换 Django 默认的 filter_horizontal
// 利用 AJAX 实现 autocomplete + 内联创建
document.addEventListener('DOMContentLoaded', function() {
    var tagSelect = document.getElementById('id_tags');
    if (!tagSelect) return;

    var selectorBox = tagSelect.closest('.selector');
    if (selectorBox) selectorBox.style.display = 'none';

    var container = document.createElement('div');
    container.className = 'tag-input-container';

    var selectedArea = document.createElement('div');
    selectedArea.id = 'tag-selected-area';
    selectedArea.style.cssText = 'display:flex; flex-wrap:wrap; gap:6px;';
    container.appendChild(selectedArea);

    var input = document.createElement('input');
    input.type = 'text';
    input.placeholder = '输入标签名搜索或创建...';
    container.appendChild(input);

    var dropdown = document.createElement('div');
    dropdown.className = 'tag-dropdown';
    document.body.appendChild(dropdown);

    if (selectorBox) {
        selectorBox.parentNode.insertBefore(container, selectorBox.nextSibling);
    }

    // 点击容器时聚焦输入框
    container.addEventListener('click', function(e) {
        if (e.target === container || e.target === selectedArea) {
            input.focus();
        }
    });

    function loadSelectedTags() {
        selectedArea.innerHTML = '';
        tagSelect.querySelectorAll('option:selected').forEach(function(opt) {
            addTagChip(opt.value, opt.textContent);
        });
    }

    function addTagChip(id, name) {
        var chip = document.createElement('span');
        chip.className = 'tag-chip';
        chip.dataset.tagId = id;

        var nameSpan = document.createElement('span');
        nameSpan.textContent = name;
        chip.appendChild(nameSpan);

        var removeBtn = document.createElement('span');
        removeBtn.className = 'tag-chip-remove';
        removeBtn.textContent = '×';
        removeBtn.onclick = function() {
            var option = tagSelect.querySelector('option[value="' + id + '"]');
            if (option) {
                option.selected = false;
                triggerChange(tagSelect);
            }
            chip.remove();
        };
        chip.appendChild(removeBtn);

        selectedArea.appendChild(chip);
    }

    function triggerChange(el) {
        el.dispatchEvent(new Event('change', { bubbles: true }));
    }

    var searchTimer = null;
    input.addEventListener('input', function() {
        clearTimeout(searchTimer);
        searchTimer = setTimeout(function() {
            searchTags(input.value.trim());
        }, 300);
    });

    function searchTags(query) {
        var xhr = new XMLHttpRequest();
        xhr.open('GET', '/api/tag-search/?q=' + encodeURIComponent(query), true);
        xhr.onload = function() {
            if (xhr.status === 200) {
                showDropdown(JSON.parse(xhr.responseText).tags, query);
            }
        };
        xhr.send();
    }

    function showDropdown(tags, query) {
        dropdown.innerHTML = '';
        if (tags.length === 0 && query) {
            dropdown.appendChild(createDropdownCreateItem(query));
        } else {
            tags.forEach(function(tag) {
                var item = document.createElement('div');
                item.className = 'tag-dropdown-item';
                var isSelected = tagSelect.querySelector('option[value="' + tag.id + '"]');
                if (isSelected && isSelected.selected) {
                    item.classList.add('is-selected');
                }
                item.innerHTML = '<span>' + tag.name + '</span><span class="tag-count">' + tag.post_count + '篇</span>';
                item.onclick = function() { selectTag(tag.id, tag.name); };
                dropdown.appendChild(item);
            });
            if (query) {
                var exactMatch = tags.some(function(t) { return t.name === query; });
                if (!exactMatch) {
                    dropdown.appendChild(createDropdownCreateItem(query));
                }
            }
        }
        positionDropdown();
        dropdown.style.display = 'block';
    }

    function createDropdownCreateItem(query) {
        var item = document.createElement('div');
        item.className = 'tag-dropdown-create';
        item.textContent = '+ 创建新标签「' + query + '」';
        item.onclick = function() { createTag(query); };
        return item;
    }

    function positionDropdown() {
        var rect = input.getBoundingClientRect();
        dropdown.style.left = rect.left + 'px';
        dropdown.style.top = (rect.bottom + 4) + 'px';
        dropdown.style.width = rect.width + 'px';
        dropdown.style.minWidth = '250px';
    }

    function selectTag(id, name) {
        var option = tagSelect.querySelector('option[value="' + id + '"]');
        if (option) {
            option.selected = true;
            triggerChange(tagSelect);
            addTagChip(id, name);
        }
        input.value = '';
        dropdown.style.display = 'none';
    }

    function createTag(name) {
        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/api/tag-quick-create/', true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.setRequestHeader('X-CSRFToken', getCSRFToken());
        xhr.onload = function() {
            if (xhr.status === 200) {
                var data = JSON.parse(xhr.responseText);
                if (data.success) {
                    var option = document.createElement('option');
                    option.value = data.tag.id;
                    option.textContent = data.tag.name;
                    option.selected = true;
                    tagSelect.appendChild(option);
                    addTagChip(data.tag.id, data.tag.name);
                    triggerChange(tagSelect);
                } else {
                    alert('创建失败：' + data.error);
                }
            }
        };
        xhr.send(JSON.stringify({ name: name }));
        input.value = '';
        dropdown.style.display = 'none';
    }

    input.addEventListener('keydown', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            var firstItem = dropdown.querySelector('div');
            if (firstItem) firstItem.click();
        }
        if (e.key === 'Backspace' && input.value === '') {
            var lastChip = selectedArea.lastElementChild;
            if (lastChip) {
                var tagId = lastChip.dataset.tagId;
                var option = tagSelect.querySelector('option[value="' + tagId + '"]');
                if (option) {
                    option.selected = false;
                    triggerChange(tagSelect);
                }
                lastChip.remove();
            }
        }
    });

    document.addEventListener('click', function(e) {
        if (!container.contains(e.target) && e.target !== dropdown) {
            dropdown.style.display = 'none';
        }
    });

    function getCSRFToken() {
        var cookie = document.cookie.split('; ').find(function(row) {
            return row.startsWith('csrftoken=');
        });
        return cookie ? cookie.split('=')[1] : '';
    }

    loadSelectedTags();
});
