#!/bin/bash

echo "🔧 本地验证nginx配置"
echo "==================="

cd /Users/okonma/PycharmProjects/demoProj/img/backend

echo "1. 检查nginx配置文件语法..."
docker run --rm -v "$(pwd)/nginx-proxy-fixed.conf:/etc/nginx/nginx.conf:ro" nginx:alpine nginx -t

if [ $? -ne 0 ]; then
    echo "❌ nginx配置语法错误!"
    exit 1
else
    echo "✅ nginx配置语法正确"
fi

echo ""
echo "2. 启动本地测试环境..."

# 创建测试用的docker-compose
cat > docker-compose-nginx-test.yml << 'EOF'
version: '3.8'

services:
  # 模拟后端文件服务
  mock-file-service:
    image: httpd:alpine
    container_name: mock-file-service
    ports:
      - "10086:80"
    volumes:
      - ./test-responses:/usr/local/apache2/htdocs
    networks:
      - test-network

  # 模拟后端AI服务  
  mock-ai-service:
    image: httpd:alpine
    container_name: mock-ai-service
    ports:
      - "8088:80"
    volumes:
      - ./test-responses:/usr/local/apache2/htdocs
    networks:
      - test-network

  # 模拟前端服务
  mock-frontend:
    image: httpd:alpine
    container_name: mock-frontend
    ports:
      - "3001:80"
    volumes:
      - ./test-responses:/usr/local/apache2/htdocs
    networks:
      - test-network

  # 测试nginx配置
  nginx-test:
    image: nginx:alpine
    container_name: nginx-test
    ports:
      - "8080:80"
    volumes:
      - ./nginx-proxy-test.conf:/etc/nginx/nginx.conf:ro
    networks:
      - test-network
    depends_on:
      - mock-file-service
      - mock-ai-service
      - mock-frontend

networks:
  test-network:
    driver: bridge
EOF

echo ""
echo "3. 创建测试nginx配置..."
cat > nginx-proxy-test.conf << 'EOF'
events {
    worker_connections 1024;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    # 测试环境的upstream配置
    upstream backend_file_service {
        server mock-file-service:80;
    }
    
    upstream backend_ai_service {
        server mock-ai-service:80;
    }
    
    upstream frontend_service {
        server mock-frontend:80;
    }

    server {
        listen 80;
        server_name _;
        
        client_max_body_size 50M;
        
        # 通用CORS设置
        add_header Access-Control-Allow-Origin * always;
        add_header Access-Control-Allow-Methods 'GET, POST, OPTIONS, PUT, DELETE' always;
        add_header Access-Control-Allow-Headers 'Accept,Authorization,Cache-Control,Content-Type,DNT,If-Modified-Since,Keep-Alive,Origin,User-Agent,X-Requested-With' always;
        
        # 处理OPTIONS预检请求
        if ($request_method = 'OPTIONS') {
            add_header Access-Control-Allow-Origin * always;
            add_header Access-Control-Allow-Methods 'GET, POST, OPTIONS, PUT, DELETE' always;
            add_header Access-Control-Allow-Headers 'Accept,Authorization,Cache-Control,Content-Type,DNT,If-Modified-Since,Keep-Alive,Origin,User-Agent,X-Requested-With' always;
            add_header Access-Control-Max-Age 1728000;
            add_header Content-Type 'text/plain charset=UTF-8';
            add_header Content-Length 0;
            return 204;
        }

        # 测试端点
        location /nginx-test {
            return 200 '{"status":"nginx-working","timestamp":"$time_iso8601"}';
            add_header Content-Type application/json;
        }

        # API路由 - 文件服务
        location /api/file/ {
            # 记录原始请求
            access_log /var/log/nginx/api_file.log;
            
            # 移除 /api/file 前缀
            rewrite ^/api/file/(.*) /$1 break;
            
            proxy_pass http://backend_file_service/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            
            # 超时设置
            proxy_connect_timeout 10s;
            proxy_send_timeout 10s;
            proxy_read_timeout 10s;
        }

        # API路由 - AI服务
        location /api/ai/ {
            # 记录原始请求
            access_log /var/log/nginx/api_ai.log;
            
            # 移除 /api/ai 前缀
            rewrite ^/api/ai/(.*) /$1 break;
            
            proxy_pass http://backend_ai_service/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            
            # 超时设置
            proxy_connect_timeout 10s;
            proxy_send_timeout 10s;
            proxy_read_timeout 10s;
        }

        # 健康检查
        location /health {
            return 200 "nginx-test-healthy\n";
            add_header Content-Type text/plain;
        }

        # 调试信息
        location /debug {
            return 200 '{
                "status": "ok",
                "server": "nginx-test",
                "upstreams": {
                    "file": "mock-file-service:80",
                    "ai": "mock-ai-service:80",
                    "frontend": "mock-frontend:80"
                }
            }';
            add_header Content-Type application/json;
        }

        # 前端路由
        location / {
            proxy_pass http://frontend_service/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
EOF

echo ""
echo "4. 创建模拟响应文件..."
mkdir -p test-responses

# 模拟文件服务响应
cat > test-responses/list << 'EOF'
{"status": "ok", "service": "file", "files": []}
EOF

cat > test-responses/list_generated << 'EOF'
{"status": "ok", "service": "ai", "generated": []}
EOF

cat > test-responses/index.html << 'EOF'
<!DOCTYPE html>
<html><head><title>Test Frontend</title></head>
<body><h1>Frontend Mock Service Working</h1></body></html>
EOF

echo ""
echo "5. 启动测试环境..."
docker compose -f docker-compose-nginx-test.yml up -d

echo ""
echo "6. 等待服务启动..."
sleep 10

echo ""
echo "7. 测试nginx配置..."

echo ""
echo "🧪 基础测试:"
echo "  - Nginx健康检查..."
curl -s http://localhost:8080/health && echo " ✅" || echo " ❌"

echo "  - Nginx测试端点..."  
curl -s http://localhost:8080/nginx-test && echo " ✅" || echo " ❌"

echo "  - Debug信息..."
curl -s http://localhost:8080/debug | jq . 2>/dev/null && echo " ✅" || echo " ❌"

echo ""
echo "🧪 API路由测试:"
echo "  - 文件服务路由 /api/file/list..."
RESPONSE=$(curl -s http://localhost:8080/api/file/list)
if [[ $RESPONSE == *"file"* ]]; then
    echo " ✅ 路由正常: $RESPONSE"
else
    echo " ❌ 路由失败: $RESPONSE"
fi

echo "  - AI服务路由 /api/ai/list_generated..."
RESPONSE=$(curl -s http://localhost:8080/api/ai/list_generated)
if [[ $RESPONSE == *"ai"* ]]; then
    echo " ✅ 路由正常: $RESPONSE"
else
    echo " ❌ 路由失败: $RESPONSE"
fi

echo ""
echo "🧪 前端路由测试:"
echo "  - 前端首页..."
RESPONSE=$(curl -s http://localhost:8080/)
if [[ $RESPONSE == *"Frontend"* ]]; then
    echo " ✅ 前端路由正常"
else
    echo " ❌ 前端路由失败"
fi

echo ""
echo "8. 检查nginx日志..."
echo ""
echo "=== Nginx访问日志 ==="
docker logs nginx-test 2>/dev/null | tail -10

echo ""
echo "9. 清理测试环境..."
read -p "是否清理测试环境? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    docker compose -f docker-compose-nginx-test.yml down
    rm -rf test-responses docker-compose-nginx-test.yml nginx-proxy-test.conf
    echo "✅ 测试环境已清理"
else
    echo "💡 保留测试环境，可以继续调试:"
    echo "   - 测试URL: http://localhost:8080"
    echo "   - 清理命令: docker compose -f docker-compose-nginx-test.yml down"
fi

echo ""
echo "🎯 nginx配置验证完成!"