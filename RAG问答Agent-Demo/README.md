# RAG 问答 Agent Demo

> 这是一个最小可运行的 RAG 问答 Agent 原型，用确定性关键词检索模拟 RAG 核心闭环：加载 Markdown 文档、按标题切分 chunk、检索相关片段、基于片段回答或拒答，并输出引用。

## 1. 项目定位

本 Demo 对应资料库中的项目化材料：

- `124-RAG问答Agent-项目README成品版.md`
- `125-RAG问答Agent-项目架构图.md`
- `126-RAG问答Agent-Demo输入输出样例.md`
- `127-RAG问答Agent-Benchmark评测表.md`
- `128-RAG问答Agent-面试项目讲述稿.md`
- `129-RAG问答Agent-简历项目经历描述.md`

它不是生产级 RAG 系统，而是用于学习、面试讲解和后续扩展的最小闭环。

## 2. 当前能力

- 读取 `knowledge/` 目录下的 Markdown 文件；
- 按二级标题 `##` 切分 chunk；
- 用 token overlap 做简易检索；
- 根据检索片段生成带引用回答；
- 上下文不足时拒答；
- 输出 Markdown 答案；
- 使用 pytest 覆盖核心逻辑。

## 3. 目录结构

```text
RAG问答Agent-Demo/
├── README.md
├── src/
│   ├── __init__.py
│   └── rag_qa_agent.py
├── tests/
│   └── test_rag_qa_agent.py
├── knowledge/
│   └── rag-agent-guide.md
└── output/
    └── demo-answer.md
```

## 4. 运行测试

```bash
cd ~/Documents/Hermes代码库/RAG问答Agent-Demo
python3 -m pytest tests/test_rag_qa_agent.py -q
```

## 5. 运行 Demo

```bash
python3 src/rag_qa_agent.py "RAG 如何找到相关资料？" --knowledge-dir knowledge --output output/demo-answer.md --json
```

生成结果：

```text
output/demo-answer.md
```

## 6. 三层工程对应关系

| 层级 | Demo 中的体现 |
|---|---|
| Prompt Engineering | `answer_as_markdown` 固定回答结构：问题、答案、引用、是否拒答 |
| Context Engineering | `load_markdown_documents`、`chunk_document`、`retrieve` 负责资料选择与上下文构造 |
| Harness Engineering | CLI、文件输入输出、测试、拒答逻辑和引用结构构成最小运行外壳 |

## 7. 后续可扩展

- 用 embedding 替换关键词检索；
- 增加 rerank；
- 支持 PDF、网页和多级目录；
- 增加引用忠实度检查；
- 增加评测集和 Recall@K 指标；
- 接入真实 LLM 生成更自然的答案；
- 增加低置信度问题沉淀和知识库补全建议。
