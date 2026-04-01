# URL 驱动的保姆式搭建流程

这是 `dify-url-entry.md` 与 `nanny-mode.md` 的组合协议。

适用场景：
- 用户直接扔一个 Dify 部署网址
- 用户直接扔一个 Dify app/workflow 页面 URL
- 用户说“我已经打开了 Dify 页面，你自己进去看”

---

## 目标

让 Agent 具备以下闭环：
- 从 URL 识别 Dify 部署 / app
- 进入查看当前 app 状态
- 判断是新建还是改造
- 再继续保姆式搭建 / 修正 / 联调流程

---

## 标准顺序

### 第 1 步：识别 URL
- 部署根网址？
- app 页面？
- workflow 页面？
- 控制台主页？

### 第 2 步：锁定目标
- 若 URL 含 app id：直接锁定
- 若 URL 不含 app id：进入后定位目标 app
- 若多个 app 近似：请用户确认

### 第 3 步：查看现状
- 当前 app 名称
- 当前 app id
- 当前 mode
- 是否已有 workflow
- 是否有 draft

### 第 4 步：决定路径
- 新建 → 进入保姆式搭建
- 修改 → review → refactor → validate
- 不清楚 → 先澄清用户意图

### 第 5 步：自主推进
如果用户授权明确，Agent 可以继续：
- 查看页面
- 核 app
- 生成方案
- 修 draft
- 发布
- 回读校验

---

## 关键提醒

- URL 是环境入口，不是可忽略信息
- Dify 任务里，用户给 URL 时，应优先利用 URL 锁定 app，而不是重新询问一遍 app 名称
- 用户只给 URL 但没说清“新建还是改造”，必须问一次，但不需要从零问所有上下文
