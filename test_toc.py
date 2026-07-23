import subprocess
import sys


def run_cli(*args):
    return subprocess.run(
        [sys.executable, "-m", "mdtoolkit", *args],
        capture_output=True, text=True
    )


def test_help_lists_all_commands():
    r = run_cli("-h")
    assert r.returncode == 0
    for cmd in ("toc", "linkcheck", "format", "export"):
        assert cmd in r.stdout


def test_version():
    r = run_cli("-V")
    assert "mdkit" in r.stdout


def test_toc_runs(tmp_path):
    md = tmp_path / "a.md"
    md.write_text("# 标题\n## 小节\n", encoding="utf-8")
    r = run_cli("toc", str(md))
    assert r.returncode == 0