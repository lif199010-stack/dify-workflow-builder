# 模板目录（V2 Pro）

## 一、基础高频模板

### 1. customer-service-chatflow
- 模式：advanced-chat
- 骨架：start → llm(intent) → if-else → tool(sales/support) → llm(reply) → answer
- 适用：客服、顾问、售前问答

### 2. api-orchestration-workflow
- 模式：workflow
- 骨架：start → parameter-extractor → http-request → code → answer
- 适用：API 调用、数据编排

### 3. rag-pipeline-basic
- 模式：rag_pipeline
- 骨架：start → tool(retrieval) → llm(answer) → answer
- 适用：基础 RAG 主链路

## 二、新补高频复杂节点模板

### 4. iteration-batch-workflow
- 模式：workflow
- 骨架：start → code(split list) → iteration → llm(item) → answer
- 节点：`iteration`
- 适用：批量处理、清单循环、逐项分析

### 5. aggregator-summary-workflow
- 模式：workflow
- 骨架：start → llm(A) + llm(B) → variable-aggregator → llm(summary) → answer
- 节点：`variable-aggregator`
- 适用：多路结果汇总、并行分析后统一总结

### 6. question-classifier-workflow
- 模式：workflow
- 骨架：start → question-classifier → llm(branches) → answer
- 节点：`question-classifier`
- 适用：问题分类、路由分流、不同类目响应

### 7. knowledge-retrieval-workflow
- 模式：workflow
- 骨架：start → knowledge-retrieval → llm(answer) → answer
- 节点：`knowledge-retrieval`
- 适用：知识检索、知识库问答

### 8. assigner-memory-workflow
- 模式：workflow
- 骨架：start → llm(clean) → assigner → answer
- 节点：`assigner`
- 适用：变量写入、上下文整理、记忆摘要

## 三、其他保留模板

### 9. form-collection-workflow
- 模式：workflow
- 适用：表单收集、资料采集

### 10. rag-assistant-chatflow
- 模式：advanced-chat
- 适用：RAG 问答助手

### 11. agent-tool-use
- 模式：agent-chat
- 适用：Agent 工具调用

### 12. ocr-to-structured-output
- 模式：workflow
- 适用：OCR

### 13. text-to-html-or-file
- 模式：advanced-chat
- 适用：HTML / 文件内容生成
