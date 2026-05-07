# 示例文章：为什么 RAG 系统不能只看向量检索

很多初学者会把 RAG 理解成“把文档切块，做 Embedding，然后相似度搜索”。这个理解只覆盖了最基础的一层。真实生产系统中，检索质量、上下文组织、答案生成和评估同样重要。

一个常见 RAG 流程包括：文档加载、Chunking、Embedding、向量存储、Retriever、Rerank、Prompt 组装、生成回答和 Evaluation。Chunking 会影响信息完整性，Embedding 会影响语义召回，Retriever 决定候选文档集合，Rerank 决定哪些内容最终进入上下文。

如果只依赖向量相似度，系统可能召回语义相近但不回答问题的片段，也可能漏掉关键词高度相关的事实。因此很多系统会采用 Hybrid Search，把稠密向量检索和关键词检索结合起来。对于复杂问题，还需要 Query Rewrite 或 Multi-hop Retrieval，把用户问题改写成更适合检索的形式。

评估也是 RAG 系统的重要组成部分。开发者需要分别评估检索阶段和生成阶段：检索看 Recall、Precision、MRR、NDCG，生成看 Faithfulness、Answer Relevance 和 Citation Accuracy。没有评估，就很难判断优化是否真的有效。

因此，一个可持续优化的 RAG 系统不只是“接一个向量数据库”，而是围绕数据、检索、排序、生成和评估建立闭环。
