# Dify YAML 审查清单

## 结构完整性
- [ ] 顶层有 app / kind / version / workflow
- [ ] workflow.graph.nodes 存在
- [ ] workflow.graph.edges 存在
- [ ] 至少有 start 节点
- [ ] 至少有 answer / end / 可见输出节点

## 节点质量
- [ ] 节点 id 唯一
- [ ] type 合法
- [ ] LLM 节点有 model / prompt
- [ ] code 节点有 code / outputs
- [ ] tool / http-request 节点关键配置存在

## 连边质量
- [ ] source / target 节点真实存在
- [ ] 没有孤立核心节点
- [ ] 主链路可从 start 走到输出
- [ ] 分支节点条件有意义

## 变量 / selector
- [ ] 变量引用格式正确
- [ ] selector 指向存在字段
- [ ] 没有明显拼错的 node id

## 导入判断
- [ ] YAML 语法可解析
- [ ] 满足 Import DSL File 基本结构
- [ ] 阻塞项已列出
- [ ] 待确认项已列出
