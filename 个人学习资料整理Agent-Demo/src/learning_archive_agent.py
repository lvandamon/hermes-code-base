"""个人学习资料整理 Agent 的最小可运行 Demo。

这个模块刻意保持轻量：不依赖外部 LLM API，只演示 Agent 系统中的
Prompt / Context / Harness 思路如何落到可测试的确定性流程里。
"""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
from typing import Iterable


AGENT_TOPIC_KEYWORDS = (
    "agent",
    "Agent",
    "SWE",
    "AI Coding",
    "Prompt Engineering",
    "Context Engineering",
    "Harness Engineering",
    "智能体",
)


def classify_request(text: str) -> dict:
    """根据用户输入判断资料主题和用途。

    这是 Demo 版的确定性分类器：真实系统中可替换为 LLM 分类、规则 +
    embedding 检索，或读取资料库索引后的上下文判断。
    """
    normalized = text.strip()
    is_agent_topic = any(keyword in normalized for keyword in AGENT_TOPIC_KEYWORDS)
    category = "面试题" if "面试" in normalized else "学习资料"
    return {
        "topic": "AI Coding 与 SWE Agent 观察" if is_agent_topic else "待进一步判断",
        "category": category,
        "needs_archive": bool(normalized),
        "confidence": "high" if is_agent_topic else "medium",
    }


def _used_numbers(existing_names: Iterable[str]) -> set[int]:
    used: set[int] = set()
    for name in existing_names:
        prefix = name.split("-", 1)[0]
        if prefix.isdigit():
            used.add(int(prefix))
    return used


def _slugify_zh_title(title: str) -> str:
    return (
        title.replace(" ", "")
        .replace("：", "-")
        .replace(":", "-")
        .replace("/", "-")
        .replace("｜", "-")
    )


def plan_documents(title: str, existing_names: Iterable[str], count: int = 1) -> list[dict]:
    """根据同级已有文件名规划新文档编号。"""
    if count < 1:
        raise ValueError("count 必须大于等于 1")
    used = _used_numbers(existing_names)
    ordinary_numbers = [number for number in used if 100 <= number <= 899]
    current = (max(ordinary_numbers) + 1) if ordinary_numbers else 100
    plan: list[dict] = []
    slug = _slugify_zh_title(title)
    while len(plan) < count:
        if current not in used:
            plan.append(
                {
                    "number": current,
                    "filename": f"{current}-{slug}-{len(plan)+1:02d}.md",
                    "description": f"{title} 第 {len(plan)+1} 份材料",
                }
            )
        current += 1
    return plan


def render_markdown(title: str, purpose: str, sections: dict[str, str]) -> str:
    """渲染结构化中文 Markdown。"""
    lines = [
        f"# {title}",
        "",
        f"> 日期：{date.today().isoformat()}  ",
        f"> 文档定位：{purpose}",
        "",
        "---",
        "",
    ]
    for heading, body in sections.items():
        lines.extend([f"## {heading}", "", body.strip(), ""])
    return "\n".join(lines).rstrip() + "\n"


def update_index_text(index_text: str, rows: list[dict]) -> str:
    """把新文档行插入到索引表格末尾、下一节标题之前。"""
    insert_lines = [
        f"| {row['number']} | [{row['filename']}]({row['filename']}) | {row['description']} |"
        for row in rows
    ]
    marker = "\n## 推荐阅读顺序"
    if marker not in index_text:
        return index_text.rstrip() + "\n" + "\n".join(insert_lines) + "\n"
    before, after = index_text.split(marker, 1)
    before = before.rstrip() + "\n" + "\n".join(insert_lines) + "\n"
    return before + marker + after


def run_demo(input_text: str, output_dir: Path) -> Path:
    """执行一个最小资料整理 Demo，并返回生成文件路径。"""
    result = classify_request(input_text)
    markdown = render_markdown(
        title="个人学习资料整理 Agent Demo 输出",
        purpose="展示从用户输入到结构化 Markdown 的最小闭环",
        sections={
            "用户输入": input_text,
            "分类结果": "\n".join(f"- {key}: {value}" for key, value in result.items()),
            "下一步建议": "读取目标专题索引，规划文件编号，生成正式落库文档并更新索引。",
        },
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "demo-output.md"
    output_path.write_text(markdown, encoding="utf-8")
    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(description="个人学习资料整理 Agent 最小 Demo")
    parser.add_argument("text", help="待整理的用户输入")
    parser.add_argument("--output-dir", default="output", help="输出目录")
    args = parser.parse_args()
    output_path = run_demo(args.text, Path(args.output_dir))
    print(f"已生成：{output_path}")


if __name__ == "__main__":
    main()
