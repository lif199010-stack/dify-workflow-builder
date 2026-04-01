#!/usr/bin/env python3
import argparse
import re
import sys
from pathlib import Path


def find_mode(text):
    m = re.search(r'^\s*mode:\s*([A-Za-z_\-]+)\s*$', text, re.M)
    return m.group(1) if m else None


def count_token(text, token):
    return len(re.findall(re.escape(token), text))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('file')
    args = ap.parse_args()

    text = Path(args.file).read_text(encoding='utf-8')
    problems = []
    warnings = []

    for key in ['app:', 'kind:', 'version:']:
        if key not in text:
            problems.append(f'missing top-level key: {key[:-1]}')

    mode = find_mode(text)
    if not mode:
        warnings.append('app.mode not found explicitly')

    has_workflow = 'workflow:' in text
    has_model_config = 'model_config:' in text

    if has_workflow:
        for k in ['graph:', 'nodes:', 'edges:']:
            if k not in text:
                problems.append(f'missing workflow.{k[:-1]}' if k == 'graph:' else f'missing {k[:-1]}')

    if mode == 'agent-chat' and not has_model_config:
        problems.append('agent-chat mode missing model_config')
    if mode == 'rag_pipeline' and not has_workflow:
        problems.append('rag_pipeline mode missing workflow block')

    node_ids = re.findall(r'^\s*id:\s*([A-Za-z0-9_\-]+)\s*$', text, re.M)
    edge_id_like = [nid for nid in node_ids if '-source-' in nid and '-target' in nid]
    node_like_ids = [nid for nid in node_ids if nid not in edge_id_like]

    seen = set()
    duplicates = set()
    for nid in node_like_ids:
        if nid in seen:
            duplicates.add(nid)
        seen.add(nid)
    for nid in sorted(duplicates):
        problems.append(f'duplicate node id: {nid}')

    if has_workflow:
        if 'type: start' not in text:
            problems.append('missing start node')
        if 'type: answer' not in text and 'type: end' not in text:
            problems.append('missing visible output node (answer/end)')

    if '{{#' in text and '#}}' not in text:
        problems.append('broken variable reference syntax')

    var_refs = re.findall(r'\{\{#([A-Za-z0-9_\-]+)\.([A-Za-z0-9_\-]+)#\}\}', text)
    for node_id, field in var_refs:
        if node_id != 'sys' and node_id not in node_like_ids:
            warnings.append(f'variable reference points to unknown node: {node_id}.{field}')

    edge_sources = re.findall(r'^\s*source:\s*([A-Za-z0-9_\-]+)\s*$', text, re.M)
    edge_targets = re.findall(r'^\s*target:\s*([A-Za-z0-9_\-]+)\s*$', text, re.M)
    for s in edge_sources:
        if s not in node_like_ids:
            problems.append(f'edge source not found in node ids: {s}')
    for t in edge_targets:
        if t not in node_like_ids:
            problems.append(f'edge target not found in node ids: {t}')

    if 'dependencies:' in text and 'marketplace_plugin_unique_identifier:' not in text:
        warnings.append('dependencies block exists but no explicit marketplace plugin identifiers found')

    has_if_else = 'type: if-else' in text
    has_tool = 'type: tool' in text
    has_http = 'type: http-request' in text
    has_code = 'type: code' in text
    has_param_extract = 'type: parameter-extractor' in text
    has_iteration = 'type: iteration' in text
    has_aggregator = 'type: variable-aggregator' in text
    has_classifier = 'type: question-classifier' in text
    has_knowledge = 'type: knowledge-retrieval' in text
    has_assigner = 'type: assigner' in text

    if has_if_else and count_token(text, 'case_id:') == 0:
        warnings.append('if-else node found without explicit case_id block')
    if has_http and 'url:' not in text:
        problems.append('http-request node missing url')
    if has_http and 'method:' not in text:
        warnings.append('http-request node missing explicit method')
    if has_tool and 'tool_name:' not in text:
        problems.append('tool node missing tool_name')
    if has_code and 'code:' not in text:
        problems.append('code node missing code body')
    if has_param_extract and 'parameters:' not in text:
        warnings.append('parameter-extractor missing parameters definition')
    if has_iteration and 'iterator_selector:' not in text:
        problems.append('iteration node missing iterator_selector')
    if has_aggregator and 'groups:' not in text:
        problems.append('variable-aggregator missing groups')
    if has_classifier and 'classes:' not in text:
        problems.append('question-classifier missing classes')
    if has_knowledge and 'query_variable_selector:' not in text:
        warnings.append('knowledge-retrieval missing query_variable_selector')
    if has_assigner and 'assigned_variable_selector:' not in text:
        problems.append('assigner missing assigned_variable_selector')
    if has_assigner and 'version:' not in text:
        warnings.append('assigner may be using incomplete legacy format')

    print(f'Mode: {mode or "unknown"}')
    print(f'Node ids: {len(node_like_ids)}')
    print(f'Edge refs: {len(edge_sources)}')
    print('Capabilities: '
          f'if-else={has_if_else}, tool={has_tool}, http-request={has_http}, code={has_code}, '
          f'parameter-extractor={has_param_extract}, iteration={has_iteration}, '
          f'variable-aggregator={has_aggregator}, question-classifier={has_classifier}, '
          f'knowledge-retrieval={has_knowledge}, assigner={has_assigner}')

    if problems:
        print('Review result: BLOCKED')
        for item in problems:
            print(f'- {item}')
        if warnings:
            print('Warnings:')
            for item in warnings:
                print(f'- {item}')
        sys.exit(2)

    print('Review result: IMPORT_CANDIDATE')
    print('- top-level structure looks complete')
    if mode == 'agent-chat':
        print('- agent-chat structure detected with model_config')
    elif mode == 'rag_pipeline':
        print('- rag_pipeline structure detected with workflow graph')
    elif has_workflow:
        print('- workflow/chatflow structure detected with graph/nodes/edges')
    print('- no blocking node/edge integrity issue found')
    print('- variable reference syntax looks consistent')
    if warnings:
        print('Warnings:')
        for item in warnings:
            print(f'- {item}')


if __name__ == '__main__':
    main()
