---
name: dify-workflow-builder
description: Design, generate, review, refactor, validate, and deliver Dify Workflow/Chatflow/RAG Pipeline configurations from business requirements. Use when the user wants to create a new Dify app, convert business logic into Dify DSL YAML, review an existing Dify YAML/DSL, refactor a broken workflow, generate importable “Dify DSL YAML file”, or validate whether a workflow is directly importable through Dify Import DSL File.
---

# dify-workflow-builder

V2 Pro：把业务需求收敛为可导入 Dify 的完整配置，并覆盖 **设计 / 生成 / 审查 / 重构 / 校验 / 交付** 全流程。

## 先读什么

1. 先读 `references/interview-checklist.md`，收敛业务需求。
2. 若需要模板选型，再读 `references/template-catalog.md`。
3. 若需要核对输出顺序，再读 `references/design-output-contract.md`。
4. 若需要结构字段速查，再读 `references/dify-dsl-spec-quickref.md`。
5. 若需要解释来源融合，读 `references/source-fusion.md`。
6. 若要对外教学、推广或交付教程，优先读 `references/public-user-tutorial.md`，补充可读 `references/promotion-tutorial.md`。
7. 若遇到 Dify 导入 / 格式 / 节点兼容 / UI 异常，读 `references/dify-bug-runbook.md`。
8. 若要解释为什么继续补复杂节点、以及怎样避免 skill 变乱，读 `references/complex-node-strategy.md`。
9. 若用户明确要求“保姆式引导”“从业务梳理一路带到落地”，读 `references/nanny-mode.md` 并按该流程推进。
10. 若用户直接提供 Dify 部署网址 / app 页面 URL，读 `references/dify-url-entry.md`、`references/url-driven-nanny-flow.md` 与 `references/dify-url-recognition-checklist.md`，优先通过 URL 锁定目标 app，再决定是新建还是改造。
11. 若要强化阶段推进感，读 `references/execution-protocol.md`，按“当前阶段 / 本阶段目标 / 下一步动作”方式推进。

## V2 Pro 核心能力

1. **business → architecture**：从业务目标自动推导 Dify 架构。
2. **architecture → DSL YAML**：输出完整 `Dify DSL YAML file`。
3. **review / refactor / validate**：能审、能修、能给导入判断。
4. **import-ready delivery**：明确说明可通过 Dify 的 **Import DSL File** 导入。
5. **Dify-native thinking**：按 Dify 的 mode、nodes、edges、selector、dependencies 来设计，而不是普通流程图思维。

## 五段式主流程

### 1. Brainstorm
需求模糊时，先问清：目标、用户、输入、输出、流程、外部依赖、模式、模型、是否新建/改造。

### 2. Design
先输出：
- 任务概述
- 模式判断
- 架构方案
- 节点清单
- 连边清单
- 关键变量 / selector
- 风险与待确认项

### 3. Generate
再输出：
- `Dify DSL YAML file`
- Import DSL File 导入说明
- 如果用户要求，附 JSON / draft 写入方案

### 4. Review / Refactor
已有 DSL 时：
- 只读检查：review
- 最小修复 / 重构：refactor
- 改完后再 validate

### 5. Validate
检查：
- 顶层结构
- mode 合理性
- graph.nodes / graph.edges 完整性
- start 到输出节点贯通
- 节点 ID、selector、变量引用、依赖、常见阻塞项

## 保姆式引导模式（强执行）

当用户使用以下固定语句或近似表达时，必须进入保姆式引导流程：
- `启动 Dify 工作流保姆式搭建流程`
- `请启动 Dify 工作流保姆式搭建流程`
- `带我从业务梳理到 Dify 工作流落地`
- `请保姆式引导我搭建 Dify 工作流`

进入该模式后，必须主动推进以下闭环：
1. 业务梳理
2. 需求确认
3. 模式判断
4. 工作流设计
5. 生成 `Dify DSL YAML file`
6. 用户确认
7. 审查与调试
8. 落地建议

如果用户同时提供 **Dify 部署网址 / app 页面 URL**，则必须把 URL 识别与 app 锁定纳入流程：
1. 先识别 URL 类型
2. 锁定目标 app / workflow
3. 查看当前状态
4. 再决定新建 / 改造路径
5. 然后继续保姆式搭建 / 修正 / 联调

关键约束：
- 不要跳过需求确认
- 不要一开始就直接输出大段 YAML
- 每到关键节点（需求确认 / 设计确认 / 大改前）必须等待用户确认
- Agent 要像项目经理一样主动推进下一步，而不是只被动回答
- 若用户提供 URL，应优先利用 URL 锁 app，而不是反复重新询问 app 名称

## 模式判断规则

- `workflow`：单次任务、文件处理、API 编排、强流程任务
- `advanced-chat`：多轮对话、智能客服、顾问式问答
- `rag_pipeline`：检索 / 召回链路是核心
- `agent-chat`：复杂任务、自主工具调用、多工具协同

如果用户没指定，必须由你判断并说明原因。

## 交付输出契约

输出顺序必须遵守：
1. 任务概述
2. 模式判断
3. 架构方案
4. 节点清单
5. 连边清单
6. 风险与待确认项
7. `Dify DSL YAML file`
8. Import DSL File 导入说明

不要一上来只给大段 YAML。

## 必须包含的导入说明

生成 YAML 后，必须附上：

```text
Dify DSL YAML file 已生成。
可将该 YAML 保存为 `.yml` 或 `.yaml` 文件，然后在 Dify 控制台中使用：
Import DSL File → 选择该文件 → 导入。
```

## review / refactor / validate 最低输出

### review
- 模式判断
- 节点清单
- 连边清单
- 字段检查表
- 风险分级
- 导入判断
- 最终结论

### refactor
- 问题归因
- 最小修复 / 重构方案
- 修改后的 YAML / DSL
- 变更影响
- 待确认风险

### validate
- YAML 是否完整
- Dify Import DSL File 候选判断
- 阻塞项 / 非阻塞项
- 下一步建议

## 生成规范

### 必须遵守
- 顶层结构默认：`app / dependencies / kind / version / workflow`
- 默认 DSL 版本：`0.3.0`
- 节点 id 唯一
- 变量引用采用 `{{#node_id.field#}}`
- edge 的 source / target 必须指向真实节点
- 不把“可导入”误说成“已跑通业务”
- 不在需求未澄清时直接承诺上线可用

### 中文安全写入
当需要真实写入 Dify 后台：
- 走 **UTF-8 文件中转 → 写入 → 立即读回校验**
- 不要直接在多层 shell / JS / AppleScript 里内联大段中文 JSON

### Dify API 关键 method
- app 元信息更新：`PUT /console/api/apps/{id}`
- workflow draft：`POST /console/api/apps/{id}/workflows/draft`
- publish：`POST /console/api/apps/{id}/workflows/publish`

## 模板目录

按需选择以下模板骨架：
- customer-service-chatflow
- api-orchestration-workflow
- form-collection-workflow
- rag-assistant-chatflow
- rag-pipeline-basic
- agent-tool-use
- ocr-to-structured-output
- text-to-html-or-file

其中本轮 V2 Pro 已补强：
- `customer-service-chatflow`：`if-else + tool`
- `api-orchestration-workflow`：`parameter-extractor + http-request + code`
- `rag-pipeline-basic`：`rag_pipeline` 基础结构
- `iteration-batch-workflow`：`iteration`
- `aggregator-summary-workflow`：`variable-aggregator`
- `question-classifier-workflow`：`question-classifier`
- `knowledge-retrieval-workflow`：`knowledge-retrieval`
- `assigner-memory-workflow`：`assigner`

模板细节见 `references/template-catalog.md`。

## 脚本

- `scripts/build_workflow.js`：生成 workflow 骨架 JSON
- `scripts/generate_dify_yaml.py`：生成 `Dify DSL YAML file`
- `scripts/review_dify_yaml.py`：做结构审查与 Import 候选判断
- `scripts/dify_workflow_update.js`：写入 Dify draft / publish
- `scripts/dify_check.sh`：检查 Dify app / draft / publish
- `scripts/inject_json_editor.js`：处理富前端 JSON 编辑器

## 来源融合

精确来源已融合：
- `wwwzhouhui/skills_collection/tree/main/dify-dsl-generator`
- `wwwzhouhui/skills_collection/blob/main/dify-dsl-generator/SKILL.md`
- `lazeyliu/dify-dsl-generator-skills`

来源映射与吸收点见 `references/source-fusion.md`。
