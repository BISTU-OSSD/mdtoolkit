"""toc —— 为 Markdown 生成/更新目录(组长模块)。

解析文档中的 ATX 标题(# ~ ######),生成带缩进的锚点链接目录。
锚点规则参照 GitHub:小写、空格转连字符、去掉非字母数字字符。
"""
import re
from pathlib import Path

TOC_BEGIN = "<!-- mdkit:toc:begin -->"
TOC_END = "<!-- mdkit:toc:end -->"

_HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
_FENCE = re.compile(r"^\s*(```|~~~)")


def slugify(text: str) -> str:
    """把标题文本转成 GitHub 风格锚点。"""
    text = text.strip().lower()
    text = re.sub(r"[^\w\u4e00-\u9fff\- ]", "", text)
    text = text.replace(" ", "-")
    return text


def extract_headings(lines, min_level=1, max_level=3):
    """返回 [(level, title, slug)],跳过代码块内的 # 行。"""
    headings = []
    in_fence = False
    for line in lines:
        if _FENCE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = _HEADING.match(line)
        if not m:
            continue
        level = len(m.group(1))
        if level < min_level or level > max_level:
            continue
        title = m.group(2).strip()
        headings.append((level, title, slugify(title)))
    return headings


def build_toc(headings, min_level=1) -> str:
    """把标题列表渲染成 Markdown 无序列表。"""
    out = []
    base = min(h[0] for h in headings) if headings else min_level
    for level, title, slug in headings:
        indent = "  " * (level - base)
        out.append(f"{indent}- [{title}](#{slug})")
    return "\n".join(out)


def insert_toc(text: str, toc: str) -> str:
    """把 toc 插入/替换到标记块之间;无标记则插到文首。"""
    block = f"{TOC_BEGIN}\n{toc}\n{TOC_END}"
    if TOC_BEGIN in text and TOC_END in text:
        pattern = re.compile(
            re.escape(TOC_BEGIN) + r".*?" + re.escape(TOC_END), re.DOTALL
        )
        return pattern.sub(block, text)
    return block + "\n\n" + text


def run(args) -> int:
    path = Path(args.file)
    if not path.is_file():
        print(f"错误:文件不存在 {path}")
        return 1
    text = path.read_text(encoding="utf-8")
    headings = extract_headings(
        text.splitlines(), args.min_level, args.max_level
    )
    if not headings:
        print("未找到符合级别范围的标题。")
        return 0
    toc = build_toc(headings, args.min_level)
    if args.write:
        path.write_text(insert_toc(text, toc), encoding="utf-8")
        print(f"已将目录写回 {path}")
    else:
        print(toc)
    return 0
