# 个人 AI Wiki / RAG Demo

## 1. Demo 目标

先用最简单、稳定、可维护的技术组合搭建个人 AI Wiki / RAG Demo：

```text
Obsidian + Markdown + 本地 Git + Hermes/OpenClaw + 一个固定 Prompt
```

暂时不接复杂模型、向量库、数据库或 UI。当前阶段的目标不是“架构复杂”，而是形成一条稳定工作流：

> 给 Agent 一篇 RAG 文章，让它生成：一页中文摘要、术语中英文对照、关键概念表、关联主题、下一步学习问题。

## 2. 当前目录结构

```text
个人AIWiki-RAG-Demo/
├── README.md
├── docs/
│   ├── 000-实现规划.md
│   └── 001-GitHub同步说明.md
├── prompts/
│   └── 固定Prompt-个人AIWikiRAG.md
├── input/
│   └── 示例RAG文章.md
├── output/
│   ├── 示例生成结果.md
│   └── 待交给Agent的Prompt.md
├── templates/
│   └── AIWiki笔记模板.md
├── scripts/
│   └── build_prompt.py
└── runs/
    └── .gitkeep
```

## 3. 最小工作流

1. 把要学习的 RAG 文章保存为 Markdown，例如：`input/某篇RAG文章.md`。
2. 运行脚本，把固定 Prompt 与文章合并：

```bash
cd ~/Documents/Hermes代码库/个人AIWiki-RAG-Demo
python3 scripts/build_prompt.py input/示例RAG文章.md --out output/待交给Agent的Prompt.md
```

3. 把 `output/待交给Agent的Prompt.md` 的内容交给 Hermes/OpenClaw。
4. Agent 输出后，按 `templates/AIWiki笔记模板.md` 保存到 Obsidian vault 或本项目 `output/`。
5. 本地 Git 提交并同步到 GitHub。

## 4. 输出要求

每篇文章至少输出 5 个部分：

1. 一页中文摘要
2. 术语中英文对照，例如 `Embedding（嵌入）`、`Rerank（重排序）`、`Retriever（检索器）`
3. 关键概念表
4. 关联主题
5. 下一步学习问题

## 5. 当前不做的事情

- 不接向量数据库。
- 不做 Web UI。
- 不引入多模型编排。
- 不做自动爬虫。
- 不把 Demo 做成复杂框架。

后续只有当 Markdown 工作流稳定后，再逐步考虑 Embedding（嵌入）、Retriever（检索器）、Rerank（重排序）、评估与可视化。
