@echo off
chcp 65001 >nul
title StockReport MCP Server

echo.
echo ========================================
echo 🚀 股票报告MCP服务器启动器
echo ========================================
echo.

REM 切换到脚本目录
cd /d "%~dp0"

REM 检查虚拟环境是否存在
if not exist ".venv\Scripts\activate.bat" (
    echo ❌ 虚拟环境不存在，请先运行 reset_env.bat 创建环境
    pause
    exit /b 1
)

REM 激活虚拟环境
echo 🔄 激活虚拟环境...
call .venv\Scripts\activate.bat

REM 设置Python路径
set PYTHONPATH=%CD%

REM 启动MCP服务器
echo 🚀 启动MCP服务器（使用AkShare数据源）...
echo 按 Ctrl+C 停止服务器
echo.
python mcp_server.py --data-source akshare

pause