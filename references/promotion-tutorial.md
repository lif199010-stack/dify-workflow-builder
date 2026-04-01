# dify-workflow-builder 推广教程

这份教程用于教别人如何使用 `dify-workflow-builder`。

## 一句话定位

`dify-workflow-builder` 是一个把**业务需求**转成 **Dify 可导入工作流 DSL YAML** 的 skill。

它不是只会“写 YAML”，而是会按顺序完成：
1. 需求澄清
2. 架构设计
3. 节点规划
4. 生成 `Dify DSL YAML file`
5. 审查 / 修复 / 校验
6. 告诉你如何通过 **Import DSL File** 导入到 Dify

---

## 适合谁用

适合这些人：
- 想快速搭 Dify 工作流的产品经理
- 要把业务逻辑转为工作流的运营 / 增长 / 咨询 / 客服团队
- 想批量生成 Dify YAML 的开发者
- 想审查、修复、迁移已有 Dify YAML 的人

---

## 它能做什么

### 1. 从业务需求生成 Dify 工作流
示例：
- 生成一个智能客服 Chatflow
- 生成一个 OCR 图片识别工作流
- 生成一个 API 编排 Workflow
- 生成一个 RAG Pipeline
- 生成一个 Agent 工具调用工作流

### 2. 审查现有 YAML / DSL
示例：
- 帮我检查这个 Dify YAML 能不能导入
- 帮我看看这个 workflow 为什么会报错
- 帮我找一下哪些节点结构不对

### 3. 修复和重构
示例：
- 帮我最小修复这个 DSL
- 帮我把这个工作流重构成更清晰的结构
- 帮我把一个普通 workflow 改成 rag_pipeline

---

## 正确使用姿势

### 方法一：从零开始搭建（最常用）

直接这样说：

```text
帮我生成一个 Dify 工作流。
目标：用户上传图片后识别文字，并输出结构化结果。
输入：图片文件。
输出：识别后的文字 JSON。
模式：workflow。
```

然后 skill 会继续问你：
- 目标用户是谁
- 输入输出格式是什么
- 是否接 API / 知识库 / 工具
- 是否有条件分支 / 循环 / 人工兜底
- 是新建还是改现有 App

### 方法二：明确指定模板

如果你已经知道场景，可以直接指定模板：

```text
用 customer-service-chatflow 模板，给我生成一个 Dify DSL YAML file。
```

可用模板包括：
- `customer-service-chatflow`
- `api-orchestration-workflow`
- `form-collection-workflow`
- `rag-assistant-chatflow`
- `rag-pipeline-basic`
- `agent-tool-use`
- `ocr-to-structured-output`
- `text-to-html-or-file`

### 方法三：审查已有 YAML

```text
帮我 review 这个 Dify YAML，判断能不能通过 Import DSL File 导入。
```

### 方法四：修复已有 YAML

```text
帮我 refactor 这个 Dify YAML，先找问题，再做最小修复。
```

---

## 标准输出长什么样

这个 skill 的正确输出顺序不是直接甩 YAML，而是：

1. 任务概述
2. 模式判断
3. 架构方案
4. 节点清单
5. 连边清单
6. 风险与待确认项
7. `Dify DSL YAML file`
8. Import DSL File 导入说明

如果别人用这个 skill 时，一上来只让它吐 YAML，容易缺上下文、容易错。

---

## 最佳提问模板

### 模板 1：从业务需求生成

```text
帮我生成一个 Dify 工作流：
- 目标：
- 用户：
- 输入：
- 输出：
- 关键流程：
- 外部依赖：
- 模式偏好：
- 模型偏好：
```

### 模板 2：生成可导入 YAML

```text
根据下面业务需求，输出完整的 Dify DSL YAML file，
并告诉我如何通过 Dify 的 Import DSL File 导入：
[粘贴需求]
```

### 模板 3：做审查

```text
请审查下面这个 Dify YAML：
1. 判断属于什么模式
2. 检查节点和连边
3. 判断是否是 Import DSL File 候选
4. 列出阻塞项和修复建议
```

### 模板 4：做修复

```text
请帮我最小修复这个 Dify YAML：
- 不要重写全部
- 先找阻塞导入的问题
- 再给修复后的 YAML
- 最后告诉我是否可以导入
```

---

## 教别人时要强调的 5 个关键点

### 1. 先讲业务，不要先讲 YAML
这个 skill 的强项是**从业务到工作流**，不是单纯写配置。

### 2. 让 skill 先澄清需求
如果目标不清，先让它问问题，不要逼它直接写。

### 3. 输出要包含 `Dify DSL YAML file`
推广时一定强调：
它不是概念图，而是会输出 **Dify DSL YAML file**。

### 4. 导入方式固定
导入说明通常是：

```text
将生成结果保存为 `.yml` 或 `.yaml` 文件，
在 Dify 控制台中使用 Import DSL File 导入。
```

### 5. 可导入 ≠ 已跑通
即使 YAML 结构能导入，也不代表业务一定调通；
导入后还要测试 prompt、tool、插件、节点配置。

---

## 常见误区

### 误区 1：只给一句“帮我做个工作流”
问题：信息太少，生成结果容易偏。
正确做法：至少说清楚目标 / 输入 / 输出 / 流程。

### 误区 2：把 review 当 generate
问题：想审查现有 YAML，却不告诉 skill 这是 review 任务。
正确做法：明确说“请审查 / review / validate”。

### 误区 3：把可导入当成可上线
问题：导入不报错就以为没问题。
正确做法：导入后再测试运行路径。

### 误区 4：看到 bug 就怪 skill
问题：很多问题其实是 Dify 版本、插件依赖、导入机制、前端格式识别 bug。
正确做法：让 skill 先做结构审查和定位。

---

## 推广时可直接复制的话术

```text
如果你有业务需求，但不会手写 Dify DSL，
直接把需求交给 dify-workflow-builder。

它会先问清业务目标，再帮你设计工作流结构，
输出完整的 Dify DSL YAML file，
并告诉你如何通过 Dify 的 Import DSL File 导入。

如果你已经有 YAML，它还能帮你 review、refactor、validate。
```

---

## 给新手的最短上手路径

只教 3 句话就够：

### 第一句：生成
```text
帮我根据下面业务需求生成 Dify DSL YAML file。
```

### 第二句：审查
```text
帮我检查这个 YAML 能不能通过 Import DSL File 导入。
```

### 第三句：修复
```text
帮我最小修复这个 Dify YAML，并告诉我还有哪些风险。
```

这样别人就能马上上手。
