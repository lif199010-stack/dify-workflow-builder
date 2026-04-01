#!/usr/bin/env node
/**
 * build_workflow.js - V2 Pro workflow scaffold generator
 */
const fs = require('fs');

const templates = {
  'customer-service-chatflow': {
    mode: 'advanced-chat',
    name: '智能客服',
    description: '多轮客服与问答，含意图识别、条件判断和工具分流',
    system_prompt: '你是专业客服，先判断用户意图，再给出清晰回复。',
    user_prompt: '用户问题：{{#sys.query#}}'
  },
  'api-orchestration-workflow': {
    mode: 'workflow',
    name: 'API编排流程',
    description: 'API 调用、参数提取、HTTP 请求、代码整理',
    system_prompt: '你负责理解输入并生成 API 调用前的结构化处理结果。',
    user_prompt: '输入：{{#sys.query#}}',
    api_url: 'https://api.example.com/endpoint'
  },
  'form-collection-workflow': {
    mode: 'workflow',
    name: '表单收集流程',
    description: '资料采集与汇总',
    system_prompt: '你负责引导用户逐步完成资料填写。',
    user_prompt: '用户输入：{{#sys.query#}}'
  },
  'iteration-batch-workflow': {
    mode: 'workflow',
    name: '批量迭代处理流程',
    description: '列表循环处理与结果汇总',
    system_prompt: '你负责把输入拆分为列表，再逐项处理。',
    user_prompt: '输入：{{#sys.query#}}'
  },
  'aggregator-summary-workflow': {
    mode: 'workflow',
    name: '聚合汇总流程',
    description: '多路输出聚合后总结',
    system_prompt: '你负责整合多个来源结果并生成总结。',
    user_prompt: '任务：{{#sys.query#}}'
  },
  'question-classifier-workflow': {
    mode: 'workflow',
    name: '问题分类流程',
    description: '问题分类与分流处理',
    system_prompt: '你负责对问题进行分类和路由。',
    user_prompt: '问题：{{#sys.query#}}'
  },
  'knowledge-retrieval-workflow': {
    mode: 'workflow',
    name: '知识检索流程',
    description: '知识检索后回答',
    system_prompt: '基于知识检索结果回答问题。',
    user_prompt: '问题：{{#sys.query#}}'
  },
  'assigner-memory-workflow': {
    mode: 'workflow',
    name: '变量写入流程',
    description: '读取输入并写入变量，再输出结果',
    system_prompt: '你负责整理用户输入并生成可写入变量的内容。',
    user_prompt: '输入：{{#sys.query#}}'
  },
  'rag-assistant-chatflow': {
    mode: 'advanced-chat',
    name: 'RAG问答助手',
    description: '知识库问答与解释',
    system_prompt: '你是知识助手，基于检索结果回答问题。',
    user_prompt: '问题：{{#sys.query#}}'
  },
  'rag-pipeline-basic': {
    mode: 'rag_pipeline',
    name: 'RAG Pipeline 基础版',
    description: '检索工具 + LLM 回答的基础 RAG Pipeline',
    system_prompt: '你是知识助手，严格根据检索结果回答。',
    user_prompt: '问题：{{#sys.query#}}'
  },
  'agent-tool-use': {
    mode: 'agent-chat',
    name: 'Agent工具助手',
    description: '复杂任务与工具协同',
    system_prompt: '你是工具型 Agent，按目标规划并调用工具。',
    user_prompt: '任务：{{#sys.query#}}'
  },
  'ocr-to-structured-output': {
    mode: 'workflow',
    name: 'OCR识别流程',
    description: '上传图片后识别并输出文字',
    system_prompt: '仅输出识别结果，不要添加多余解释。',
    user_prompt: ''
  },
  'text-to-html-or-file': {
    mode: 'advanced-chat',
    name: 'HTML生成流程',
    description: '根据文本生成HTML或文件内容，含参数提取',
    system_prompt: '根据用户描述生成可直接使用的 HTML 内容。',
    user_prompt: '需求：{{#sys.query#}}'
  }
};

function main() {
  const args = process.argv.slice(2);
  let template = null;
  let output = '/tmp/dify_workflow_builder_config.json';
  for (const arg of args) {
    if (arg.startsWith('--template=')) template = arg.split('=')[1];
    else if (arg.startsWith('--output=')) output = arg.split('=')[1];
  }
  if (!template || !templates[template]) {
    console.error('Available templates:');
    Object.keys(templates).forEach(k => console.error(`- ${k}`));
    process.exit(1);
  }
  fs.writeFileSync(output, JSON.stringify({ template, ...templates[template] }, null, 2), 'utf-8');
  console.log(output);
}
main();
