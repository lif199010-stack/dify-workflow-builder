#!/usr/bin/env node
/**
 * inject_json_editor.js - 富前端 JSON 编辑器注入脚本
 * 
 * 用途：
 * - 飞书开发者后台"批量导入权限"等 JSON 编辑器
 * - Dify 复杂的 workflow 配置注入
 * 
 * 问题：普通 type/fill 会出现内容错位/叠字
 * 根因：这类页面是 Monaco/CodeMirror/contenteditable 组件，不是普通 <textarea>
 * 
 * 用法：
 *   node inject_json_editor.js --print                    # 输出可直接用于 browser evaluate 的脚本
 *   node inject_json_editor.js --file payload.json --print # 使用自定义 payload
 */

const fs = require('fs');

function generateInjector(payload) {
  const escapedPayload = JSON.stringify(payload).slice(1, -1);
  
  return `
(function() {
  const payload = "${escapedPayload}";
  const data = JSON.parse(payload);
  
  // 策略 1: Monaco Editor
  const monacoEditor = document.querySelector('.monaco-editor');
  if (monacoEditor && window.monaco) {
    const model = monacoEditor.__monaco_model || 
                  monacoEditor.querySelector('[role="textbox"]')?.monaco_model;
    if (model) {
      model.setValue(JSON.stringify(data, null, 2));
      model.pushEditOperations([], [], () => null);
      console.log('[Injector] Monaco Editor 注入成功');
      return true;
    }
  }
  
  // 策略 2: CodeMirror
  const cmEditor = document.querySelector('.CodeMirror');
  if (cmEditor && cmEditor.CodeMirror) {
    cmEditor.CodeMirror.setValue(JSON.stringify(data, null, 2));
    cmEditor.CodeMirror.refresh();
    console.log('[Injector] CodeMirror 注入成功');
    return true;
  }
  
  // 策略 3: contenteditable
  const contentEditable = document.querySelector('[contenteditable="true"]');
  if (contentEditable) {
    contentEditable.focus();
    contentEditable.textContent = JSON.stringify(data, null, 2);
    contentEditable.dispatchEvent(new InputEvent('input', { bubbles: true }));
    contentEditable.dispatchEvent(new Event('change', { bubbles: true }));
    console.log('[Injector] ContentEditable 注入成功');
    return true;
  }
  
  // 策略 4: textarea
  const textarea = document.querySelector('textarea');
  if (textarea) {
    textarea.value = JSON.stringify(data, null, 2);
    textarea.dispatchEvent(new InputEvent('input', { bubbles: true }));
    textarea.dispatchEvent(new Event('change', { bubbles: true }));
    console.log('[Injector] Textarea 注入成功');
    return true;
  }
  
  // 策略 5: 通用 fallback
  const anyInput = document.querySelector('input, textarea, [contenteditable]');
  if (anyInput) {
    if (anyInput.tagName === 'INPUT' || anyInput.tagName === 'TEXTAREA') {
      anyInput.value = JSON.stringify(data, null, 2);
    } else {
      anyInput.textContent = JSON.stringify(data, null, 2);
    }
    anyInput.dispatchEvent(new InputEvent('input', { bubbles: true }));
    anyInput.dispatchEvent(new Event('change', { bubbles: true }));
    console.log('[Injector] 通用注入成功');
    return true;
  }
  
  console.error('[Injector] 未找到可注入的编辑器');
  return false;
})();
  `.trim();
}

function generateWithButtonTrigger(payload) {
  const escapedPayload = JSON.stringify(payload).slice(1, -1);
  
  return `
(function() {
  const payload = "${escapedPayload}";
  const data = JSON.parse(payload);
  
  function triggerSave() {
    // 尝试触发附近的确认/保存按钮
    const buttons = document.querySelectorAll('button');
    for (const btn of buttons) {
      const text = btn.textContent.toLowerCase();
      if (text.includes('确认') || text.includes('保存') || text.includes('确定') || 
          text.includes('save') || text.includes('confirm') || text.includes('next') ||
          text.includes('下一步')) {
        btn.click();
        console.log('[Injector] 已触发按钮:', btn.textContent);
        return true;
      }
    }
    return false;
  }
  
  // 执行注入
  let injected = false;
  
  // Monaco
  const monacoEditor = document.querySelector('.monaco-editor');
  if (!injected && monacoEditor && window.monaco) {
    const model = monacoEditor.__monaco_model || 
                  monacoEditor.querySelector('[role="textbox"]')?.monaco_model;
    if (model) {
      model.setValue(JSON.stringify(data, null, 2));
      model.pushEditOperations([], [], () => null);
      injected = true;
      console.log('[Injector] Monaco Editor');
    }
  }
  
  // CodeMirror
  const cmEditor = document.querySelector('.CodeMirror');
  if (!injected && cmEditor && cmEditor.CodeMirror) {
    cmEditor.CodeMirror.setValue(JSON.stringify(data, null, 2));
    cmEditor.CodeMirror.refresh();
    injected = true;
    console.log('[Injector] CodeMirror');
  }
  
  // contenteditable
  const contentEditable = document.querySelector('[contenteditable="true"]');
  if (!injected && contentEditable) {
    contentEditable.focus();
    contentEditable.textContent = JSON.stringify(data, null, 2);
    contentEditable.dispatchEvent(new InputEvent('input', { bubbles: true }));
    contentEditable.dispatchEvent(new Event('change', { bubbles: true }));
    injected = true;
    console.log('[Injector] ContentEditable');
  }
  
  // textarea
  const textarea = document.querySelector('textarea');
  if (!injected && textarea) {
    textarea.value = JSON.stringify(data, null, 2);
    textarea.dispatchEvent(new InputEvent('input', { bubbles: true }));
    textarea.dispatchEvent(new Event('change', { bubbles: true }));
    injected = true;
    console.log('[Injector] Textarea');
  }
  
  if (injected) {
    setTimeout(triggerSave, 500);
    return true;
  }
  
  console.error('[Injector] 未找到编辑器');
  return false;
})();
  `.trim();
}

// ===== 主函数 =====

function main() {
  const args = process.argv.slice(2);
  
  let filePath = null;
  let shouldPrint = false;
  let triggerButton = false;
  
  for (const arg of args) {
    if (arg.startsWith('--file=')) {
      filePath = arg.split('=')[1];
    } else if (arg === '--print') {
      shouldPrint = true;
    } else if (arg === '--trigger') {
      triggerButton = true;
    }
  }
  
  // 准备 payload
  let payload;
  if (filePath) {
    const content = fs.readFileSync(filePath, 'utf-8');
    payload = JSON.parse(content);
  } else {
    // 默认示例 payload
    payload = {
      "type": "ENTRY_CARD",
      "title": "示例卡片",
      "description": "这是示例配置"
    };
  }
  
  // 生成注入脚本
  const injector = triggerButton 
    ? generateWithButtonTrigger(payload)
    : generateInjector(payload);
  
  if (shouldPrint) {
    console.log(injector);
  } else {
    console.log('使用 --print 参数输出脚本');
    console.log('使用 --trigger 参数同时触发保存按钮');
  }
}

main();
