# dify-workflow-builder

A production-oriented Agent Skill for **designing, generating, reviewing, refactoring, validating, and landing Dify workflows** from business requirements.

It helps users go from:

- business idea
- requirement clarification
- workflow architecture
- Dify DSL YAML generation
- import validation
- debugging and refinement

…all the way to a workflow that can be imported through **Dify → Import DSL File**.

---

## What it does

`dify-workflow-builder` is not just a YAML generator.
It is a full workflow-building skill that can:

1. **Clarify business requirements**
2. **Choose the right Dify mode**
   - `workflow`
   - `advanced-chat`
   - `rag_pipeline`
   - `agent-chat`
3. **Design the workflow structure**
4. **Generate importable Dify DSL YAML**
5. **Review existing Dify YAML/DSL**
6. **Refactor broken or messy flows**
7. **Validate whether a YAML is an Import DSL File candidate**
8. **Guide users through a nanny-style end-to-end flow**
9. **Use a Dify URL as entry context** to identify the target app and continue building/fixing

---

## Included capabilities

### Design & generation
- Business interview and requirement clarification
- Architecture planning
- Node and edge planning
- Dify-native DSL output

### Review & validation
- YAML structure review
- Node/edge integrity checks
- Import candidate validation
- Common Dify bug troubleshooting runbook

### Execution guidance
- Stage-based execution protocol
- Nanny-mode guided workflow building
- URL-driven entry into an existing Dify deployment/app

---

## Built-in templates

This project currently includes templates and generation paths for:

- `customer-service-chatflow`
- `api-orchestration-workflow`
- `form-collection-workflow`
- `rag-assistant-chatflow`
- `rag-pipeline-basic`
- `agent-tool-use`
- `ocr-to-structured-output`
- `text-to-html-or-file`
- `iteration-batch-workflow`
- `aggregator-summary-workflow`
- `question-classifier-workflow`
- `knowledge-retrieval-workflow`
- `assigner-memory-workflow`

Supported higher-frequency node families include:

- `if-else`
- `tool`
- `http-request`
- `code`
- `parameter-extractor`
- `iteration`
- `variable-aggregator`
- `question-classifier`
- `knowledge-retrieval`
- `assigner`

---

## How to use

### Typical trigger

Ask your Agent:

```text
Help me build a Dify workflow from this business requirement.
```

### Generate YAML directly

```text
Generate a Dify DSL YAML file from the following business requirement, and tell me how to import it through Import DSL File.
```

### Review existing YAML

```text
Review this Dify YAML and tell me whether it is an Import DSL File candidate.
```

### Start nanny mode

```text
启动 Dify 工作流保姆式搭建流程
```

### URL-driven continuation

```text
This is my Dify app URL. Identify the target app and continue helping me inspect, fix, and build the workflow:
https://your-dify-url/apps/xxx/workflow
```

---

## Output contract

The skill is designed to avoid dumping raw YAML too early.
It should normally output in this order:

1. task summary
2. mode selection
3. architecture plan
4. node list
5. edge list
6. risks / pending confirmations
7. `Dify DSL YAML file`
8. Import DSL File guidance

---

## Repository layout

```text
dify-workflow-builder/
├── SKILL.md
├── README.md
├── TUTORIAL.md
├── USER_GUIDE_FOR_DIFY_USERS.md
├── examples/
├── references/
└── scripts/
```

---

## References / inspirations

This project was informed and inspired by the following open repositories and skills:

1. **wwwzhouhui / skills_collection / dify-dsl-generator**
   - Repository directory:
     <https://github.com/wwwzhouhui/skills_collection/tree/main/dify-dsl-generator>
   - SKILL.md:
     <https://github.com/wwwzhouhui/skills_collection/blob/main/dify-dsl-generator/SKILL.md>
   - Main inspiration:
     - Dify DSL structure coverage
     - import-oriented YAML output thinking
     - node-level YAML examples

2. **lazeyliu / dify-dsl-generator-skills**
   - Repository:
     <https://github.com/lazeyliu/dify-dsl-generator-skills>
   - Main inspiration:
     - skill decomposition
     - author / review / refactor / governance routing
     - output contract and validation mindset

This repository is a new integrated implementation, not a verbatim copy of either source.

---

## Notes

- Importable does **not** automatically mean production-ready.
- Dify has real import / compatibility / UI edge cases, so review and validation remain important.
- For real Dify write-back flows, use UTF-8 file handoff and read-back verification.

---

## Author

Created and published by **Irfan Lee** (`lif199010-stack`) as an OpenClaw/Agent Skill project.
