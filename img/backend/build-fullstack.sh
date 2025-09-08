#!/bin/bash

# Img Gen Full Stack Build Script
# 构建前端和后端的生产版本

set -e

PROJECT_ROOT=$(dirname $(dirname $(realpath $0)))
BACKEND_DIR="$PROJECT_ROOT/backend"
FRONTEND_DIR="$PROJECT_ROOT/frontend"

echo "🚀 Img Gen Full Stack Build Script"
echo "=================================="
echo "项目根目录: $PROJECT_ROOT"
echo "后端目录: $BACKEND_DIR"
echo "前端目录: $FRONTEND_DIR"
echo ""

# 检查目录
if [[ ! -d "$BACKEND_DIR" ]]; then
    echo "❌ 后端目录不存在: $BACKEND_DIR"
    exit 1
fi

if [[ ! -d "$FRONTEND_DIR" ]]; then
    echo "❌ 前端目录不存在: $FRONTEND_DIR"
    exit 1
fi

# 构建前端
echo "🔨 构建前端应用..."
cd "$FRONTEND_DIR"

if [[ ! -f "package.json" ]]; then
    echo "❌ package.json 不存在"
    exit 1
fi

echo "📦 安装前端依赖..."
if [[ ! -f "package-lock.json" ]]; then
    echo "⚠️  package-lock.json不存在，重新生成..."
    npm install
else
    npm ci
fi

echo "🏗️  构建前端 (生产模式)..."
npm run build

if [[ ! -d "dist" ]]; then
    echo "❌ 前端构建失败，dist目录不存在"
    exit 1
fi

echo "✅ 前端构建完成"

# 检查后端依赖
echo "🔍 检查后端依赖..."
cd "$BACKEND_DIR"

if [[ ! -f "requirements-core.txt" ]]; then
    echo "❌ requirements-core.txt 不存在"
    exit 1
fi

echo "✅ 后端检查通过"

# 创建部署包
echo "📦 创建部署包..."
cd "$PROJECT_ROOT"

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
PACKAGE_NAME="img-gen-fullstack-$TIMESTAMP.tar.gz"

tar -czf "$PACKAGE_NAME" \
    --exclude='backend/node_modules' \
    --exclude='backend/__pycache__' \
    --exclude='backend/venv' \
    --exclude='backend/upload' \
    --exclude='backend/generated' \
    --exclude='frontend/node_modules' \
    --exclude='frontend/.vite' \
    backend/ frontend/

echo "✅ 部署包创建完成: $PACKAGE_NAME"

# 显示部署信息
echo ""
echo "📋 部署信息:"
echo "==================="
echo "部署包: $PACKAGE_NAME"
echo "包大小: $(du -h $PACKAGE_NAME | cut -f1)"
echo ""
echo "🚀 Docker 部署命令:"
echo "tar -xzf $PACKAGE_NAME"
echo "cd backend"
echo "docker-compose -f docker-compose-fullstack.yml up -d --build"
echo ""
echo "🌐 访问地址:"
echo "前端界面: http://localhost:3000"
echo "API代理: http://localhost (通过Nginx)"
echo "直接API: http://localhost:8088 (AI服务), http://localhost:10086 (文件服务)"
echo ""