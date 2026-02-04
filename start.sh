#!/bin/bash
# 启动前后端服务

cd "$(dirname "$0")"

echo "🚀 启动 Img Gen 服务..."
echo "================================"

# 创建日志目录
mkdir -p backend/logs

# Activate virtual environment
if [ -d ".venv" ]; then
    source .venv/bin/activate
    echo "✅ Activated virtual environment (.venv)"
elif [ -d "venv" ]; then
    source venv/bin/activate
    echo "✅ Activated virtual environment (venv)"
fi

# 加载环境变量
if [ -f backend/.env ]; then
    set -a
    source backend/.env
    set +a
    echo "✅ 已加载环境变量 (backend/.env)"
fi

# 启动文件存储服务 (端口 10086)
echo "📁 启动文件存储服务 (端口 10086)..."
cd backend
python -m tools.file_storage.routes > logs/file_service.log 2>&1 &
FILE_PID=$!
echo "   PID: $FILE_PID"
cd ..

sleep 1

# 启动AI图像生成服务 (端口 8088)
echo "🤖 启动AI图像生成服务 (端口 8088)..."
cd backend
python -m tools.img_gen.routes > logs/ai_service.log 2>&1 &
AI_PID=$!
echo "   PID: $AI_PID"
cd ..

sleep 1

# 启动前端服务 (端口 5173)
echo "🎨 启动前端服务 (端口 5173)..."
cd frontend
npm run dev > ../backend/logs/frontend.log 2>&1 &
FRONTEND_PID=$!
echo "   PID: $FRONTEND_PID"
cd ..

# 保存PID到文件
echo "$FILE_PID" > .file_service.pid
echo "$AI_PID" > .ai_service.pid
echo "$FRONTEND_PID" > .frontend.pid

sleep 2

echo "================================"
echo "✅ 所有服务启动完成!"
echo ""
echo "📡 可用服务:"
echo "   前端界面: http://localhost:5173"
echo "   文件存储: http://localhost:10086"
echo "   AI生成:   http://localhost:8088"
echo ""
echo "💡 使用 ./stop.sh 停止所有服务"
