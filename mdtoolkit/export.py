import html
import re
from pathlib import Path

_HEADING = re.compile(r"^(#{1,6})\s+(.*)$")
_ULIST = re.compile(r"^\s*[-*+]\s+(.*)$")
_FENCE = re.compile(r"^\s*(```|~~~)")
_LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
_CODE = re.compile(r"`([^`]+)`")

_TEMPLATE = """<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="utf-8">
<title>{title}</title>
</head>
<body>
{body}
</body>
</html>
"""


def inline(text):
    text = html.escape(text)
    text = _LINK.sub(r'<a href="\2">\1</a>', text)
    text = _CODE.sub(r"<code>\1</code>", text)
    return text


def md_to_html(text):
    out, in_fence, in_list = [], False, False
    for line in text.splitlines():
        if _FENCE.match(line):
            if in_fence:
                out.append("</code></pre>"); in_fence = False
            else:
                if in_list:
                    out.append("</ul>"); in_list = False
                out.append("<pre><code>"); in_fence = True
            continue
        if in_fence:
            out.append(html.escape(line)); continue
        m = _HEADING.match(line)
        if m:
            if in_list:
                out.append("</ul>"); in_list = False
            lv = len(m.group(1))
            out.append(f"<h{lv}>{inline(m.group(2))}</h{lv}>"); continue
        m = _ULIST.match(line)
        if m:
            if not in_list:
                out.append("<ul>"); in_list = True
            out.append(f"<li>{inline(m.group(1))}</li>"); continue
        if in_list:
            out.append("</ul>"); in_list = False
        if line.strip() == "":
            continue
        out.append(f"<p>{inline(line)}</p>")
    if in_list:
        out.append("</ul>")
    return "\n".join(out)


def run(args) -> int:
    path = Path(args.file)
    if not path.is_file():
        print(f"错误:文件不存在 {path}")
        return 1
    body = md_to_html(path.read_text(encoding="utf-8"))
    doc = _TEMPLATE.format(title=path.stem, body=body)
    out_path = Path(args.output) if args.output else path.with_suffix(".html")
    out_path.write_text(doc, encoding="utf-8")
    print(f"已导出 {out_path}")
    return 0