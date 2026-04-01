# Dify URL 进入与识别协议

当用户直接提供 Dify 网址时，Agent 必须具备“通过 URL 进入 Dify、识别目标 app、查看现状、再搭建或修正”的能力。

---

## 支持的输入类型

### 1. Dify 部署根网址
例如：
- `https://dify.example.com`
- `https://cloud.dify.ai`

### 2. Dify App / Workflow 页面网址
例如：
- `https://dify.example.com/apps/<app_id>/workflow`
- `https://dify.example.com/app/<app_id>`
- 任何能明确定位到 app 的页面 URL

### 3. 带已有登录态的浏览器页面
如果用户说“我已经打开了 Dify 页面”，也应视为可进入。

---

## Agent 标准动作

当收到 Dify URL 时，按以下顺序执行：

### Phase 1：识别 URL 类型
先判断是：
- 根网址
- app 页面
- workflow 页面
- 仅控制台主页

### Phase 2：锁定目标
如果 URL 已含 app id：
- 直接锁目标 app
- 不要靠标题猜

如果 URL 不含 app id：
- 先进入控制台
- 再通过页面 / URL / app 列表定位目标 app
- 若存在多个近似 app，必须请用户确认目标对象

### Phase 3：查看现状
至少收集：
- 当前 app id
- 当前 app 名称
- 当前 mode
- 当前是否已有 workflow / draft
- 当前页面是否是目标页面

### Phase 4：决定路径
- 如果用户要新建：进入搭建流程
- 如果用户要修改现有：进入 review → refactor → validate
- 如果用户只给 URL 但目标不清：先澄清用户想新建还是改造

---

## 关键规则

### 规则 1：先锁 app id，再改 draft，再 publish
不要只凭标题、tab 文案或口头描述判断目标 workflow。

### 规则 2：URL > 标题
如果 URL 和页面标题不一致，以 URL 提取到的 app id 为准。

### 规则 3：若用户反馈“改了但没变化”
优先怀疑：
- 改错 app
- draft 目标错位
- 当前 tab 不是用户看的那个 app

### 规则 4：若需真实写入 Dify
必须走：
- 先识别当前 app
- 再写 draft
- 再确认 publish
- 再回读校验

---

## 保姆式模式下的增强动作

如果用户一边给 Dify URL，一边要求“保姆式引导”，Agent 应自动把 URL 作为环境上下文接入流程：

1. 先识别当前 Dify 部署和目标 app
2. 再做业务梳理与需求确认
3. 再根据现有 app 状态判断是新建 / 改造
4. 设计后可直接进入查看、修正、搭建、校验

也就是说：
**URL 输入不是额外负担，而是保姆式流程的入口之一。**
