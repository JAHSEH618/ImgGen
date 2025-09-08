#!/bin/bash

echo "🔍 诊断Docker服务问题..."
echo "========================"

cd /Users/okonma/PycharmProjects/demoProj/img/backend

echo "1. 检查容器状态..."
docker compose -f docker-compose-fullstack.yml ps

echo ""
echo "2. 检查容器详细信息..."
docker compose -f docker-compose-fullstack.yml ps -a

echo ""
echo "3. 查看nginx日志..."
echo "--- Nginx Logs ---"
docker compose -f docker-compose-fullstack.yml logs nginx | tail -20

echo ""
echo "4. 查看后端服务日志..."
echo "--- Backend Logs ---"
docker compose -f docker-compose-fullstack.yml logs img-gen-backend | tail -20

echo ""
echo "5. 查看前端服务日志..."
echo "--- Frontend Logs ---"
docker compose -f docker-compose-fullstack.yml logs img-gen-frontend | tail -20

echo ""
echo "6. 检查网络连接..."
docker network ls | grep img-gen

echo ""
echo "7. 检查端口占用..."
echo "端口80占用情况:"
lsof -i :80 || netstat -an | grep :80

echo ""
echo "端口3000占用情况:"
lsof -i :3000 || netstat -an | grep :3000

echo ""
echo "8. 测试容器内部连接..."
if docker compose -f docker-compose-fullstack.yml exec nginx /bin/sh -c "wget -q --spider http://img-gen-frontend:80 && echo 'Frontend reachable'" 2>/dev/null; then
    echo "✅ Nginx -> Frontend: 连接正常"
else
    echo "❌ Nginx -> Frontend: 连接失败"
fi

if docker compose -f docker-compose-fullstack.yml exec nginx /bin/sh -c "wget -q --spider http://img-gen-backend:10086/list && echo 'Backend file service reachable'" 2>/dev/null; then
    echo "✅ Nginx -> Backend File: 连接正常"
else
    echo "❌ Nginx -> Backend File: 连接失败"
fi

if docker compose -f docker-compose-fullstack.yml exec nginx /bin/sh -c "wget -q --spider http://img-gen-backend:8088/list_generated && echo 'Backend AI service reachable'" 2>/dev/null; then
    echo "✅ Nginx -> Backend AI: 连接正常"
else
    echo "❌ Nginx -> Backend AI: 连接失败"
fi