@echo off
REM ===================================================
REM  网易企业邮箱下载工具启动脚本
REM ===================================================

chcp 65001 > nul
title 网易企业邮箱下载工具

echo.
echo ================================================
echo          网易企业邮箱下载工具
echo ================================================
echo.

REM 保存当前目录
set CURRENT_DIR=%~dp0
set PARENT_DIR=%CURRENT_DIR%..

REM 查找 Python
set PYTHON_CMD=
where python >nul 2>&1
if %errorlevel% == 0 set PYTHON_CMD=python
if not defined PYTHON_CMD where python3 >nul 2>&1
if %errorlevel% == 0 set PYTHON_CMD=python3
if not defined PYTHON_CMD where py >nul 2>&1
if %errorlevel% == 0 set PYTHON_CMD=py

if not defined PYTHON_CMD (
    echo [错误] 未找到 Python
    echo.
    echo 请先安装 Python: https://www.python.org/downloads/
    echo 安装时务必勾选 "Add Python to PATH"
    echo.
    echo 或运行 "检查环境.bat" 进行诊断
    echo.
    pause
    exit /b 1
)

echo [信息] 找到 Python: %PYTHON_CMD%
%PYTHON_CMD% --version
echo.

REM 检查主程序文件
if not exist "%PARENT_DIR%\easy_mail_downloader.py" (
    echo [错误] 未找到主程序文件
    echo 期望位置: %PARENT_DIR%\easy_mail_downloader.py
    echo.
    pause
    exit /b 1
)

echo [信息] 正在启动程序...
echo.

REM 切换到主程序目录并运行
cd /d "%PARENT_DIR%"
%PYTHON_CMD% easy_mail_downloader.py

echo.
pause
