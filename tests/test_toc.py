from mdtoolkit.toc import (
    slugify,
    extract_headings,
    build_toc,
    insert_toc,
    TOC_BEGIN,
    TOC_END,
)


def test_slugify_basic():
    assert slugify("Hello World") == "hello-world"
    assert slugify("A & B: C!") == "a--b-c"


def test_slugify_cjk():
    assert slugify("安装说明") == "安装说明"


def test_extract_skips_code_fence():
    text = """# 标题一

```
# 这是代码里的井号,不算标题
```

## 标题二
"""
    headings = extract_headings(text.splitlines())
    titles = [h[1] for h in headings]
    assert titles == ["标题一", "标题二"]


def test_extract_respects_level_range():
    text = "# H1\n## H2\n### H3\n#### H4\n"
    headings = extract_headings(text.splitlines(), min_level=2, max_level=3)
    assert [h[0] for h in headings] == [2, 3]


def test_build_toc_indent():
    headings = [(1, "顶层", "顶层"), (2, "子节", "子节")]
    toc = build_toc(headings)
    lines = toc.splitlines()
    assert lines[0] == "- [顶层](#顶层)"
    assert lines[1] == "  - [子节](#子节)"


def test_insert_toc_replaces_existing_block():
    text = f"{TOC_BEGIN}\n旧目录\n{TOC_END}\n\n# 正文\n"
    result = insert_toc(text, "- [新](#新)")
    assert "旧目录" not in result
    assert "- [新](#新)" in result
    assert result.count(TOC_BEGIN) == 1


def test_insert_toc_prepends_when_no_marker():
    text = "# 正文\n"
    result = insert_toc(text, "- [正文](#正文)")
    assert result.startswith(TOC_BEGIN)
    assert "# 正文" in result
