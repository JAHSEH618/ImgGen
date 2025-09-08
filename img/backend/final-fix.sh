#!/bin/bash

echo "🔥 最终修复 - 502错误"
echo "===================="

cd /Users/okonma/PycharmProjects/demoProj/img/backend

echo "1. 完全停止所有服务..."
docker stop $(docker ps -aq) 2>/dev/null || true
docker rm $(docker ps -aq) 2>/dev/null || true

echo ""
echo "2. 创建最简单可工作的配置..."
cat > docker-compose-minimal.yml << 'EOF'
version: '3.8'

services:
  # 只启动后端服务
  img-gen-backend:
    build: 
      context: .
      dockerfile: Dockerfile
    container_name: img-gen-backend
    ports:
      - "8088:8088"
      - "10086:10086" 
    environment:
      - FLASK_ENV=production
      - PYTHONUNBUFFERED=1
      - GEMINI_API_KEY=${GEMINI_API_KEY}
    volumes:
      - ./upload:/app/upload
      - ./generated:/app/generated
    restart: unless-stopped

  # 只启动前端服务
  img-gen-frontend:
    build: 
      context: ../frontend
      dockerfile: Dockerfile
    container_name: img-gen-frontend
    ports:
      - "3000:80"
    restart: unless-stopped
EOF

echo ""
echo "3. 启动最简配置（跳过nginx）..."
docker compose -f docker-compose-minimal.yml --env-file .env up -d --build

echo ""
echo "4. 等待服务启动..."
sleep 30

echo ""
echo "5. 检查容器状态..."
docker compose -f docker-compose-minimal.yml ps

echo ""
echo "6. 检查服务日志..."
echo "=== 后端日志 ==="
docker logs img-gen-backend | tail -10

echo ""
echo "=== 前端日志 ==="
docker logs img-gen-frontend | tail -10

echo ""
echo "7. 测试服务可用性..."

echo "测试后端文件服务:"
curl -s http://localhost:10086/list && echo "✅ 文件服务可用" || echo "❌ 文件服务不可用"

echo ""
echo "测试后端AI服务:"
curl -s http://localhost:8088/list_generated && echo "✅ AI服务可用" || echo "❌ AI服务不可用"

echo ""
echo "测试前端服务:"
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/)
if [ "$HTTP_CODE" = "200" ]; then
    echo "✅ 前端服务可用 (HTTP $HTTP_CODE)"
else
    echo "❌ 前端服务不可用 (HTTP $HTTP_CODE)"
fi

echo ""
echo "8. 修改前端API配置为直接访问..."
cat > ../frontend/src/config/api-direct.js << 'JSEOF'
// 直接访问后端API配置（跳过nginx）
const API_CONFIG = {
  baseURL: window.location.protocol + '//' + window.location.hostname,
  fileService: window.location.protocol + '//' + window.location.hostname + ':10086',
  aiService: window.location.protocol + '//' + window.location.hostname + ':8088'
}

export const API_URLS = {
  // 文件服务
  fileUpload: `${API_CONFIG.fileService}/upload`,
  fileList: `${API_CONFIG.fileService}/list`,
  fileImage: (filename) => `${API_CONFIG.fileService}/image/${filename}`,
  fileDownload: (filename) => `${API_CONFIG.fileService}/download/${filename}`,
  
  // AI服务  
  aiGenerate: `${API_CONFIG.aiService}/generate`,
  aiImage: (filename) => `${API_CONFIG.aiService}/image/${filename}`,
  aiDownload: (filename) => `${API_CONFIG.aiService}/download/${filename}`,
  aiList: `${API_CONFIG.aiService}/list_generated`
}

export default API_CONFIG
JSEOF

echo ""
echo "9. 重新构建前端（使用直接API配置）..."
# 备份原配置
cp ../frontend/src/config/api.js ../frontend/src/config/api-backup.js
# 使用直接配置
cp ../frontend/src/config/api-direct.js ../frontend/src/config/api.js

# 重新构建前端
docker compose -f docker-compose-minimal.yml build img-gen-frontend
docker compose -f docker-compose-minimal.yml up -d img-gen-frontend

echo ""
echo "10. 最终测试..."
sleep 10

HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/)
echo "前端最终状态: HTTP $HTTP_CODE"

echo ""
echo "🎯 最简修复完成!"
echo ""
echo "📡 现在可以通过以下地址访问:"
echo "  • 前端界面: http://43.153.26.219:3000"
echo "  • 文件API: http://43.153.26.219:10086"
echo "  • AI API: http://43.153.26.219:8088"
echo ""
echo "💡 这个配置跳过了nginx代理，直接访问后端服务"
echo "   如果这样工作正常，说明问题出在nginx配置上"