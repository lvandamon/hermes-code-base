# 个人学习资料整理 Agent Demo

> 这是一个最小可运行的 Python Demo，用来演示“个人学习资料整理 Agent”如何把用户输入转成结构化 Markdown，并为后续资料库落库、索引维护和同步流程提供可测试的核心逻辑。

## 1. 项目定位

本 Demo 对应资料库中的项目化材料：

- `118-个人学习资料整理Agent-项目README成品版.md`
- `119-个人学习资料整理Agent-项目架构图.md`
- `120-个人学习资料整理Agent-Demo输入输出样例.md`
- `121-个人学习资料整理Agent-Benchmark评测表.md`
- `122-个人学习资料整理Agent-面试项目讲述稿.md`
- `123-个人学习资料整理Agent-简历项目经历描述.md`

它不是生产级 Agent，而是一个**可运行、可测试、可讲解**的最小闭环。

## 2. 核心能力

当前 Demo 支持：

1. 根据用户输入判断主题、资料类型和是否需要落库；
2. 根据同级已有文件名规划下一个可用三位数编号；
3. 渲染结构化中文 Markdown；
4. 将新文档行插入索引表格；
5. 通过 CLI 生成一个 Demo 输出文件；
6. 使用 pytest 验证核心逻辑。

## 3. 目录结构

```text
个人学习资料整理Agent-Demo/
├── README.md
├── src/
│   ├── __init__.py
│   └── learning_archive_agent.py
├── tests/
│   └── test_learning_archive_agent.py
├── examples/
│   └── sample_input.txt
└── output/
    └── demo-output.md
```

## 4. 运行方式

在项目目录执行：

```bash
python3 -m pytest tests/test_learning_archive_agent.py -q
```

运行 Demo：

```bash
python3 src/learning_archive_agent.py "请整理 Prompt Engineering、Context Engineering，并扩展到 Agent 系统构建" --output-dir output
```

生成结果：

```text
output/demo-output.md
```

## 5. 三层工程对应关系

| 层级 | Demo 中的体现 |
|---|---|
| Prompt Engineering | `render_markdown` 固定输出结构，模拟资料整理输出协议 |
| Context Engineering | `classify_request` 和 `plan_documents` 使用输入文本与已有文件名进行判断 |
| Harness Engineering | CLI、文件写入、索引更新函数、pytest 测试共同构成最小执行外壳 |

## 6. 测试覆盖

测试文件：

```text
tests/test_learning_archive_agent.py
```

覆盖行为：

- Agent 学习主题分类；
- 同级编号规划；
- Markdown 渲染；
- 索引表格插入。

## 7. 后续可扩展

- 接入真实 LLM，用模型替换规则分类；
- 接入资料库真实索引，自动读取目录和已有编号；
- 增加 Markdown 坏链接检查；
- 增加多文档拆分；
- 增加 Git commit/push 和飞书同步封装；
- 增加 benchmark 批量评测命令。
