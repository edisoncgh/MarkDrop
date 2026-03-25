"""
Markdown 渲染工具
Phase 1: 基础渲染
Phase 2: 添加 mermaid, LaTeX, 代码高亮支持
"""

from markdown_it import MarkdownIt
from pygments import highlight
from pygments.lexers import get_lexer_by_name, TextLexer
from pygments.formatters import HtmlFormatter


def render_markdown(text: str) -> str:
    """
    渲染 Markdown 文本为 HTML

    Args:
        text: Markdown 文本

    Returns:
        渲染后的 HTML 字符串
    """
    if not text:
        return ""

    # Phase 1: 基础渲染
    md = MarkdownIt("commonmark", {"html": True, "linkify": True})
    md.enable("table")
    md.enable("strikethrough")

    # 自定义代码块处理
    def code_block_renderer(tokens, idx, options, env):
        token = tokens[idx]
        info = token.info.strip() if token.info else ""
        code = token.content

        if info:
            try:
                lexer = get_lexer_by_name(info, stripall=True)
            except Exception:
                lexer = TextLexer()
        else:
            lexer = TextLexer()

        formatter = HtmlFormatter(cssclass="highlight", linenos=False)
        return highlight(code, lexer, formatter)

    # 注册自定义渲染器
    md.add_render_rule("fence", code_block_renderer)

    return md.render(text)
