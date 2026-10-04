#!/usr/bin/env bash
# 只运行软件回归，不启动台架、不使用原有数据库。
set -euo pipefail
ats_root="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ats_root"
ats_python="${ATS_PYTHON:-$ats_root/.venv-integration/bin/python}"
mkdir -p logs
if [ ! -x "$ats_python" ]; then
  echo "缺少集成 Python 环境，请按 docs/SAT_ECU_INTEGRATION.md 安装"
  exit 1
fi
echo "开始后端与 Agent 软件回归"
"$ats_python" -m pytest tests -q -o addopts='' 2>&1 | tee logs/集成回归.log
echo "开始前端类型检查、单测与构建"
(
  cd frontend
  npm run type-check
  npm run test:unit
  npm run build
) 2>&1 | tee logs/前端构建.log
echo "软件验收完成。原 XAT 的故意失败示例和真实台架不包含在通过判定内。"
