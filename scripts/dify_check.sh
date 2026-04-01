#!/bin/bash
#
# dify_check.sh - Dify Workflow 健康检查脚本
#
# 功能：
# 1. 检查 app id 是否存在
# 2. 验证 draft 版本
# 3. 检查中文编码（抽样）
# 4. 输出 workflow 结构摘要
#
# 用法：
#   ./dify_check.sh --app-id=xxx
#   DIFY_API_KEY=xxx ./dify_check.sh --app-id=xxx

set -e

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 配置
DIFY_API_BASE="${DIFY_API_BASE:-https://your-dify.com/console/api}"
DIFY_API_KEY="${DIFY_API_KEY:-}"

# 解析参数
APP_ID=""
while [[ $# -gt 0 ]]; do
  case $1 in
    --app-id=*)
      APP_ID="${1#*=}"
      shift
      ;;
    *)
      echo "未知参数: $1"
      exit 1
      ;;
  esac
done

if [[ -z "$APP_ID" ]]; then
  echo -e "${RED}错误: 必须提供 --app-id${NC}"
  echo "用法: ./dify_check.sh --app-id=xxx"
  exit 1
fi

if [[ -z "$DIFY_API_KEY" ]]; then
  echo -e "${RED}错误: 必须设置 DIFY_API_KEY 环境变量${NC}"
  exit 1
fi

echo "========================================"
echo "Dify Workflow 健康检查"
echo "========================================"
echo ""

# ===== 检查 1: App 存在性 =====
echo "[1/5] 检查 App 存在性..."
APP_RESPONSE=$(curl -s -w "\n%{http_code}" \
  "${DIFY_API_BASE}/apps/${APP_ID}" \
  -H "Authorization: Bearer ${DIFY_API_KEY}")

HTTP_CODE=$(echo "$APP_RESPONSE" | tail -n1)
APP_DATA=$(echo "$APP_RESPONSE" | sed '$d')

if [[ "$HTTP_CODE" != "200" ]]; then
  echo -e "${RED}  ❌ App 检查失败: HTTP $HTTP_CODE${NC}"
  echo "  响应: $APP_DATA"
  exit 1
fi

APP_NAME=$(echo "$APP_DATA" | grep -o '"name":"[^"]*"' | head -1 | cut -d'"' -f4)
echo -e "${GREEN}  ✅ App 存在: $APP_NAME${NC}"

# ===== 检查 2: Workflow Draft =====
echo ""
echo "[2/5] 检查 Workflow Draft..."
DRAFT_RESPONSE=$(curl -s -w "\n%{http_code}" \
  "${DIFY_API_BASE}/apps/${APP_ID}/workflows/draft" \
  -H "Authorization: Bearer ${DIFY_API_KEY}")

HTTP_CODE=$(echo "$DRAFT_RESPONSE" | tail -n1)
DRAFT_DATA=$(echo "$DRAFT_RESPONSE" | sed '$d')

if [[ "$HTTP_CODE" != "200" ]]; then
  echo -e "${YELLOW}  ⚠️ Draft 获取失败: HTTP $HTTP_CODE${NC}"
else
  DRAFT_VERSION=$(echo "$DRAFT_DATA" | grep -o '"version":"[^"]*"' | head -1 | cut -d'"' -f4)
  echo -e "${GREEN}  ✅ Draft 版本: $DRAFT_VERSION${NC}"
fi

# ===== 检查 3: 已发布版本 =====
echo ""
echo "[3/5] 检查已发布版本..."
PUBLISHED_RESPONSE=$(curl -s -w "\n%{http_code}" \
  "${DIFY_API_BASE}/apps/${APP_ID}/workflows" \
  -H "Authorization: Bearer ${DIFY_API_KEY}")

HTTP_CODE=$(echo "$PUBLISHED_RESPONSE" | tail -n1)
PUBLISHED_DATA=$(echo "$PUBLISHED_RESPONSE" | sed '$d')

if [[ "$HTTP_CODE" != "200" ]]; then
  echo -e "${YELLOW}  ⚠️ 已发布版本获取失败: HTTP $HTTP_CODE${NC}"
else
  PUBLISHED_VERSION=$(echo "$PUBLISHED_DATA" | grep -o '"version":"[^"]*"' | head -1 | cut -d'"' -f4)
  echo -e "${GREEN}  ✅ 已发布版本: $PUBLISHED_VERSION${NC}"
fi

# ===== 检查 4: 中文编码抽样 =====
echo ""
echo "[4/5] 中文编码抽样检查..."
# 检查 app 名称是否包含乱码特征
if echo "$APP_NAME" | grep -q '\\u[0-9a-fA-F]\{4\}'; then
  echo -e "${RED}  ❌ 检测到 Unicode 转义序列，可能存在编码问题${NC}"
elif echo "$APP_NAME" | grep -q '[]'; then
  echo -e "${RED}  ❌ 检测到替换字符()，存在编码损坏${NC}"
else
  echo -e "${GREEN}  ✅ App 名称中文正常${NC}"
fi

# ===== 检查 5: 节点数量摘要 =====
echo ""
echo "[5/5] Workflow 结构摘要..."
if command -v jq &> /dev/null; then
  NODE_COUNT=$(echo "$DRAFT_DATA" | jq '.graph.nodes | length' 2>/dev/null || echo "?")
  EDGE_COUNT=$(echo "$DRAFT_DATA" | jq '.graph.edges | length' 2>/dev/null || echo "?")
  echo "  节点数量: $NODE_COUNT"
  echo "  连接数量: $EDGE_COUNT"
  
  # 列出节点类型
  echo ""
  echo "  节点类型分布:"
  echo "$DRAFT_DATA" | jq -r '.graph.nodes[] | "    - " + .type + ": " + (.title // .id)' 2>/dev/null | head -20
else
  echo -e "${YELLOW}  ⚠️ 未安装 jq，跳过结构分析${NC}"
fi

echo ""
echo "========================================"
echo -e "${GREEN}检查完成${NC}"
echo "========================================"
