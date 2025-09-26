#!/usr/bin/env python3
"""
StockReport MCP 系统启动脚本

这是一个交互式启动脚本，用于在没有uv包管理器的环境中启动MCP服务器。
脚本会自动检测和安装必要的依赖包，并提供友好的用户界面来选择数据源。

主要功能:
- 自动检测Python环境和依赖包
- 交互式选择数据源（AkShare或Baostock）
- 自动安装缺失的依赖包
- 启动相应的MCP服务器

适用场景:
- 没有安装uv包管理器的环境
- 需要快速体验项目功能
- 系统Python环境部署
- 教学和演示用途

使用方法:
    python system_start.py

支持的数据源:
- AkShare: 支持A股、港股、美股，数据覆盖面广
- Baostock: 专注A股和宏观数据，数据质量高

作者: StockReport MCP Project
许可证: MIT License
"""
import subprocess
import sys
import os

def check_and_install_package(package_name):
    """检查并安装包"""
    try:
        __import__(package_name)
        return True
    except ImportError:
        print(f"📦 安装 {package_name}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
            return True
        except subprocess.CalledProcessError:
            print(f"❌ 安装 {package_name} 失败")
            return False

def main():
    print("🚀 StockReport MCP 系统启动")
    print("=" * 50)
    
    # 检查基础依赖
    required_packages = ["pandas", "mcp"]
    
    print("\n🔍 检查基础依赖...")
    for package in required_packages:
        if not check_and_install_package(package):
            print(f"❌ 无法安装 {package}，请手动安装")
            return
    
    # 获取数据源选择
    print("\n📊 选择数据源:")
    print("1. AkShare (推荐 - 支持A股、港股、美股)")
    print("2. Baostock (A股、指数、宏观数据)")
    
    while True:
        choice = input("\n请选择 (1-2): ").strip()
        if choice == "1":
            data_source = "akshare"
            # 检查akshare
            if not check_and_install_package("akshare"):
                return
            break
        elif choice == "2":
            data_source = "baostock"
            # 检查baostock
            if not check_and_install_package("baostock"):
                return
            break
        else:
            print("❌ 无效选择，请输入 1 或 2")
    
    print(f"\n✅ 选择数据源: {data_source.upper()}")
    
    # 尝试安装fastmcp
    print("\n🔍 检查 FastMCP...")
    if not check_and_install_package("fastmcp"):
        print("❌ FastMCP 安装失败，尝试从源码安装...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "git+https://github.com/jlowin/fastmcp.git"])
            print("✅ FastMCP 从源码安装成功")
        except subprocess.CalledProcessError:
            print("❌ FastMCP 安装失败，请手动安装")
            return
    
    # 直接启动服务器
    print("\n🔄 启动 MCP 服务器...")
    try:
        cmd = [sys.executable, "mcp_server.py", "--data-source", data_source]
        subprocess.run(cmd, cwd=os.path.dirname(os.path.abspath(__file__)))
    except KeyboardInterrupt:
        print("\n\n👋 服务器已停止")
    except Exception as e:
        print(f"\n❌ 启动失败: {e}")

if __name__ == "__main__":
    main()