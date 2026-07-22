"""linkcheck —— 检查 Markdown 中的死链和坏的相对路径(成员2 模块)。

待实现,见 Issue: linkcheck 子命令。
预期功能:
  - 提取文档中的所有链接 [text](url)
  - 相对路径链接:检查目标文件是否存在
  - http(s) 链接:发起请求检查可达性(可选,带超时)
  - 返回:打印坏链列表,存在坏链时退出码非 0
"""


def run(args) -> int:
    raise NotImplementedError(
        "linkcheck 尚未实现。负责人:成员2。参见仓库 Issue。"
    )
