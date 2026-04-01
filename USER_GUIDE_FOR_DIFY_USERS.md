# dify-workflow-builder：Dify 使用者教程成品

## 这是什么

`dify-workflow-builder` 是一个帮助你**从业务需求直接搭建 Dify 工作流**的 Agent Skill。

它可以做的事情，不只是“写 YAML”，而是完整帮你完成：
- 业务梳理
- 需求明确
- 工作流设计
- 输出 `Dify DSL YAML file`
- 检查是否可导入
- 提醒常见 Dify bug 风险
- 指导你最终落地到 Dify

---

## 它里面有什么

这个 skill 内部包含：
- 业务访谈能力
- 工作流设计能力
- YAML 生成能力
- review / refactor / validate 能力
- Dify bug 排查能力
- 保姆式项目引导能力
- 通过 Dify URL 直接识别和进入目标 app 的能力

---

## 它能做什么

你可以让它：
- 从零搭 Dify 工作流
- 审查已有 YAML
- 修复已有 DSL
- 给你可导入的 `Dify DSL YAML file`
- 识别你提供的 Dify 部署网址 / app 页面 URL
- 在你给出 URL 后，进入查看 app，并继续搭建或修正流程

---

## 在哪里用

你是在**安装了该 skill 的 Agent**里使用它，不是在 Dify 后台直接点这个 skill。

---

## 怎么调用这个 skill

### 普通触发语句
```text
帮我搭一个 Dify 工作流
```

```text
帮我根据业务需求生成 Dify DSL YAML file
```

```text
帮我 review 这个 Dify YAML
```

### 最推荐的固定触发语句
```text
启动 Dify 工作流保姆式搭建流程
```

如果你已经有 Dify 页面 / 网址，也可以直接说：

```text
这是我的 Dify 部署网址，你自己进去看并继续帮我搭：
https://your-dify-url
```

或者：

```text
这是目标 app 的页面地址，你自己识别并继续搭建 / 修正：
https://your-dify-url/apps/xxx/workflow
```

---

## Agent 调用后会怎么带你走

### 情况 A：你只有业务需求
Agent 会按保姆式流程：
1. 业务梳理
2. 需求确认
3. 模式判断
4. 工作流设计
5. 生成 `Dify DSL YAML file`
6. 用户确认
7. 检查调试
8. 落地建议

### 情况 B：你直接给了 Dify URL
Agent 会：
1. 先识别 URL 类型
2. 锁定目标 app / workflow
3. 查看当前状态
4. 判断是新建还是改造
5. 再继续保姆式搭建 / 修正 / 联调

这意味着：
**你只给网址，Agent 也可以接着往下做。**

---

## 你应该怎么说，Agent 才最容易成功调用 skill

### 用于从零搭建
```text
启动 Dify 工作流保姆式搭建流程。
我要做一个工作流：用户上传图片后自动识别文字，并输出结构化结果。
```

### 用于根据业务生成 YAML
```text
帮我根据下面业务需求生成 Dify DSL YAML file，并告诉我怎么通过 Import DSL File 导入。
```

### 用于已有 Dify 页面 / app 继续推进
```text
这是 Dify app 页面地址，你自己识别目标 app，并继续帮我检查、修正、搭建和调试：
[粘贴 URL]
```

---

## 最后怎么落地到 Dify

生成后：
1. 保存 `.yml` / `.yaml`
2. 打开 Dify
3. 使用 **Import DSL File**
4. 导入后检查节点、工具、模型、变量
5. 跑真实测试

---

## 最关键的 3 句话

### 1
```text
启动 Dify 工作流保姆式搭建流程
```

### 2
```text
帮我根据业务需求生成 Dify DSL YAML file
```

### 3
```text
这是我的 Dify 页面地址，你自己识别并继续帮我搭建 / 修正：
[粘贴 URL]
```
