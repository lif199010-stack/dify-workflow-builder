# Dify Bug 排查 / 定位 / 修复 Runbook

这份 runbook 只记录两类内容：
1. 能被公开资料或源码证实的问题
2. 基于这些证据推导出的保守、可执行排查动作

不胡编，不把猜测写成结论。

---

## 一、先分层判断：问题出在哪一层

Dify 相关问题不要混在一起看，先分 4 层：

1. **DSL 文件层**
   - YAML 语法
   - 顶层结构
   - 节点 / 连边 / selector / 变量引用

2. **导入层（Import DSL File / imports API）**
   - 版本兼容
   - yaml-content / yaml-url 调用方式
   - malformed import

3. **运行层（工作流能否真正跑通）**
   - prompt / 模型 / 工具 / 插件依赖
   - 节点字段兼容性
   - 变量传递问题

4. **Dify 前端/UI 层**
   - 导入后画布异常
   - 页面 crash
   - 表单保存异常
   - 旧格式节点在 UI 中静默失败

先分层，再定位。

---

## 二、已证实的常见问题

### 1. `yaml_content is required when import_mode is yaml-content`

#### 已证实来源
- 官方 issue：#23492、#20383
- Dify 源码 `api/services/app_dsl_service.py` 中存在明确错误分支

#### 含义
调用 imports API 时，若使用 `import_mode=yaml-content`，但没有真正传 `yaml_content`，导入会失败。

#### 标准检查动作
- 确认你是走 UI 导入，还是走 API 导入
- 如果走 API：确认 body 里真有 `yaml_content`
- 不要只传文件名或空字段

#### 修复建议
- UI 导入优先，最稳
- API 导入时，显式传完整 YAML 字符串
- 若你其实传的是远程 URL，就不要伪装成 `yaml-content`

---

### 2. GitHub `blob` 链接与原始 YAML 获取问题

#### 已证实来源
- Dify 源码 `app_dsl_service.py`
- 代码会将 GitHub `blob` YAML URL 自动替换为 `raw.githubusercontent.com`

#### 含义
如果用 YAML URL 导入，Dify 对 GitHub `blob` 的 `.yml/.yaml` 链接有专门改写逻辑。

#### 标准检查动作
- 如果你给的是 GitHub URL，确认它是 `.yml/.yaml`
- 优先直接给 raw 链接，而不是普通仓库网页链接

#### 修复建议
- 最稳方式：直接使用 raw YAML URL
- 如果 URL 不是 `.yml/.yaml` 文件结尾，不要赌 Dify 能自动识别

---

### 3. DSL 版本兼容问题

#### 已证实来源
- Dify 源码当前主线里 `CURRENT_DSL_VERSION = "0.6.0"`
- 公开 issue：旧版本 YAML 无法导入 / 导入 warning / malformed import
- 旧文档和大量社区案例仍在使用 `0.3.0`

#### 含义
Dify 社区里大量案例仍是旧 DSL 版本，但服务端版本门槛在持续前进。旧 YAML 不是一定不能导入，但兼容性风险是真实存在的。

#### 标准检查动作
- 先看 YAML 里的 `version`
- 再看目标 Dify 实例版本
- 若 import 后只是 warning，不等于运行没问题

#### 修复建议
- 如果目标环境较新，尽量用更接近当前版本的结构
- 对历史 YAML：先做结构审查，再导入，不要直接批量导
- 旧案例先 review，再决定 refactor

---

### 4. malformed DSL 导入会造成 broken app / 页面异常

#### 已证实来源
- 官方 issue：#31804

#### 含义
不是所有错误都会在导入前被优雅拦截；某些 malformed DSL 可能导入成坏 app，甚至影响 `/apps` 页面。

#### 标准检查动作
- 导入前先本地审查：顶层结构、nodes、edges、id、引用
- 高风险 YAML 不要直接导入生产 Dify
- 先在测试环境导入

#### 修复建议
- 先用 `review_dify_yaml.py` 做结构审查
- 对高风险变更先做最小子集导入
- 保留原 YAML 备份，避免把唯一可用配置污染掉

---

### 5. 导入后流程一直 loading / 最终信息不显示

#### 已证实来源
- 官方 issue：#3643

#### 含义
有些 DSL 导入后运行态异常，并不是 YAML 语法错误，而是导入后的流程结构或字段兼容问题。

#### 标准检查动作
- 比较：同逻辑在 UI 手工重建是否正常
- 若 UI 重建正常、导入版异常，优先怀疑 import 兼容问题
- 检查最终输出节点是否真的连通
- 检查 answer/end 节点和 upstream 输出变量是否存在

#### 修复建议
- 对问题 DSL 做最小化：删掉可疑节点，只保留主链路再导入
- 若最小主链路正常，再逐步加回复杂节点
- 对 imported DSL 和 UI 手工版做 diff

---

### 6. custom tool / plugin 依赖导入后无法自动识别

#### 已证实来源
- 官方 issue：#10911、#20247
- 现象：工具项目 / DSL 项目跨系统迁移后，custom tools 无法自动重新绑定

#### 含义
即使 YAML 导入成功，依赖工具未必自动可用。

#### 标准检查动作
- 看 `dependencies` 是否声明了插件
- 看导入目标环境是否已安装对应插件 / tool
- 检查 tool node 的 `provider_id / tool_name / provider_name`

#### 修复建议
- 先安装依赖插件，再导入 DSL
- 对 custom tools，不要假设跨环境会自动映射
- 导入后逐个核对 tool node 是否成功绑定

---

### 7. LLM 配置变更后 workflow 异常

#### 已证实来源
- 官方 issue：#17169

#### 含义
某些 Dify 版本下，直接替换 LLM 配置 / provider / model 后，工作流可能变得不可访问或报错。

#### 标准检查动作
- 如果异常发生在“改模型之后”，优先怀疑节点配置兼容
- 检查 provider / model / completion_params 是否与当前实例支持能力一致

#### 修复建议
- 模型替换不要一次性全局替换，先改单节点验证
- 改完立即导出 / 备份当前 YAML
- 出问题时回退到最后一个可运行版本

---

### 8. 导出 / 导入对文件类型等字段的保真度不一致

#### 已证实来源
- 官方 issue：#19114、#21449

#### 含义
某些 file input 相关配置在导出后不一定被完整保留，或者 UI 录入时有特殊操作要求。

#### 标准检查动作
- 对 file input 节点重点检查：
  - `allowed_file_types`
  - `allowed_file_extensions`
  - `allowed_file_upload_methods`
- 导入后回到 UI 检查字段是否被吃掉

#### 修复建议
- 文件上传相关节点导入后必须人工复核一遍
- 不把“导出 DSL 正常”直接等价成“导入后字段完全保真”

---

### 9. 旧格式节点 / assigner / selector 兼容性问题

#### 已证实来源
- issue：#28862（legacy V1 data format）
- release 记录里有 selector 相关修复

#### 含义
某些旧格式节点即使不报错，也可能静默失败。

#### 标准检查动作
- 对 assigner / selector / conversation variable 相关节点重点检查
- 旧 YAML 导入后，不要只看是否导入成功，要跑一次真实路径

#### 修复建议
- 历史 YAML 优先迁到当前字段格式
- 变量相关节点必须做真实输入回放验证

---

## 三、标准排障流程（推荐照抄执行）

### Phase 1：先做静态审查
- YAML 能否解析
- 顶层结构是否完整
- nodes / edges 是否齐
- node id 是否唯一
- source / target 是否指向真实节点
- answer/end 是否存在

### Phase 2：再做导入校验
- Import DSL File 是否报错
- 是否有版本 warning
- 是否有 plugin / tool 缺失
- 导入后 UI 是否正常打开

### Phase 3：再做最小运行验证
- 从最短主链路跑通
- 检查输出节点能否出结果
- 再逐个加回复杂节点

### Phase 4：再做依赖校验
- model/provider 是否可用
- plugin 是否已安装
- tool node 是否已绑定
- API / HTTP 节点是否真实可调用

---

## 四、当没有现成确定解法时，怎么保守推进

如果公开资料没有明确修复结论，不要编一个“官方解法”。
正确做法是：

1. 先把问题归层：DSL / import / runtime / UI
2. 做最小复现版本
3. 对比：UI 手工搭建版 vs DSL 导入版
4. 缩小到最小出错节点
5. 给出**保守修复路径**，而不是假装知道根因

例如：
- 先删掉 tool / if-else / iteration，只保留 start → llm → answer
- 若可运行，则说明复杂节点是问题区
- 再逐个加回，定位到具体节点类型或字段

这类方法虽然慢，但可靠。

---

## 五、skill 内的行动建议

使用 `dify-workflow-builder` 时，遇到 bug 应优先这样做：

1. 先 `review`
2. 再 `refactor`
3. 最后 `validate`

而不是一上来大改 YAML。

因为 Dify 的问题很多并不是“语法错”，而是：
- 版本漂移
- 导入层兼容
- 插件绑定
- UI 静默异常
- 旧格式节点兼容

这也是为什么 skill 要先指导行动，而不是只堆更多节点。
