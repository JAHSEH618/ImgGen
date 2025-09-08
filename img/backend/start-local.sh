#!/bin/bash

# Img Gen 本地开发一键启动脚本
echo "🚀 Img Gen 本地开发环境启动"
echo "=========================="

# 获取脚本目录
SCRIPT_DIR=$(dirname $(realpath $0))
FRONTEND_DIR="$SCRIPT_DIR/../frontend"

echo "后端目录: $SCRIPT_DIR"
echo "前端目录: $FRONTEND_DIR"
echo ""

# 检查前端目录
if [[ ! -d "$FRONTEND_DIR" ]]; then
    echo "❌ 前端目录不存在: $FRONTEND_DIR"
    exit 1
fi

# 1. 检查并配置API密钥
echo "🔑 检查API密钥配置..."
if [[ ! -f ".env" || ! -s ".env" ]]; then
    echo "未找到API密钥配置，启动配置向导..."
    ./setup-api-key.sh
    if [[ $? -ne 0 ]]; then
        echo "❌ API密钥配置失败"
        exit 1
    fi
else
    echo "✅ 发现现有API密钥配置"
fi

# 2. 准备后端环境
echo ""
echo "🐍 准备后端Python环境..."
if [[ ! -d "venv" ]]; then
    echo "创建Python虚拟环境..."
    python3 -m venv venv
    if [[ $? -ne 0 ]]; then
        echo "❌ Python虚拟环境创建失败"
        exit 1
    fi
fi

echo "激活虚拟环境并安装依赖..."
source venv/bin/activate
pip install -r requirements-flexible.txt > /dev/null 2>&1
if [[ $? -ne 0 ]]; then
    echo "⚠️  使用核心依赖重试..."
    pip install -r requirements-core.txt
fi

echo "✅ 后端环境准备完成"

# 3. 准备前端环境
echo ""
echo "📦 准备前端Node.js环境..."
cd "$FRONTEND_DIR"

if [[ ! -d "node_modules" ]]; then
    echo "安装前端依赖..."
    npm install > /dev/null 2>&1
    if [[ $? -ne 0 ]]; then
        echo "❌ 前端依赖安装失败"
        exit 1
    fi
fi

echo "✅ 前端环境准备完成"

# 4. 启动后端服务
echo ""
echo "🔧 启动后端服务..."
cd "$SCRIPT_DIR"
source venv/bin/activate

# 加载环境变量
export $(grep -v '^#' .env | xargs)

# 启动文件服务
echo "启动文件存储服务 (端口 10086)..."
python file.py > logs/file-service.log 2>&1 &
FILE_PID=$!

sleep 2

# 启动AI服务
echo "启动AI生成服务 (端口 8088)..."
python gemini_api.py > logs/ai-service.log 2>&1 &
AI_PID=$!

sleep 3

# 检查后端服务状态
echo "检查后端服务状态..."
if curl -f -s -m 5 http://localhost:10086/list > /dev/null; then
    echo "✅ 文件存储服务正常运行"
else
    echo "❌ 文件存储服务启动失败"
    kill $FILE_PID $AI_PID 2>/dev/null
    exit 1
fi

if curl -f -s -m 5 http://localhost:8088/list_generated > /dev/null; then
    echo "✅ AI生成服务正常运行"
else
    echo "❌ AI生成服务启动失败"
    kill $FILE_PID $AI_PID 2>/dev/null
    exit 1
fi

# 5. 启动前端服务
echo ""
echo "🎨 启动前端开发服务器..."
cd "$FRONTEND_DIR"
npm run dev > ../backend/logs/frontend-dev.log 2>&1 &
FRONTEND_PID=$!

sleep 5

# 检查前端服务状态
if curl -f -s -m 5 http://localhost:5173 > /dev/null; then
    echo "✅ 前端开发服务器正常运行"
else
    echo "❌ 前端开发服务器启动失败"
    kill $FILE_PID $AI_PID $FRONTEND_PID 2>/dev/null
    exit 1
fi

# 创建停止脚本
cat > "$SCRIPT_DIR/stop-local.sh" << EOF
#!/bin/bash
echo "🛑 停止Img Gen本地开发服务..."
kill $FILE_PID $AI_PID $FRONTEND_PID 2>/dev/null
echo "✅ 所有服务已停止"
rm -f "$SCRIPT_DIR/stop-local.sh"
EOF
chmod +x "$SCRIPT_DIR/stop-local.sh"

# 显示成功信息
echo ""
echo "🎉 Img Gen 本地开发环境启动成功！"
echo "================================="
echo ""
echo "📡 服务访问地址:"
echo "  • 前端开发界面:    http://localhost:5173"
echo "  • 后端文件服务:    http://localhost:10086"
echo "  • 后端AI生成服务:  http://localhost:8088"
echo ""
echo "📋 开发说明:"
echo "  • 前端支持热重载，修改代码自动刷新"
echo "  • 后端修改需要重启服务"
echo "  • API测试: curl http://localhost:10086/list"
echo ""
echo "📊 监控和日志:"
echo "  • 查看文件服务日志: tail -f logs/file-service.log"
echo "  • 查看AI服务日志:   tail -f logs/ai-service.log"
echo "  • 查看前端日志:     tail -f logs/frontend-dev.log"
echo ""
echo "🛑 停止服务:"
echo "  ./stop-local.sh"
echo "  或按 Ctrl+C 然后运行停止脚本"
echo ""

# 设置信号处理
cleanup() {
    echo ""
    echo "🛑 正在停止所有服务..."
    kill $FILE_PID $AI_PID $FRONTEND_PID 2>/dev/null
    echo "✅ 所有服务已停止"
    rm -f "$SCRIPT_DIR/stop-local.sh"
    exit 0
}

trap cleanup INT TERM

# 保持脚本运行
echo "💡 提示: 按 Ctrl+C 停止所有服务"
echo ""
wait