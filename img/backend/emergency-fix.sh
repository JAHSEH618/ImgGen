#!/bin/bash

echo "🚨 紧急修复 - 容器启动问题"
echo "=========================="

cd /Users/okonma/PycharmProjects/demoProj/img/backend

echo "1. 强制停止所有容器..."
docker compose -f docker-compose-fullstack.yml down --volumes --remove-orphans

echo ""
echo "2. 清理Docker缓存..."
docker system prune -f

echo ""
echo "3. 创建简化的docker-compose配置..."
cat > docker-compose-emergency.yml << 'EOF'
version: '3.8'

services:
  # Backend Services  
  img-gen-backend:
    build: 
      context: .
      dockerfile: Dockerfile
    container_name: img-gen-backend
    ports:
      - "8088:8088"  # 直接暴露端口以便调试
      - "10086:10086" 
    environment:
      - FLASK_ENV=production
      - PYTHONUNBUFFERED=1
      - GEMINI_API_KEY=${GEMINI_API_KEY}
    volumes:
      - ./upload:/app/upload
      - ./generated:/app/generated
    restart: unless-stopped
    networks:
      - img-gen-network

  # Frontend Service
  img-gen-frontend:
    build: 
      context: ../frontend
      dockerfile: Dockerfile
    container_name: img-gen-frontend
    ports:
      - "3000:80"  # 恢复直接端口映射
    restart: unless-stopped
    networks:
      - img-gen-network

  # Nginx Reverse Proxy
  nginx:
    image: nginx:alpine
    container_name: img-gen-proxy
    ports:
      - "80:80"
    volumes:
      - ./nginx-proxy-fixed.conf:/etc/nginx/nginx.conf:ro
    restart: unless-stopped
    networks:
      - img-gen-network

networks:
  img-gen-network:
    driver: bridge
EOF

echo ""
echo "4. 使用紧急配置启动服务..."
docker compose -f docker-compose-emergency.yml --env-file .env up -d --build

echo ""
echo "5. 等待服务启动..."
sleep 20

echo ""
echo "6. 检查容器状态..."
docker compose -f docker-compose-emergency.yml ps

echo ""
echo "7. 测试直接访问..."
echo "测试后端文件服务:"
curl -s http://localhost:10086/list && echo "✅ 文件服务正常" || echo "❌ 文件服务失败"

echo ""
echo "测试后端AI服务:"
curl -s http://localhost:8088/list_generated && echo "✅ AI服务正常" || echo "❌ AI服务失败"

echo ""
echo "测试前端服务:"
curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/ | grep -q "200" && echo "✅ 前端服务正常" || echo "❌ 前端服务失败"

echo ""
echo "测试Nginx代理:"
curl -s http://localhost/health && echo "✅ Nginx正常" || echo "❌ Nginx失败"

echo ""
echo "🎯 紧急修复完成!"
echo "现在可以通过以下方式访问:"
echo "  • 前端: http://43.153.26.219:3000"
echo "  • 后端API: http://43.153.26.219:10086, http://43.153.26.219:8088"
echo "  • Nginx代理: http://43.153.26.219"
echo ""
echo "如果仍有问题，查看日志:"
echo "  docker compose -f docker-compose-emergency.yml logs -f"