from pathlib import Path

from src.learning_archive_agent import (
    classify_request,
    plan_documents,
    render_markdown,
    update_index_text,
)


def test_classify_agent_learning_request_to_ai_coding_topic():
    result = classify_request("请整理 Prompt Engineering、Context Engineering，并扩展到 Agent 系统构建")

    assert result["topic"] == "AI Coding 与 SWE Agent 观察"
    assert result["category"] == "学习资料"
    assert result["needs_archive"] is True


def test_plan_documents_allocates_next_available_numbers():
    existing_names = [
        "000-资料索引.md",
        "123-个人学习资料整理Agent-简历项目经历描述.md",
    ]
    plan = plan_documents(
        title="RAG 问答 Agent 项目包",
        existing_names=existing_names,
        count=2,
    )

    assert [item["number"] for item in plan] == [124, 125]
    assert plan[0]["filename"] == "124-RAG问答Agent项目包-01.md"
    assert plan[1]["filename"] == "125-RAG问答Agent项目包-02.md"


def test_render_markdown_contains_metadata_and_sections():
    markdown = render_markdown(
        title="个人学习资料整理 Agent Demo",
        purpose="展示资料整理 Agent 的最小闭环",
        sections={"输入": "用户给出学习主题", "输出": "Markdown 文档与索引更新建议"},
    )

    assert markdown.startswith("# 个人学习资料整理 Agent Demo")
    assert "## 输入" in markdown
    assert "用户给出学习主题" in markdown
    assert "## 输出" in markdown


def test_update_index_text_inserts_new_rows_after_anchor():
    original = """# 索引\n\n| 编号 | 文件 | 定位 |\n|---|---|---|\n| 123 | [旧文档.md](旧文档.md) | 旧材料 |\n\n## 推荐阅读顺序\n"""
    rows = [
        {"number": 124, "filename": "124-新文档.md", "description": "新材料"},
        {"number": 125, "filename": "125-第二份.md", "description": "第二份材料"},
    ]

    updated = update_index_text(original, rows)

    assert "| 124 | [124-新文档.md](124-新文档.md) | 新材料 |" in updated
    assert "| 125 | [125-第二份.md](125-第二份.md) | 第二份材料 |" in updated
    assert updated.index("| 123 |") < updated.index("| 124 |") < updated.index("## 推荐阅读顺序")
