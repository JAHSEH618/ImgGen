#!/bin/bash

echo "🔧 nginx配置问题分析和修复"
echo "========================="

cd /Users/okonma/PycharmProjects/demoProj/img/backend

echo "📋 发现的nginx配置问题:"
echo ""
echo "1. ❌ 日志格式使用了不存在的变量:"
echo "   - \$upstream_addr 和 \$upstream_response_time 在某些nginx版本中不可用"
echo ""
echo "2. ❌ CORS处理使用了 if 语句:"
echo "   - nginx中的if是evil，容易导致意外行为"
echo ""  
echo "3. ❌ proxy_pass URL结尾不一致:"
echo "   - 有些有/，有些没有，会导致路径重写问题"
echo ""
echo "4. ❌ location匹配符使用错误:"
echo "   - ^~ 修饰符可能导致路由冲突"
echo ""

echo "🔧 应用修复..."
echo ""
echo "1. 备份原配置..."
cp nginx-proxy-fixed.conf nginx-proxy-fixed.conf.backup

echo ""
echo "2. 应用修正配置..."
cp nginx-proxy-corrected.conf nginx-proxy-fixed.conf

echo ""
echo "3. 修复说明:"
echo "   ✅ 简化了日志格式，移除了不兼容的变量"
echo "   ✅ 用location块替换了if语句处理OPTIONS请求"
echo "   ✅ 统一了proxy_pass URL格式"
echo "   ✅ 简化了location匹配符"
echo "   ✅ 改善了错误页面处理"
echo "   ✅ 添加了更好的调试端点"
echo ""

echo "4. 创建配置验证脚本..."
cat > validate-nginx-simple.sh << 'EOF'
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
EOF

chmod +x validate-nginx-simple.sh

echo ""
echo "5. 运行简单验证..."
./validate-nginx-simple.sh

echo ""
echo "6. 更新docker-compose配置..."
echo "确保docker-compose使用修正的配置文件..."

# 检查docker-compose是否正确引用配置文件
if grep -q "nginx-proxy-fixed.conf" docker-compose-fullstack.yml; then
    echo "✅ docker-compose配置正确"
else
    echo "⚠️  docker-compose可能需要更新配置文件引用"
fi

echo ""
echo "🎯 nginx配置修复完成!"
echo ""
echo "主要修复内容:"
echo "1. 移除了不兼容的nginx日志变量"
echo "2. 改用location块处理CORS预检请求"
echo "3. 统一了proxy_pass URL格式" 
echo "4. 简化了location匹配规则"
echo "5. 改善了错误处理"
echo ""
echo "现在可以重新部署测试:"
echo "  ./fix-api-404.sh"
echo ""
echo "如果仍有问题，备份文件在:"
echo "  nginx-proxy-fixed.conf.backup"