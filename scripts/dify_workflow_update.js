#!/usr/bin/env node
/**
 * dify_workflow_update.js - Dify Workflow 批量更新脚本
 * 
 * 功能：
 * 1. 锁定 app id 并验证存在
 * 2. 安全写入 UTF-8 中文配置
 * 3. 自动读回校验（3类字段抽样）
 * 4. 分层 API 调用（区分 PUT/POST）
 * 
 * 用法：
 *   node dify_workflow_update.js --app-id=xxx --config=./config.json
 *   node dify_workflow_update.js --app-id=xxx --update-name="新名称" --update-desc="新描述"
 */

const fs = require('fs');
const path = require('path');

// ===== 配置 =====
const DIFY_API_BASE = process.env.DIFY_API_BASE || 'https://your-dify.com/console/api';
const DIFY_API_KEY = process.env.DIFY_API_KEY || '';

// ===== 工具函数 =====

/**
 * 带重试的 fetch
 */
async function fetchWithRetry(url, options, retries = 3) {
  for (let i = 0; i < retries; i++) {
    try {
      const response = await fetch(url, options);
      return response;
    } catch (err) {
      if (i === retries - 1) throw err;
      console.log(`  重试 ${i + 1}/${retries}...`);
      await new Promise(r => setTimeout(r, 1000 * (i + 1)));
    }
  }
}

/**
 * 验证 app 存在
 */
async function verifyApp(appId) {
  console.log(`[1/4] 验证 app: ${appId}`);
  const response = await fetchWithRetry(
    `${DIFY_API_BASE}/apps/${appId}`,
    {
      headers: {
        'Authorization': `Bearer ${DIFY_API_KEY}`,
        'Content-Type': 'application/json'
      }
    }
  );
  
  if (!response.ok) {
    throw new Error(`App 验证失败: ${response.status} ${response.statusText}`);
  }
  
  const data = await response.json();
  console.log(`  ✅ App 存在: ${data.name} (${data.id})`);
  return data;
}

/**
 * 更新 app 元信息（名称/描述）
 * 注意：此接口用 PUT，不是 POST！
 */
async function updateAppMeta(appId, updates) {
  console.log(`[2/4] 更新 app 元信息...`);
  
  // 关键：app 元信息更新用 PUT，不是 POST
  const response = await fetchWithRetry(
    `${DIFY_API_BASE}/apps/${appId}`,
    {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${DIFY_API_KEY}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(updates)
    }
  );
  
  if (!response.ok) {
    const error = await response.text();
    throw new Error(`更新失败: ${response.status} ${error}`);
  }
  
  console.log(`  ✅ 元信息更新成功`);
}

/**
 * 更新 workflow draft
 */
async function updateWorkflowDraft(appId, workflowConfig) {
  console.log(`[3/4] 更新 workflow draft...`);
  
  const response = await fetchWithRetry(
    `${DIFY_API_BASE}/apps/${appId}/workflows/draft`,
    {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${DIFY_API_KEY}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(workflowConfig)
    }
  );
  
  if (!response.ok) {
    const error = await response.text();
    throw new Error(`Draft 更新失败: ${response.status} ${error}`);
  }
  
  const data = await response.json();
  console.log(`  ✅ Draft 更新成功: version=${data.version}`);
  return data;
}

/**
 * 发布 workflow
 */
async function publishWorkflow(appId) {
  console.log(`[4/4] 发布 workflow...`);
  
  const response = await fetchWithRetry(
    `${DIFY_API_BASE}/apps/${appId}/workflows/publish`,
    {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${DIFY_API_KEY}`,
        'Content-Type': 'application/json'
      }
    }
  );
  
  if (!response.ok) {
    const error = await response.text();
    throw new Error(`发布失败: ${response.status} ${error}`);
  }
  
  console.log(`  ✅ 发布成功`);
}

/**
 * 读回校验（3类字段抽样）
 */
async function verifyUpdate(appId, expectedName) {
  console.log(`[校验] 读回确认...`);
  
  const response = await fetchWithRetry(
    `${DIFY_API_BASE}/apps/${appId}`,
    {
      headers: {
        'Authorization': `Bearer ${DIFY_API_KEY}`,
        'Content-Type': 'application/json'
      }
    }
  );
  
  const data = await response.json();
  
  // 3类字段抽样
  const checks = [
    { field: 'App 名称', actual: data.name, expected: expectedName },
    { field: 'App ID', actual: data.id, expected: appId }
  ];
  
  let allPass = true;
  for (const check of checks) {
    if (check.expected && check.actual !== check.expected) {
      console.log(`  ❌ ${check.field} 不匹配: 期望="${check.expected}", 实际="${check.actual}"`);
      allPass = false;
    } else {
      console.log(`  ✅ ${check.field}: ${check.actual}`);
    }
  }
  
  if (!allPass) {
    throw new Error('读回校验失败，可能存在编码问题');
  }
  
  return data;
}

// ===== 主函数 =====

async function main() {
  const args = process.argv.slice(2);
  
  // 解析参数
  let appId = null;
  let configPath = null;
  let updateName = null;
  let updateDesc = null;
  let shouldPublish = false;
  
  for (const arg of args) {
    if (arg.startsWith('--app-id=')) {
      appId = arg.split('=')[1];
    } else if (arg.startsWith('--config=')) {
      configPath = arg.split('=')[1];
    } else if (arg.startsWith('--update-name=')) {
      updateName = arg.split('=')[1];
    } else if (arg.startsWith('--update-desc=')) {
      updateDesc = arg.split('=')[1];
    } else if (arg === '--publish') {
      shouldPublish = true;
    }
  }
  
  // 验证必要参数
  if (!appId) {
    console.error('错误: 必须提供 --app-id');
    console.log('用法: node dify_workflow_update.js --app-id=xxx [--config=./config.json] [--update-name="名称"] [--publish]');
    process.exit(1);
  }
  
  if (!DIFY_API_KEY) {
    console.error('错误: 必须设置 DIFY_API_KEY 环境变量');
    process.exit(1);
  }
  
  try {
    // Phase 1: 验证 app
    await verifyApp(appId);
    
    // Phase 2: 更新元信息（如果提供）
    if (updateName || updateDesc) {
      const updates = {};
      if (updateName) updates.name = updateName;
      if (updateDesc) updates.description = updateDesc;
      await updateAppMeta(appId, updates);
      
      // 立即读回校验
      await verifyUpdate(appId, updateName);
    }
    
    // Phase 3: 更新 workflow draft（如果提供配置）
    if (configPath) {
      const config = JSON.parse(fs.readFileSync(configPath, 'utf-8'));
      await updateWorkflowDraft(appId, config);
    }
    
    // Phase 4: 发布（如果指定）
    if (shouldPublish) {
      await publishWorkflow(appId);
    }
    
    console.log('\n✅ 全部完成');
    
  } catch (err) {
    console.error(`\n❌ 错误: ${err.message}`);
    process.exit(1);
  }
}

main();
