#!/bin/bash
# 重启前后端服务

cd "$(dirname "$0")"

echo "🔄 重启 Img Gen 服务..."
echo ""

# 先停止
./stop.sh

sleep 1

# 再启动
./start.sh
