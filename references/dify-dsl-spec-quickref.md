# Dify DSL 快速结构参考

```yaml
app:
  description: ''
  icon: 🤖
  icon_background: '#FFEAD5'
  mode: workflow
  name: 示例工作流
  use_icon_as_answer_icon: false

dependencies: []
kind: app
version: 0.3.0
workflow:
  conversation_variables: []
  environment_variables: []
  features: {}
  graph:
    nodes: []
    edges: []
```

常见节点：
- start
- llm
- answer
- code
- http-request
- if-else
- tool
- parameter-extractor
- variable-aggregator
- iteration

变量引用：
- `{{#sys.query#}}`
- `{{#node_id.text#}}`
- `{{#node_id.output_field#}}`

导入要求：
- YAML 可解析
- 顶层结构完整
- graph.nodes 与 graph.edges 存在
- 节点 id 唯一
- edges 的 source / target 指向真实节点
```