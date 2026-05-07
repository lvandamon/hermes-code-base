"""RAG 问答 Agent 最小可运行 Demo。

这个 Demo 不依赖外部 LLM 或向量数据库，使用确定性关键词检索模拟 RAG 的
核心闭环：加载文档 → 切分 chunk → 检索 → 基于片段回答/拒答 → 输出引用。
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class Document:
    doc_id: str
    title: str
    path: str
    text: str


@dataclass(frozen=True)
class Chunk:
    chunk_id: str
    doc_id: str
    title: str
    path: str
    heading: str
    text: str


@dataclass(frozen=True)
class SearchResult:
    chunk: Chunk
    score: int


@dataclass(frozen=True)
class Citation:
    doc_id: str
    path: str
    chunk_id: str
    heading: str


@dataclass(frozen=True)
class Answer:
    text: str
    citations: list[Citation]
    refused: bool


_STOPWORDS = {
    "什么", "如何", "怎么", "为什么", "以及", "一个", "这个", "那个", "相关", "资料",
    "the", "and", "or", "of", "to", "a", "in", "is", "for", "with",
}


def _extract_title(text: str, fallback: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def load_markdown_documents(source_dir: Path) -> list[Document]:
    """读取目录下所有 Markdown 文件。"""
    docs: list[Document] = []
    for path in sorted(source_dir.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        docs.append(
            Document(
                doc_id=path.stem,
                title=_extract_title(text, path.stem),
                path=path.name,
                text=text,
            )
        )
    return docs


def chunk_document(document: Document) -> list[Chunk]:
    """按二级标题切分 Markdown 文档。"""
    pattern = re.compile(r"^##\s+(.+)$", flags=re.MULTILINE)
    matches = list(pattern.finditer(document.text))
    chunks: list[Chunk] = []
    if not matches:
        body = re.sub(r"^#\s+.+\n?", "", document.text).strip()
        if body:
            chunks.append(
                Chunk(
                    chunk_id=f"{document.doc_id}#1",
                    doc_id=document.doc_id,
                    title=document.title,
                    path=document.path,
                    heading=document.title,
                    text=body,
                )
            )
        return chunks

    for index, match in enumerate(matches, start=1):
        start = match.end()
        end = matches[index].start() if index < len(matches) else len(document.text)
        heading = match.group(1).strip()
        body = document.text[start:end].strip()
        chunks.append(
            Chunk(
                chunk_id=f"{document.doc_id}#{index}",
                doc_id=document.doc_id,
                title=document.title,
                path=document.path,
                heading=heading,
                text=body,
            )
        )
    return chunks


def build_index(documents: list[Document]) -> list[Chunk]:
    """构建内存检索索引。"""
    chunks: list[Chunk] = []
    for document in documents:
        chunks.extend(chunk_document(document))
    return chunks


def _tokens(text: str) -> set[str]:
    words = re.findall(r"[A-Za-z0-9_]+|[\u4e00-\u9fff]{2,}", text.lower())
    return {word for word in words if word not in _STOPWORDS}


def retrieve(question: str, index: list[Chunk], top_k: int = 3) -> list[SearchResult]:
    """用简单 token overlap 检索相关 chunk。"""
    question_tokens = _tokens(question)
    results: list[SearchResult] = []
    for chunk in index:
        chunk_tokens = _tokens(" ".join([chunk.title, chunk.heading, chunk.text]))
        score = len(question_tokens & chunk_tokens)
        if score > 0:
            results.append(SearchResult(chunk=chunk, score=score))
    results.sort(key=lambda item: (-item.score, item.chunk.path, item.chunk.chunk_id))
    return results[:top_k]


def _first_sentence(text: str) -> str:
    normalized = " ".join(text.split())
    parts = re.split(r"(?<=[。！？.!?])\s*", normalized)
    return parts[0] if parts and parts[0] else normalized


def answer_question(question: str, index: list[Chunk], min_score: int = 1, top_k: int = 3) -> Answer:
    """基于检索片段回答；上下文不足时拒答。"""
    results = retrieve(question, index, top_k=top_k)
    if not results or results[0].score < min_score:
        return Answer(text="资料中没有足够信息回答该问题。建议补充相关文档后再提问。", citations=[], refused=True)

    cited_results = [results[0]]
    answer_parts = []
    citations: list[Citation] = []
    for result in cited_results:
        chunk = result.chunk
        answer_parts.append(_first_sentence(chunk.text))
        citations.append(Citation(doc_id=chunk.doc_id, path=chunk.path, chunk_id=chunk.chunk_id, heading=chunk.heading))

    citation_text = " ".join(f"[{idx}]" for idx, _ in enumerate(citations, start=1))
    text = f"基于已检索资料：{' '.join(answer_parts)} {citation_text}".strip()
    return Answer(text=text, citations=citations, refused=False)


def answer_as_markdown(question: str, answer: Answer) -> str:
    lines = ["# RAG 问答 Agent Demo 输出", "", f"## 问题", "", question, "", "## 答案", "", answer.text, ""]
    lines.extend(["## 引用", ""])
    if not answer.citations:
        lines.append("无引用。")
    else:
        for idx, citation in enumerate(answer.citations, start=1):
            lines.append(f"[{idx}] `{citation.path}` / `{citation.heading}` / `{citation.chunk_id}`")
    lines.extend(["", "## 是否拒答", "", "是" if answer.refused else "否", ""])
    return "\n".join(lines)


def run_demo(question: str, knowledge_dir: Path, output_path: Path) -> Answer:
    documents = load_markdown_documents(knowledge_dir)
    index = build_index(documents)
    answer = answer_question(question, index)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(answer_as_markdown(question, answer), encoding="utf-8")
    return answer


def main() -> None:
    parser = argparse.ArgumentParser(description="RAG 问答 Agent 最小 Demo")
    parser.add_argument("question", help="用户问题")
    parser.add_argument("--knowledge-dir", default="knowledge", help="Markdown 知识库目录")
    parser.add_argument("--output", default="output/demo-answer.md", help="输出 Markdown 文件")
    parser.add_argument("--json", action="store_true", help="同时在 stdout 输出 JSON")
    args = parser.parse_args()
    answer = run_demo(args.question, Path(args.knowledge_dir), Path(args.output))
    print(f"已生成：{args.output}")
    if args.json:
        print(json.dumps(asdict(answer), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
