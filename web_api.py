"""web_api.py —— mdtoolkit 的本地 HTTP 服务。

把 mdtoolkit 包里真实的核心函数(toc/format/export/linkcheck)
暴露成 HTTP 接口,供 docs/index.html 的"在线体验"区通过 fetch 调用。

运行:
    pip install flask
    python web_api.py
启动后会自动打开浏览器,网页直接调用 mdtoolkit 包里真实的 Python 代码。
"""
import threading
import webbrowser
from pathlib import Path

from flask import Flask, request, jsonify, send_from_directory

from mdtoolkit.toc import extract_headings, build_toc
from mdtoolkit.format import normalize
from mdtoolkit.export import md_to_html, _TEMPLATE
from mdtoolkit.linkcheck import extract_links, check_http

DOCS_DIR = Path(__file__).parent / "docs"
app = Flask(__name__, static_folder=None)


@app.get("/")
def index():
    return send_from_directory(DOCS_DIR, "index.html")


@app.after_request
def add_cors(resp):
    """允许 docs/index.html 从 file:// 或任意源跨域调用(本地演示用)。"""
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type"
    resp.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return resp


def _text():
    data = request.get_json(silent=True) or {}
    return data.get("text", "")


@app.get("/api/health")
def health():
    return jsonify(status="ok", service="mdtoolkit")


@app.post("/api/toc")
def api_toc():
    text = _text()
    headings = extract_headings(text.splitlines(), 1, 3)
    if not headings:
        return jsonify(result="未找到符合级别范围的标题。")
    return jsonify(result=build_toc(headings, 1))


@app.post("/api/format")
def api_format():
    return jsonify(result=normalize(_text()))


@app.post("/api/export")
def api_export():
    body = md_to_html(_text())
    return jsonify(result=_TEMPLATE.format(title="预览", body=body))


@app.post("/api/linkcheck")
def api_linkcheck():
    """真实探测外链可达性;相对路径无文件上下文,仅列出不判定。"""
    text = _text()
    lines = text.splitlines()
    reports, bad = [], 0
    for lineno, target in extract_links(lines):
        if target.startswith(("http://", "https://")):
            ok = check_http(target)
            if ok:
                reports.append(f"第 {lineno} 行  OK    {target}")
            else:
                reports.append(f"第 {lineno} 行  坏链  {target} (无法访问)")
                bad += 1
        elif target.startswith(("mailto:", "#")):
            continue
        else:
            reports.append(f"第 {lineno} 行  相对路径  {target} (需在本地文件上下文中检查)")
    if not reports:
        return jsonify(result="文档里没有找到链接。")
    summary = f"\n共发现 {bad} 处坏链。" if bad else "\n外链全部可达。"
    return jsonify(result="\n".join(reports) + summary)


if __name__ == "__main__":
    url = "http://127.0.0.1:5000"
    print("mdtoolkit 服务已启动:", url)
    print("浏览器会自动打开;若没弹出,手动访问上面的地址即可。")
    print("用完关闭这个窗口即可停止服务。")
    threading.Timer(1.0, lambda: webbrowser.open(url)).start()
    app.run(host="127.0.0.1", port=5000, debug=False)
