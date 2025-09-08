#!/bin/bash

# Gemini API Key 设置脚本
echo "🔑 Gemini API Key 配置向导"
echo "========================"

# 检查是否已设置环境变量
if [[ -n "$GEMINI_API_KEY" ]]; then
    echo "✅ GEMINI_API_KEY 环境变量已设置"
    echo "当前值: ${GEMINI_API_KEY:0:8}..."
    echo ""
    read -p "是否要更新API Key? (y/n): " update_key
    if [[ $update_key != "y" && $update_key != "Y" ]]; then
        echo "配置保持不变"
        exit 0
    fi
fi

echo ""
echo "📖 获取Gemini API Key:"
echo "1. 访问: https://aistudio.google.com/app/apikey"
echo "2. 登录Google账户"
echo "3. 点击 'Create API Key'"
echo "4. 复制生成的API Key"
echo ""

# 获取API Key
read -p "请输入您的Gemini API Key: " api_key

if [[ -z "$api_key" ]]; then
    echo "❌ API Key不能为空"
    exit 1
fi

# 验证API Key格式 (Gemini API Key通常以 AIza 开头)
if [[ ! "$api_key" =~ ^AIza.* ]]; then
    echo "⚠️  警告: API Key格式可能不正确 (通常以'AIza'开头)"
    read -p "是否继续? (y/n): " continue_anyway
    if [[ $continue_anyway != "y" && $continue_anyway != "Y" ]]; then
        exit 1
    fi
fi

# 选择配置方式
echo ""
echo "选择配置方式:"
echo "1) 创建 .env 文件 (推荐)"
echo "2) 设置系统环境变量"
echo "3) 仅显示Docker运行命令"
read -p "请选择 (1-3): " config_method

case $config_method in
    1)
        # 创建 .env 文件
        cat > .env << EOF
# Img Gen Backend Environment Variables
GEMINI_API_KEY=$api_key
FLASK_ENV=production
EOF
        echo "✅ .env 文件已创建"
        echo "💡 启动命令: docker-compose -f docker-compose-fullstack.yml --env-file .env up -d"
        ;;
    2)
        # 系统环境变量
        echo "export GEMINI_API_KEY='$api_key'" >> ~/.bashrc
        echo "✅ 环境变量已添加到 ~/.bashrc"
        echo "💡 运行: source ~/.bashrc 使设置生效"
        ;;
    3)
        # 仅显示命令
        echo "💡 Docker 运行命令:"
        echo "GEMINI_API_KEY='$api_key' docker-compose -f docker-compose-fullstack.yml up -d"
        ;;
    *)
        echo "❌ 无效选择"
        exit 1
        ;;
esac

echo ""
echo "🚀 配置完成！现在可以启动服务了"
echo ""
echo "测试API Key是否工作:"
echo "export GEMINI_API_KEY='$api_key'"
echo "python -c \"import os; os.environ['GEMINI_API_KEY']='$api_key'; import gemini_api; print('✅ API Key配置正确')\""