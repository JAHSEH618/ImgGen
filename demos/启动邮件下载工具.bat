@echo off
chcp 65001 > nul
title 网易企业邮箱下载工具

echo.
echo ================================================
echo          网易企业邮箱下载工具
echo ================================================
echo.

REM 检查 Python 是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到 Python，请先安装 Python 3.6 或更高版本
    echo.
    echo 下载地址: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo [提示] 检测到 Python 环境
python --version
echo.

REM 运行脚本
python easy_mail_downloader.py

pause
