from pathlib import Path

from src.rag_qa_agent import (
    Citation,
    Document,
    answer_question,
    build_index,
    chunk_document,
    load_markdown_documents,
    retrieve,
)


def test_chunk_document_splits_markdown_by_headings():
    doc = Document(
        doc_id="rag-guide",
        title="RAG 指南",
        path="docs/rag.md",
        text="# RAG 指南\n\n## 检索\nRAG 需要先检索相关片段。\n\n## 引用\n答案必须带引用。",
    )

    chunks = chunk_document(doc)

    assert len(chunks) == 2
    assert chunks[0].chunk_id == "rag-guide#1"
    assert chunks[0].heading == "检索"
    assert "先检索相关片段" in chunks[0].text
    assert chunks[1].heading == "引用"


def test_retrieve_returns_ranked_chunks_for_question():
    docs = [
        Document("rag", "RAG", "rag.md", "## 检索\nRAG 使用向量检索和 rerank 找到相关资料。"),
        Document("agent", "Agent", "agent.md", "## 工具\nAgent 使用工具调用执行任务。"),
    ]
    index = build_index(docs)

    results = retrieve("RAG 如何找到相关资料？", index, top_k=1)

    assert len(results) == 1
    assert results[0].chunk.doc_id == "rag"
    assert results[0].score > 0


def test_answer_question_returns_cited_answer_when_context_matches():
    docs = [
        Document("rag", "RAG", "rag.md", "## 检索\nRAG 使用向量检索和 rerank 找到相关资料。\n\n## 引用\n答案应该标注来源。"),
    ]
    index = build_index(docs)

    answer = answer_question("RAG 如何找到相关资料？", index, min_score=1)

    assert answer.refused is False
    assert "向量检索" in answer.text
    assert answer.citations == [Citation(doc_id="rag", path="rag.md", chunk_id="rag#1", heading="检索")]


def test_answer_question_refuses_when_context_is_insufficient():
    docs = [Document("rag", "RAG", "rag.md", "## 检索\nRAG 使用向量检索。")]
    index = build_index(docs)

    answer = answer_question("如何训练图像扩散模型？", index, min_score=1)

    assert answer.refused is True
    assert "资料中没有足够信息" in answer.text
    assert answer.citations == []


def test_load_markdown_documents_reads_files(tmp_path: Path):
    source = tmp_path / "knowledge"
    source.mkdir()
    (source / "rag.md").write_text("# RAG\n\n## 检索\nRAG 需要检索。", encoding="utf-8")

    docs = load_markdown_documents(source)

    assert docs == [Document(doc_id="rag", title="RAG", path="rag.md", text="# RAG\n\n## 检索\nRAG 需要检索。")]
