# mdtoolkit

一个 Markdown 命令行工具箱。把日常处理 Markdown 的零散操作——生成目录、检查死链、规范格式、导出 HTML——收进一个命令 `mdkit` 里。

## 面向的用户与解决的问题

写文档、博客、README 的人经常需要:手动维护目录、排查文档里失效的链接、统一混乱的格式、把 Markdown 转成能分享的 HTML。这些事零散又重复。mdtoolkit 把它们做成统一的命令行子命令,一条命令搞定一件事,也方便接入 CI 做文档检查。

## 安装

```bash
pip install mdtoolkit
```

开发安装:

```bash
git clone https://github.com/BISTU-OSSD/mdtoolkit.git
cd mdtoolkit
pip install -e ".[dev]"
```

## 使用

```bash
mdkit toc README.md            # 打印目录
mdkit toc README.md -w         # 把目录写回文件
mdkit linkcheck docs/guide.md  # 检查死链
mdkit format notes.md -w       # 规范化格式并写回
mdkit export post.md -o post.html   # 导出 HTML
```

### 子命令一览

| 子命令 | 作用 |
|--------|------|
| `toc` | 解析标题,生成/更新带锚点的目录 |
| `linkcheck` | 检查相对路径链接与外链可达性 |
| `format` | 规范标题空格、列表符号、多余空行 |
| `export` | 将 Markdown 导出为 HTML |

`toc` 会在 `<!-- mdkit:toc:begin -->` / `<!-- mdkit:toc:end -->` 标记之间插入或更新目录;文件中没有标记时插入到文首。

## 开发与贡献

本项目采用 Issue 拆分任务、Pull Request 提交贡献、成员互相 Review 的协作方式。

1. 从 Issue 认领任务,基于 `main` 开分支
2. 开发并补充测试,本地跑通 `pytest -q`
3. 提 PR,关联对应 Issue,由其他成员 Review
4. Review 通过后合并到 `main`

提交信息遵循约定式提交:`feat:` / `fix:` / `docs:` / `test:`。

## 运行测试

```bash
pytest -q
```

## 许可证

[MIT](LICENSE)
