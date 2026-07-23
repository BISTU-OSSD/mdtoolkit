from pathlib import Path
import pytest
from mdtoolkit.linkcheck import extract_links, run
import argparse


def make_args(file):
    args = argparse.Namespace(file=str(file))
    return args


def test_no_links(tmp_path):
    md = tmp_path / "a.md"
    md.write_text("# 标题\n\n普通段落，没有链接。\n", encoding="utf-8")
    assert run(make_args(md)) == 0


def test_relative_link_exists(tmp_path):
    target = tmp_path / "other.md"
    target.write_text("hello", encoding="utf-8")
    md = tmp_path / "a.md"
    md.write_text("[链接](other.md)\n", encoding="utf-8")
    assert run(make_args(md)) == 0


def test_relative_link_missing(tmp_path):
    md = tmp_path / "a.md"
    md.write_text("[坏链](./nope.md)\n", encoding="utf-8")
    assert run(make_args(md)) == 1


def test_skip_anchor_only(tmp_path):
    md = tmp_path / "a.md"
    md.write_text("[锚点](#section)\n", encoding="utf-8")
    assert run(make_args(md)) == 0


def test_skip_links_in_code_fence(tmp_path):
    md = tmp_path / "a.md"
    md.write_text("```\n[坏链](./nope.md)\n```\n", encoding="utf-8")
    assert run(make_args(md)) == 0


def test_file_not_found(tmp_path):
    args = make_args(tmp_path / "nonexistent.md")
    assert run(args) == 1
