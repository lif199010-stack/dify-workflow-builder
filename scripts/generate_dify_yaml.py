#!/usr/bin/env python3
import argparse, json
from pathlib import Path


def q(value):
    if isinstance(value, bool):
        return 'true' if value else 'false'
    if value is None:
        return 'null'
    if isinstance(value, (int, float)):
        return str(value)
    s = str(value).replace("'", "''")
    return f"'{s}'"


def simple_header(mode, name, desc, icon='#FFEAD5'):
    return f"app:\n  description: {q(desc)}\n  icon: 🤖\n  icon_background: '{icon}'\n  mode: {mode}\n  name: {q(name)}\n  use_icon_as_answer_icon: false\n\ndependencies: []\nkind: app\nversion: 0.3.0\n"


def build_iteration_yaml(name, desc, provider, model, input_label):
    return simple_header('workflow', name, desc) + f"""workflow:
  conversation_variables: []
  environment_variables: []
  features: {{}}
  graph:
    nodes:
      - data:
          title: 开始
          type: start
          variables:
            - label: {q(input_label)}
              max_length: 4000
              options: []
              required: true
              type: paragraph
              variable: query
        id: start
        position: {{ x: 80, y: 280 }}
        type: custom
        width: 244
        height: 90
      - data:
          title: 拆分列表
          type: code
          code_language: python3
          code: |
            def main(query: str) -> dict:
                items = [x.strip() for x in query.split(',') if x.strip()]
                return {{"items": items}}
          outputs:
            items:
              type: array[string]
          variables:
            - variable: query
              value_selector:
                - start
                - query
        id: split_code
        position: {{ x: 380, y: 280 }}
        type: custom
        width: 244
        height: 90
      - data:
          title: 列表循环
          type: iteration
          iterator_selector:
            - split_code
            - items
          output_selector:
            - item_llm
            - text
          output_type: array[string]
          startNodeType: llm
          start_node_id: item_llm
        id: iter_node
        position: {{ x: 700, y: 280 }}
        type: custom
        width: 244
        height: 90
      - data:
          title: 单项处理
          type: llm
          model:
            provider: {provider}
            name: {q(model)}
            mode: chat
            completion_params: {{ temperature: 0.2 }}
          prompt_template:
            - id: s1
              role: system
              text: '处理单个列表项并输出结果。'
            - id: u1
              role: user
              text: '项目：{{#split_code.items#}}'
          vision:
            enabled: false
        id: item_llm
        position: {{ x: 1020, y: 280 }}
        type: custom
        width: 244
        height: 90
      - data:
          title: 直接回复
          type: answer
          answer: '{{{{#item_llm.text#}}}}'
          variables: []
        id: answer
        position: {{ x: 1340, y: 280 }}
        type: custom
        width: 244
        height: 90
    edges:
      - data: {{ isInIteration: false, isInLoop: false, sourceType: start, targetType: code }}
        id: start-source-split_code-target
        source: start
        sourceHandle: source
        target: split_code
        targetHandle: target
        type: custom
        zIndex: 0
      - data: {{ isInIteration: false, isInLoop: false, sourceType: code, targetType: iteration }}
        id: split_code-source-iter_node-target
        source: split_code
        sourceHandle: source
        target: iter_node
        targetHandle: target
        type: custom
        zIndex: 0
      - data: {{ isInIteration: false, isInLoop: false, sourceType: iteration, targetType: llm }}
        id: iter_node-source-item_llm-target
        source: iter_node
        sourceHandle: source
        target: item_llm
        targetHandle: target
        type: custom
        zIndex: 0
      - data: {{ isInIteration: false, isInLoop: false, sourceType: llm, targetType: answer }}
        id: item_llm-source-answer-target
        source: item_llm
        sourceHandle: source
        target: answer
        targetHandle: target
        type: custom
        zIndex: 0
"""


def build_aggregator_yaml(name, desc, provider, model, input_label):
    return simple_header('workflow', name, desc) + f"""workflow:
  conversation_variables: []
  environment_variables: []
  features: {{}}
  graph:
    nodes:
      - data:
          title: 开始
          type: start
          variables:
            - label: {q(input_label)}
              max_length: 4000
              options: []
              required: true
              type: paragraph
              variable: query
        id: start
        position: {{ x: 80, y: 280 }}
        type: custom
        width: 244
        height: 90
      - data:
          title: 路径A
          type: llm
          model:
            provider: {provider}
            name: {q(model)}
            mode: chat
            completion_params: {{ temperature: 0.2 }}
          prompt_template:
            - id: a1
              role: system
              text: '从角度A分析输入。'
            - id: a2
              role: user
              text: '输入：{{#sys.query#}}'
          vision: {{ enabled: false }}
        id: llm_a
        position: {{ x: 380, y: 180 }}
        type: custom
        width: 244
        height: 90
      - data:
          title: 路径B
          type: llm
          model:
            provider: {provider}
            name: {q(model)}
            mode: chat
            completion_params: {{ temperature: 0.2 }}
          prompt_template:
            - id: b1
              role: system
              text: '从角度B分析输入。'
            - id: b2
              role: user
              text: '输入：{{#sys.query#}}'
          vision: {{ enabled: false }}
        id: llm_b
        position: {{ x: 380, y: 380 }}
        type: custom
        width: 244
        height: 90
      - data:
          title: 变量聚合器
          type: variable-aggregator
          groups:
            - group_name: summary_group
              output_type: string
              variables:
                - variable: from_a
                  value_selector:
                    - llm_a
                    - text
                - variable: from_b
                  value_selector:
                    - llm_b
                    - text
        id: aggregator
        position: {{ x: 740, y: 280 }}
        type: custom
        width: 244
        height: 90
      - data:
          title: 汇总生成
          type: llm
          model:
            provider: {provider}
            name: {q(model)}
            mode: chat
            completion_params: {{ temperature: 0.2 }}
          prompt_template:
            - id: c1
              role: system
              text: '整合两个来源结果，生成统一总结。'
            - id: c2
              role: user
              text: 'A：{{#llm_a.text#}}\nB：{{#llm_b.text#}}'
          vision: {{ enabled: false }}
        id: summary_llm
        position: {{ x: 1080, y: 280 }}
        type: custom
        width: 244
        height: 90
      - data:
          title: 直接回复
          type: answer
          answer: '{{{{#summary_llm.text#}}}}'
          variables: []
        id: answer
        position: {{ x: 1400, y: 280 }}
        type: custom
        width: 244
        height: 90
    edges:
      - data: {{ isInIteration: false, isInLoop: false, sourceType: start, targetType: llm }}
        id: start-source-llm_a-target
        source: start
        sourceHandle: source
        target: llm_a
        targetHandle: target
        type: custom
        zIndex: 0
      - data: {{ isInIteration: false, isInLoop: false, sourceType: start, targetType: llm }}
        id: start-source-llm_b-target
        source: start
        sourceHandle: source
        target: llm_b
        targetHandle: target
        type: custom
        zIndex: 0
      - data: {{ isInIteration: false, isInLoop: false, sourceType: llm, targetType: variable-aggregator }}
        id: llm_a-source-aggregator-target
        source: llm_a
        sourceHandle: source
        target: aggregator
        targetHandle: target
        type: custom
        zIndex: 0
      - data: {{ isInIteration: false, isInLoop: false, sourceType: llm, targetType: variable-aggregator }}
        id: llm_b-source-aggregator-target
        source: llm_b
        sourceHandle: source
        target: aggregator
        targetHandle: target
        type: custom
        zIndex: 0
      - data: {{ isInIteration: false, isInLoop: false, sourceType: variable-aggregator, targetType: llm }}
        id: aggregator-source-summary_llm-target
        source: aggregator
        sourceHandle: source
        target: summary_llm
        targetHandle: target
        type: custom
        zIndex: 0
      - data: {{ isInIteration: false, isInLoop: false, sourceType: llm, targetType: answer }}
        id: summary_llm-source-answer-target
        source: summary_llm
        sourceHandle: source
        target: answer
        targetHandle: target
        type: custom
        zIndex: 0
"""


def build_classifier_yaml(name, desc, provider, model, input_label):
    return simple_header('workflow', name, desc) + f"""workflow:
  conversation_variables: []
  environment_variables: []
  features: {{}}
  graph:
    nodes:
      - data:
          title: 开始
          type: start
          variables:
            - label: {q(input_label)}
              max_length: 4000
              options: []
              required: true
              type: paragraph
              variable: query
        id: start
        position: {{ x: 80, y: 280 }}
        type: custom
        width: 244
        height: 90
      - data:
          title: 问题分类
          type: question-classifier
          classes:
            - id: c1
              name: product
            - id: c2
              name: support
          model:
            provider: {provider}
            name: {q(model)}
            mode: chat
            completion_params: {{ temperature: 0.1 }}
          query:
            - start
            - query
          instruction: '将问题分类为 product 或 support'
        id: classifier
        position: {{ x: 380, y: 280 }}
        type: custom
        width: 244
        height: 90
      - data:
          title: 产品回答
          type: llm
          model:
            provider: {provider}
            name: {q(model)}
            mode: chat
            completion_params: {{ temperature: 0.2 }}
          prompt_template:
            - id: p1
              role: system
              text: '你负责回答产品咨询。'
            - id: p2
              role: user
              text: '问题：{{#start.query#}}'
          vision: {{ enabled: false }}
        id: llm_product
        position: {{ x: 740, y: 180 }}
        type: custom
        width: 244
        height: 90
      - data:
          title: 售后回答
          type: llm
          model:
            provider: {provider}
            name: {q(model)}
            mode: chat
            completion_params: {{ temperature: 0.2 }}
          prompt_template:
            - id: s1
              role: system
              text: '你负责回答售后问题。'
            - id: s2
              role: user
              text: '问题：{{#start.query#}}'
          vision: {{ enabled: false }}
        id: llm_support
        position: {{ x: 740, y: 380 }}
        type: custom
        width: 244
        height: 90
      - data:
          title: 直接回复
          type: answer
          answer: '{{{{#llm_product.text#}}}}\n{{{{#llm_support.text#}}}}'
          variables: []
        id: answer
        position: {{ x: 1080, y: 280 }}
        type: custom
        width: 244
        height: 90
    edges:
      - data: {{ isInIteration: false, isInLoop: false, sourceType: start, targetType: question-classifier }}
        id: start-source-classifier-target
        source: start
        sourceHandle: source
        target: classifier
        targetHandle: target
        type: custom
        zIndex: 0
      - data: {{ isInIteration: false, isInLoop: false, sourceType: question-classifier, targetType: llm }}
        id: classifier-source-llm_product-target
        source: classifier
        sourceHandle: source
        target: llm_product
        targetHandle: target
        type: custom
        zIndex: 0
      - data: {{ isInIteration: false, isInLoop: false, sourceType: question-classifier, targetType: llm }}
        id: classifier-source-llm_support-target
        source: classifier
        sourceHandle: source
        target: llm_support
        targetHandle: target
        type: custom
        zIndex: 0
      - data: {{ isInIteration: false, isInLoop: false, sourceType: llm, targetType: answer }}
        id: llm_product-source-answer-target
        source: llm_product
        sourceHandle: source
        target: answer
        targetHandle: target
        type: custom
        zIndex: 0
      - data: {{ isInIteration: false, isInLoop: false, sourceType: llm, targetType: answer }}
        id: llm_support-source-answer-target
        source: llm_support
        sourceHandle: source
        target: answer
        targetHandle: target
        type: custom
        zIndex: 0
"""


def build_knowledge_yaml(name, desc, provider, model, input_label):
    return simple_header('workflow', name, desc) + f"""workflow:
  conversation_variables: []
  environment_variables: []
  features: {{}}
  graph:
    nodes:
      - data:
          title: 开始
          type: start
          variables:
            - label: {q(input_label)}
              max_length: 4000
              options: []
              required: true
              type: paragraph
              variable: query
        id: start
        position: {{ x: 80, y: 280 }}
        type: custom
        width: 244
        height: 90
      - data:
          title: 知识检索
          type: knowledge-retrieval
          query_variable_selector:
            - start
            - query
          dataset_ids: []
          retrieval_mode: multiple
          top_k: 4
        id: knowledge_node
        position: {{ x: 380, y: 280 }}
        type: custom
        width: 244
        height: 90
      - data:
          title: 回答生成
          type: llm
          model:
            provider: {provider}
            name: {q(model)}
            mode: chat
            completion_params: {{ temperature: 0.2 }}
          prompt_template:
            - id: k1
              role: system
              text: '基于知识检索结果回答问题。'
            - id: k2
              role: user
              text: '问题：{{#start.query#}}\n知识：{{#knowledge_node.result#}}'
          vision: {{ enabled: false }}
        id: llm_answer
        position: {{ x: 700, y: 280 }}
        type: custom
        width: 244
        height: 90
      - data:
          title: 直接回复
          type: answer
          answer: '{{{{#llm_answer.text#}}}}'
          variables: []
        id: answer
        position: {{ x: 1020, y: 280 }}
        type: custom
        width: 244
        height: 90
    edges:
      - data: {{ isInIteration: false, isInLoop: false, sourceType: start, targetType: knowledge-retrieval }}
        id: start-source-knowledge_node-target
        source: start
        sourceHandle: source
        target: knowledge_node
        targetHandle: target
        type: custom
        zIndex: 0
      - data: {{ isInIteration: false, isInLoop: false, sourceType: knowledge-retrieval, targetType: llm }}
        id: knowledge_node-source-llm_answer-target
        source: knowledge_node
        sourceHandle: source
        target: llm_answer
        targetHandle: target
        type: custom
        zIndex: 0
      - data: {{ isInIteration: false, isInLoop: false, sourceType: llm, targetType: answer }}
        id: llm_answer-source-answer-target
        source: llm_answer
        sourceHandle: source
        target: answer
        targetHandle: target
        type: custom
        zIndex: 0
"""


def build_assigner_yaml(name, desc, provider, model, input_label):
    return simple_header('workflow', name, desc) + f"""workflow:
  conversation_variables: []
  environment_variables: []
  features: {{}}
  graph:
    nodes:
      - data:
          title: 开始
          type: start
          variables:
            - label: {q(input_label)}
              max_length: 4000
              options: []
              required: true
              type: paragraph
              variable: query
        id: start
        position: {{ x: 80, y: 280 }}
        type: custom
        width: 244
        height: 90
      - data:
          title: 整理输入
          type: llm
          model:
            provider: {provider}
            name: {q(model)}
            mode: chat
            completion_params: {{ temperature: 0.1 }}
          prompt_template:
            - id: a1
              role: system
              text: '把用户输入整理为一句标准摘要。'
            - id: a2
              role: user
              text: '输入：{{#start.query#}}'
          vision: {{ enabled: false }}
        id: llm_clean
        position: {{ x: 380, y: 280 }}
        type: custom
        width: 244
        height: 90
      - data:
          title: 变量赋值
          type: assigner
          assigned_variable_selector:
            - conversation
            - latest_summary
          input_variable_selector:
            - llm_clean
            - text
          write_mode: overwrite
          version: '2'
          items:
            - operation: overwrite
              value_selector:
                - llm_clean
                - text
        id: assign_node
        position: {{ x: 700, y: 280 }}
        type: custom
        width: 244
        height: 90
      - data:
          title: 直接回复
          type: answer
          answer: '{{{{#llm_clean.text#}}}}'
          variables: []
        id: answer
        position: {{ x: 1020, y: 280 }}
        type: custom
        width: 244
        height: 90
    edges:
      - data: {{ isInIteration: false, isInLoop: false, sourceType: start, targetType: llm }}
        id: start-source-llm_clean-target
        source: start
        sourceHandle: source
        target: llm_clean
        targetHandle: target
        type: custom
        zIndex: 0
      - data: {{ isInIteration: false, isInLoop: false, sourceType: llm, targetType: assigner }}
        id: llm_clean-source-assign_node-target
        source: llm_clean
        sourceHandle: source
        target: assign_node
        targetHandle: target
        type: custom
        zIndex: 0
      - data: {{ isInIteration: false, isInLoop: false, sourceType: assigner, targetType: answer }}
        id: assign_node-source-answer-target
        source: assign_node
        sourceHandle: source
        target: answer
        targetHandle: target
        type: custom
        zIndex: 0
"""


def build_placeholder_existing(cfg):
    # keep older high-frequency templates usable with compact skeletons
    mode = cfg.get('mode', 'workflow')
    name = cfg.get('name', 'Dify Workflow')
    desc = cfg.get('description', 'Generated by dify-workflow-builder V2 Pro')
    provider = cfg.get('model_provider', 'openai')
    model = cfg.get('model_name', 'gpt-4')
    input_label = cfg.get('input_label', '用户输入')
    return simple_header(mode, name, desc) + f"""workflow:
  conversation_variables: []
  environment_variables: []
  features: {{}}
  graph:
    nodes:
      - data:
          title: 开始
          type: start
          variables:
            - label: {q(input_label)}
              max_length: 4000
              options: []
              required: true
              type: paragraph
              variable: query
        id: start
        position: {{ x: 80, y: 280 }}
        type: custom
        width: 244
        height: 90
      - data:
          title: 核心处理
          type: llm
          model:
            provider: {provider}
            name: {q(model)}
            mode: chat
            completion_params: {{ temperature: 0.3 }}
          prompt_template:
            - id: s1
              role: system
              text: '请根据用户输入完成任务。'
            - id: u1
              role: user
              text: '输入：{{#sys.query#}}'
          vision: {{ enabled: false }}
        id: core_llm
        position: {{ x: 380, y: 280 }}
        type: custom
        width: 244
        height: 90
      - data:
          title: 直接回复
          type: answer
          answer: '{{{{#core_llm.text#}}}}'
          variables: []
        id: answer
        position: {{ x: 700, y: 280 }}
        type: custom
        width: 244
        height: 90
    edges:
      - data: {{ isInIteration: false, isInLoop: false, sourceType: start, targetType: llm }}
        id: start-source-core_llm-target
        source: start
        sourceHandle: source
        target: core_llm
        targetHandle: target
        type: custom
        zIndex: 0
      - data: {{ isInIteration: false, isInLoop: false, sourceType: llm, targetType: answer }}
        id: core_llm-source-answer-target
        source: core_llm
        sourceHandle: source
        target: answer
        targetHandle: target
        type: custom
        zIndex: 0
"""


def build_agent_yaml(cfg):
    name = cfg.get('name', 'Dify Agent')
    desc = cfg.get('description', 'Generated by dify-workflow-builder V2 Pro')
    provider = cfg.get('model_provider', 'openai')
    model = cfg.get('model_name', 'gpt-4')
    return f"""app:
  description: {q(desc)}
  icon: 🤖
  icon_background: '#FFEAD5'
  mode: agent-chat
  name: {q(name)}
  use_icon_as_answer_icon: false
dependencies: []
kind: app
model_config:
  agent_mode:
    enabled: true
    max_iteration: 5
    prompt: null
    strategy: function_call
    tools: []
  annotation_reply:
    enabled: false
  chat_prompt_config: {{}}
  completion_prompt_config: {{}}
  dataset_configs:
    datasets:
      datasets: []
    reranking_enable: false
    retrieval_model: multiple
    top_k: 4
  dataset_query_variable: ''
  external_data_tools: []
  file_upload:
    enabled: false
    allowed_file_extensions: []
    allowed_file_types: []
    allowed_file_upload_methods:
      - remote_url
      - local_file
    image:
      enabled: false
      detail: high
      number_limits: 3
      transfer_methods:
        - remote_url
        - local_file
    number_limits: 3
  model:
    completion_params:
      stop: []
    mode: chat
    name: {q(model)}
    provider: {provider}
  more_like_this:
    enabled: false
  opening_statement: ''
  pre_prompt: ''
  prompt_type: simple
  retriever_resource:
    enabled: true
  sensitive_word_avoidance:
    configs: []
    enabled: false
    type: ''
  speech_to_text:
    enabled: false
  suggested_questions: []
  suggested_questions_after_answer:
    enabled: false
  text_to_speech:
    enabled: false
    language: ''
    voice: ''
  user_input_form: []
version: 0.3.0
"""


def build_from_config(cfg):
    mode = cfg.get('mode', 'workflow')
    if mode == 'agent-chat':
        return build_agent_yaml(cfg)

    name = cfg.get('name', 'Dify Workflow')
    desc = cfg.get('description', 'Generated by dify-workflow-builder V2 Pro')
    provider = cfg.get('model_provider', 'openai')
    model = cfg.get('model_name', 'gpt-4')
    input_label = cfg.get('input_label', '用户输入')
    template = cfg.get('template', 'basic-assistant')

    if template == 'iteration-batch-workflow':
        return build_iteration_yaml(name, desc, provider, model, input_label)
    if template == 'aggregator-summary-workflow':
        return build_aggregator_yaml(name, desc, provider, model, input_label)
    if template == 'question-classifier-workflow':
        return build_classifier_yaml(name, desc, provider, model, input_label)
    if template == 'knowledge-retrieval-workflow':
        return build_knowledge_yaml(name, desc, provider, model, input_label)
    if template == 'assigner-memory-workflow':
        return build_assigner_yaml(name, desc, provider, model, input_label)

    return build_placeholder_existing(cfg)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--config', required=True)
    ap.add_argument('--out', required=True)
    args = ap.parse_args()
    cfg = json.loads(Path(args.config).read_text(encoding='utf-8'))
    text = build_from_config(cfg)
    Path(args.out).write_text(text, encoding='utf-8')
    print(args.out)


if __name__ == '__main__':
    main()
