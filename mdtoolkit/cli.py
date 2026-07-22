"""命令行入口:把 toc / linkcheck / format / export 四个子命令挂到 argparse。"""
import argparse
import sys

from mdtoolkit import __version__


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="mdkit",
        description="Markdown 命令行工具箱:目录生成、链接检查、格式化、导出。",
    )
    parser.add_argument("-V", "--version", action="version",
                        version=f"mdkit {__version__}")
    sub = parser.add_subparsers(dest="command", metavar="<command>")

    # toc —— 组长实现
    p_toc = sub.add_parser("toc", help="为 Markdown 生成/更新目录")
    p_toc.add_argument("file", help="Markdown 文件路径")
    p_toc.add_argument("-w", "--write", action="store_true",
                       help="将目录写回文件(默认打印到标准输出)")
    p_toc.add_argument("--min-level", type=int, default=1, help="纳入目录的最小标题级别")
    p_toc.add_argument("--max-level", type=int, default=3, help="纳入目录的最大标题级别")

    # linkcheck —— 成员2 实现
    p_lc = sub.add_parser("linkcheck", help="检查文档中的死链和坏的相对路径")
    p_lc.add_argument("file", help="Markdown 文件路径")

    # format —— 成员3 实现
    p_fmt = sub.add_parser("format", help="规范化 Markdown 格式")
    p_fmt.add_argument("file", help="Markdown 文件路径")
    p_fmt.add_argument("-w", "--write", action="store_true", help="将结果写回文件")

    # export —— 成员4 实现
    p_exp = sub.add_parser("export", help="将 Markdown 导出为 HTML")
    p_exp.add_argument("file", help="Markdown 文件路径")
    p_exp.add_argument("-o", "--output", help="输出 HTML 路径")

    return parser


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if not args.command:
        parser.print_help()
        return 0

    if args.command == "toc":
        from mdtoolkit.toc import run
        return run(args)
    if args.command == "linkcheck":
        from mdtoolkit.linkcheck import run
        return run(args)
    if args.command == "format":
        from mdtoolkit.format import run
        return run(args)
    if args.command == "export":
        from mdtoolkit.export import run
        return run(args)

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
