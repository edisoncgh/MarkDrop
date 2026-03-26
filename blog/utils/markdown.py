"""
Markdown 渲染工具
支持：基础语法、mermaid 图表、LaTeX 公式、代码高亮
"""

from markdown_it import MarkdownIt
from mdit_py_plugins.front_matter import front_matter_plugin
from mdit_py_plugins.footnote import footnote_plugin
from pygments import highlight
from pygments.lexers import get_lexer_by_name, TextLexer
from pygments.formatters import HtmlFormatter
import re


class MarkdownRenderer:
    """Markdown 渲染器"""

    def __init__(self):
        self.md = MarkdownIt("commonmark", {"html": True, "linkify": True})
        self.md.enable("table")
        self.md.enable("strikethrough")
        self.md.use(front_matter_plugin)
        self.md.use(footnote_plugin)

        # 自定义 fence 渲染
        self.md.add_render_rule("fence", self._render_fence)

    def _render_fence(self, tokens, idx, options, env):
        """自定义代码块渲染"""
        token = tokens[idx]
        info = token.info.strip().lower() if token.info else ""
        code = token.content

        # mermaid 图表 - 保留换行符
        if info == "mermaid":
            # 不处理 code，直接输出原始内容
            return f'<div class="mermaid">{code}</div>\n'

        # LaTeX 公式块 - 保留换行符
        if info in ["math", "latex", "katex"]:
            return f'<div class="katex-display">{code}</div>\n'
        # 代码高亮
        if info:
            try:
                lexer = get_lexer_by_name(info, stripall=True)
            except Exception:
                lexer = TextLexer()
        else:
            lexer = TextLexer()

        formatter = HtmlFormatter(cssclass="highlight", linenos=False, nowrap=False)
        return highlight(code, lexer, formatter)

    def render(self, text: str) -> str:
        """渲染 Markdown 文本"""
        if not text:
            return ""
        return self.md.render(text)


# 全局渲染器实例
_renderer = MarkdownRenderer()


def render_markdown(text: str) -> str:
    """
    渲染 Markdown 文本为 HTML

    Args:
        text: Markdown 文本

    Returns:
        渲染后的 HTML 字符串
    """
    return _renderer.render(text)
