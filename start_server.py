#!/usr/bin/env python3
"""
StockReport MCP Server 启动脚本
提供交互式数据源选择功能
"""

import sys
import subprocess
import os
from pathlib import Path

def print_banner():
    """打印启动横幅"""
    print("=" * 60)
    print("🚀 Financial Data MCP Server 启动器")
    print("=" * 60)
    print()

def print_data_source_info():
    """打印数据源信息"""
    print("📊 可用数据源:")
    print()
    print("1. Hybrid (推荐，默认)")
    print("   🎯 智能混合数据源，自动选择最佳数据源")
    print("   📈 A股: Baostock (详细财务数据)")
    print("   🌍 港股/美股: AkShare (实时行情)")
    print("   📊 宏观数据: Baostock (权威指标)")
    print()
    print("2. Baostock")
    print("   🎯 支持: A股、指数、财务数据、宏观经济数据")
    print("   ✅ 优势: 数据完整、稳定可靠")
    print("   📈 适用: 深度A股分析、财务研究")
    print()
    print("3. AkShare")
    print("   🌍 支持: A股、港股、美股")
    print("   ✅ 优势: 多市场覆盖、实时数据")
    print("   📈 适用: 全球市场分析、跨市场比较")
    print()

def get_user_choice():
    """获取用户选择"""
    while True:
        try:
            choice = input("请选择数据源 (1-Hybrid, 2-Baostock, 3-AkShare, 默认1): ").strip()
            
            if choice == "" or choice == "1":
                return "hybrid"
            elif choice == "2":
                return "baostock"
            elif choice == "3":
                return "akshare"
            else:
                print("❌ 无效选择，请输入 1、2 或 3")
                continue
                
        except KeyboardInterrupt:
            print("\n\n👋 用户取消操作")
            sys.exit(0)
        except EOFError:
            print("\n\n👋 输入结束")
            sys.exit(0)

def get_log_level():
    """获取日志级别"""
    print("\n📝 日志级别:")
    print("1. INFO (默认) - 基本信息")
    print("2. DEBUG - 详细调试信息")
    print("3. WARNING - 仅警告和错误")
    print("4. ERROR - 仅错误信息")
    
    while True:
        try:
            choice = input("请选择日志级别 (1-4, 默认1): ").strip()
            
            if choice == "" or choice == "1":
                return "INFO"
            elif choice == "2":
                return "DEBUG"
            elif choice == "3":
                return "WARNING"
            elif choice == "4":
                return "ERROR"
            else:
                print("❌ 无效选择，请输入 1-4")
                continue
                
        except KeyboardInterrupt:
            print("\n\n👋 用户取消操作")
            sys.exit(0)

def check_dependencies(data_source):
    """检查依赖包"""
    print(f"\n🔍 检查 {data_source.upper()} 数据源依赖...")
    
    required_packages = ["pandas", "fastmcp"]
    
    if data_source == "baostock":
        required_packages.append("baostock")
    elif data_source == "akshare":
        required_packages.append("akshare")
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package} (缺失)")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  缺少依赖包: {', '.join(missing_packages)}")
        install = input("是否自动安装缺失的包? (y/N): ").strip().lower()
        
        if install in ['y', 'yes']:
            print("📦 使用 uv 同步依赖...")
            try:
                # 使用 uv sync 来安装所有依赖
                subprocess.check_call(["uv", "sync"], cwd=os.path.dirname(os.path.abspath(__file__)))
                print("  ✅ 依赖同步成功")
            except subprocess.CalledProcessError:
                print("  ❌ 依赖同步失败")
                print("  💡 请尝试手动运行: uv sync")
                return False
        else:
            print("❌ 请手动安装缺失的依赖包后重试")
            return False
    
    return True

def start_server(data_source, log_level):
    """启动服务器"""
    print(f"\n🚀 启动服务器...")
    print(f"📊 数据源: {data_source.upper()}")
    print(f"📝 日志级别: {log_level}")
    print("=" * 60)
    
    # 构建命令
    script_dir = Path(__file__).parent
    server_script = script_dir / "mcp_server.py"
    
    cmd = [
        sys.executable,
        str(server_script),
        "--data-source", data_source,
        "--log-level", log_level
    ]
    
    try:
        # 启动服务器
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\n\n👋 服务器已停止")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ 服务器启动失败: {e}")
        sys.exit(1)

def main():
    """主函数"""
    print_banner()
    print_data_source_info()
    
    # 获取用户选择
    data_source = get_user_choice()
    log_level = get_log_level()
    
    # 检查依赖
    if not check_dependencies(data_source):
        sys.exit(1)
    
    # 启动服务器
    start_server(data_source, log_level)

if __name__ == "__main__":
    main()