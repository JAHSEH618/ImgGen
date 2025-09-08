#!/bin/bash

# 修复API 404错误的快速重建脚本
echo "🔧 修复API 404错误（端口映射问题）..."
echo "======================================"

# 获取脚本目录
SCRIPT_DIR=$(dirname $(realpath $0))
cd "$SCRIPT_DIR"

echo "1. 检查配置文件..."
if [[ ! -f ".env" ]]; then
    echo "❌ 未找到.env文件，请先配置API密钥:"
    echo "echo 'GEMINI_API_KEY=your_api_key' > .env"
    exit 1
fi

echo "✅ 发现配置文件"

echo ""
echo "2. 停止现有服务..."
docker compose -f docker-compose-fullstack.yml down

echo ""
echo "3. 重新构建所有服务（统一端口架构）..."
docker compose -f docker-compose-fullstack.yml --env-file .env build --no-cache

echo ""
echo "4. 启动服务..."
docker compose -f docker-compose-fullstack.yml --env-file .env up -d

echo ""
echo "5. 等待服务启动..."
sleep 15

echo ""
echo "6. 检查服务状态..."
docker compose -f docker-compose-fullstack.yml ps

echo ""
echo "7. 测试所有端点..."
echo ""

# 测试两个端口
for port in 80 3000; do
    echo "🧪 测试端口 $port..."
    
    # 测试nginx代理
    echo "  - Nginx健康检查..."
    curl -s http://localhost:$port/health && echo "  ✅ 健康检查通过" || echo "  ❌ 健康检查失败"
    
    # 测试前端
    echo "  - 前端访问..."
    curl -s -o /dev/null -w "%{http_code}" http://localhost:$port/ | grep -q "200" && echo "  ✅ 前端正常" || echo "  ❌ 前端异常"
    
    # 测试API路由
    echo "  - API调试..."
    curl -s http://localhost:$port/api/debug > /dev/null && echo "  ✅ API路由正常" || echo "  ❌ API路由失败"
    
    # 测试文件服务
    echo "  - 文件服务API..."
    curl -s http://localhost:$port/api/file/list > /dev/null && echo "  ✅ 文件服务正常" || echo "  ❌ 文件服务失败"
    
    # 测试AI服务
    echo "  - AI服务API..."
    curl -s http://localhost:$port/api/ai/list_generated > /dev/null && echo "  ✅ AI服务正常" || echo "  ❌ AI服务失败"
    
    echo ""
done

echo "🎉 修复完成！"
echo ""
echo "📡 现在可以通过以下地址访问:"
echo "  • http://43.153.26.219 (推荐)"
echo "  • http://43.153.26.219:3000 (兼容性)"
echo "  • http://localhost"
echo "  • http://localhost:3000"
echo ""
echo "🔍 如果仍有问题，查看日志:"
echo "  docker compose -f docker-compose-fullstack.yml logs -f"
echo ""
echo "💡 现在所有服务都通过nginx代理，API调用会自动路由到正确的后端服务"