@echo off
REM ===================================================
REM  Netease Enterprise Mail Downloader Launcher
REM ===================================================

chcp 65001 > nul
title Netease Mail Downloader

echo.
echo ================================================
echo      Netease Enterprise Mail Downloader
echo ================================================
echo.

REM Save current directory
set CURRENT_DIR=%~dp0
set PARENT_DIR=%CURRENT_DIR%..

REM Find Python
set PYTHON_CMD=
where python >nul 2>&1
if %errorlevel% == 0 set PYTHON_CMD=python
if not defined PYTHON_CMD where python3 >nul 2>&1
if %errorlevel% == 0 set PYTHON_CMD=python3
if not defined PYTHON_CMD where py >nul 2>&1
if %errorlevel% == 0 set PYTHON_CMD=py

if not defined PYTHON_CMD (
    echo [ERROR] Python not found
    echo.
    echo Please install Python first: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    echo Or run "check-environment.bat" for diagnosis
    echo.
    pause
    exit /b 1
)

echo [INFO] Found Python: %PYTHON_CMD%
%PYTHON_CMD% --version
echo.

REM Check main program file
if not exist "%PARENT_DIR%\easy_mail_downloader.py" (
    echo [ERROR] Main program file not found
    echo Expected location: %PARENT_DIR%\easy_mail_downloader.py
    echo.
    pause
    exit /b 1
)

echo [INFO] Starting program...
echo.

REM Switch to main program directory and run
cd /d "%PARENT_DIR%"
%PYTHON_CMD% easy_mail_downloader.py

echo.
pause
