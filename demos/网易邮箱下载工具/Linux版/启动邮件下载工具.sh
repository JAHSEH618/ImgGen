#!/bin/bash

# 网易企业邮箱下载工具启动脚本

echo ""
echo "================================================"
echo "          网易企业邮箱下载工具"
echo "================================================"
echo ""

# 检查 Python 是否安装
if ! command -v python3 &> /dev/null; then
    echo "[错误] 未检测到 Python 3，请先安装 Python 3.6 或更高版本"
    echo ""
    echo "macOS 安装方法:"
    echo "  brew install python3"
    echo ""
    echo "Linux 安装方法:"
    echo "  Ubuntu/Debian: sudo apt-get install python3"
    echo "  CentOS/RHEL: sudo yum install python3"
    echo ""
    exit 1
fi

echo "[提示] 检测到 Python 环境"
python3 --version
echo ""

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
# 切换到父目录（主程序所在位置）
cd "$SCRIPT_DIR/.."

# 运行脚本
python3 easy_mail_downloader.py

# 等待用户按键
echo ""
read -p "按回车键退出..."
