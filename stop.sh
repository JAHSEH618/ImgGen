#!/bin/bash
# 停止前后端服务

cd "$(dirname "$0")"

echo "🛑 停止 Img Gen 服务..."
echo "================================"

# 停止前端服务
if [ -f .frontend.pid ]; then
    FRONTEND_PID=$(cat .frontend.pid)
    if kill -0 "$FRONTEND_PID" 2>/dev/null; then
        echo "🎨 停止前端服务 (PID: $FRONTEND_PID)..."
        kill "$FRONTEND_PID" 2>/dev/null
    fi
    rm -f .frontend.pid
fi

# 停止文件存储服务
if [ -f .file_service.pid ]; then
    FILE_PID=$(cat .file_service.pid)
    if kill -0 "$FILE_PID" 2>/dev/null; then
        echo "📁 停止文件存储服务 (PID: $FILE_PID)..."
        kill "$FILE_PID" 2>/dev/null
    fi
    rm -f .file_service.pid
fi

# 停止AI服务
if [ -f .ai_service.pid ]; then
    AI_PID=$(cat .ai_service.pid)
    if kill -0 "$AI_PID" 2>/dev/null; then
        echo "🤖 停止AI图像生成服务 (PID: $AI_PID)..."
        kill "$AI_PID" 2>/dev/null
    fi
    rm -f .ai_service.pid
fi

# 查找并停止残留进程
echo "🔍 检查残留进程..."
pkill -f "tools/file_storage/routes.py" 2>/dev/null
pkill -f "tools/img_gen/routes.py" 2>/dev/null
pkill -f "vite" 2>/dev/null

echo "================================"
echo "✅ 所有服务已停止"
