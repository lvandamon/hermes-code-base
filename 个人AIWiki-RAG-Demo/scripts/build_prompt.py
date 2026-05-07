#!/usr/bin/env python3
"""把固定 Prompt 与一篇 RAG 文章合并，生成可直接交给 Hermes/OpenClaw 的 Prompt 文件。"""

from __future__ import annotations

import argparse
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="构建个人 AI Wiki / RAG Demo Prompt")
    parser.add_argument("article", type=Path, help="输入文章 Markdown 路径")
    parser.add_argument(
        "--template",
        type=Path,
        default=Path("prompts/固定Prompt-个人AIWikiRAG.md"),
        help="固定 Prompt 模板路径",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("runs/待交给Agent的Prompt.md"),
        help="输出 Prompt 路径",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    article_path = args.article
    template_path = args.template
    out_path = args.out

    if not article_path.exists():
        raise FileNotFoundError(f"输入文章不存在：{article_path}")
    if not template_path.exists():
        raise FileNotFoundError(f"Prompt 模板不存在：{template_path}")

    article = article_path.read_text(encoding="utf-8").strip()
    template = template_path.read_text(encoding="utf-8")
    if "{{ARTICLE}}" not in template:
        raise ValueError("Prompt 模板必须包含 {{ARTICLE}} 占位符")

    prompt = template.replace("{{ARTICLE}}", article)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(prompt + "\n", encoding="utf-8")
    print(f"已生成 Prompt：{out_path}")


if __name__ == "__main__":
    main()
