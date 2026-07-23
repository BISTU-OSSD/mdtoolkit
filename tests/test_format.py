from pathlib import Path
import argparse
from mdtoolkit.format import normalize, run


def make_args(file, write=False):
    return argparse.Namespace(file=str(file), write=write)


def test_heading_space():
    assert normalize("#标题\n") == "# 标题\n"
    assert normalize("##  两空格\n") == "## 两空格\n"


def test_list_symbol():
    assert normalize("* a\n+ b\n") == "- a\n- b\n"


def test_blank_line_collapse():
    result = normalize("a\n\n\n\nb\n")
    assert result == "a\n\nb\n"


def test_trailing_space():
    result = normalize("hello   \n")
    assert result == "hello\n"


def test_code_fence_untouched():
    src = "```\n#不改\n* 不改\n```\n"
    assert normalize(src) == src


def test_write_back(tmp_path):
    md = tmp_path / "t.md"
    md.write_text("*  a\n", encoding="utf-8")
    run(make_args(md, write=True))
    assert md.read_text(encoding="utf-8") == "- a\n"
