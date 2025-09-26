@echo off
chcp 65001 >nul
title Financial Data MCP Server

echo.
echo ========================================
echo 🚀 Financial Data MCP Server 启动器
echo ========================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 未找到Python，请先安装Python 3.8+
    pause
    exit /b 1
)

REM 切换到脚本目录
cd /d "%~dp0"

REM 运行启动脚本
python start_server.py

pause