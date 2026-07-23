from pathlib import Path
import argparse
from mdtoolkit.export import run


def make_args(file, output=None):
    return argparse.Namespace(file=str(file), output=output)


def test_basic_output(tmp_path):
    md = tmp_path / "t.md"
    md.write_text("# 标题\n\n段落\n", encoding="utf-8")
    run(make_args(md))
    html = (tmp_path / "t.html").read_text(encoding="utf-8")
    assert '<meta charset="utf-8">' in html
    assert "<h1>" in html
    assert "<p>" in html


def test_custom_output(tmp_path):
    md = tmp_path / "t.md"
    md.write_text("hello\n", encoding="utf-8")
    out = tmp_path / "out.html"
    run(make_args(md, output=str(out)))
    assert out.exists()


def test_list_converted(tmp_path):
    md = tmp_path / "t.md"
    md.write_text("- a\n- b\n", encoding="utf-8")
    run(make_args(md))
    html = (tmp_path / "t.html").read_text(encoding="utf-8")
    assert "<ul>" in html
    assert "<li>" in html


def test_file_not_found(tmp_path):
    args = make_args(tmp_path / "nope.md")
    assert run(args) == 1
