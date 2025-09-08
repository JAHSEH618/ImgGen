#!/bin/bash

echo "简单nginx配置验证..."

# 检查配置文件是否存在
if [ ! -f "nginx-proxy-fixed.conf" ]; then
    echo "❌ nginx配置文件不存在"
    exit 1
fi

echo "✅ nginx配置文件存在"

# 检查语法（简单检查）
echo "检查常见语法问题..."

# 检查括号匹配
OPEN_BRACES=$(grep -o '{' nginx-proxy-fixed.conf | wc -l)
CLOSE_BRACES=$(grep -o '}' nginx-proxy-fixed.conf | wc -l)

if [ $OPEN_BRACES -eq $CLOSE_BRACES ]; then
    echo "✅ 大括号匹配 ($OPEN_BRACES 对)"
else
    echo "❌ 大括号不匹配: 开 $OPEN_BRACES, 关 $CLOSE_BRACES"
fi

# 检查分号
MISSING_SEMICOLONS=$(grep -E '^\s*(listen|server_name|return|add_header|proxy_pass|proxy_set_header|client_max_body_size|sendfile|tcp_nopush|tcp_nodelay|keepalive_timeout|gzip|gzip_vary|gzip_min_length|access_log|error_log)' nginx-proxy-fixed.conf | grep -v ';$' | wc -l)

if [ $MISSING_SEMICOLONS -eq 0 ]; then
    echo "✅ 分号检查通过"
else
    echo "⚠️  可能缺少 $MISSING_SEMICOLONS 个分号"
fi

# 检查关键指令
REQUIRED_DIRECTIVES=("events" "http" "server" "listen")
for directive in "${REQUIRED_DIRECTIVES[@]}"; do
    if grep -q "$directive" nginx-proxy-fixed.conf; then
        echo "✅ 找到必要指令: $directive"
    else
        echo "❌ 缺少必要指令: $directive"
    fi
done

echo ""
echo "配置文件结构:"
echo "Events块: $(grep -c 'events' nginx-proxy-fixed.conf)"
echo "HTTP块: $(grep -c 'http' nginx-proxy-fixed.conf)"  
echo "Server块: $(grep -c 'server' nginx-proxy-fixed.conf)"
echo "Location块: $(grep -c 'location' nginx-proxy-fixed.conf)"
echo "Upstream块: $(grep -c 'upstream' nginx-proxy-fixed.conf)"

echo ""
echo "✅ 基本配置验证完成"
