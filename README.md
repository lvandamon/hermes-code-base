# Hermes 代码库

这个目录用于保存用户后续所有可运行代码、Demo、脚本和项目化实验。

- 本地路径：`~/Documents/Hermes代码库/`
- GitHub 仓库：`git@github-code:lvandamon/hermes-code-base.git`
- 自动同步：系统 crontab 每 30 分钟运行一次 `~/.hermes/scripts/git-autosync.sh ~/Documents/Hermes代码库`
- 手动同步：重要改动完成后由 Hermes 主动 `git commit && git push`

## 当前子项目

| 子项目 | 定位 | 状态 |
|---|---|---|
| `个人AIWiki-RAG-Demo/` | 用 Obsidian + Markdown + 本地 Git + 固定 Prompt，把一篇 RAG 文章转成可沉淀的中文 Wiki 笔记 | 已创建最小可用版 |

## 维护原则

1. 所有代码、Demo、脚本、项目模板优先放在本目录下。
2. 不提前创建大量空项目目录；有真实项目内容时再新增子目录。
3. 每个子项目至少包含 `README.md`、可执行脚本或固定 Prompt、示例输入和示例输出。
4. 文档默认使用中文；英文专业术语首次出现时保留中英文对照。
