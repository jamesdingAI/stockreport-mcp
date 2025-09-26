#!/usr/bin/env python3
"""
Cherry Studio 配置测试脚本

这个脚本帮助验证 StockReport MCP 在 Cherry Studio 中的配置是否正确。
运行此脚本可以快速诊断常见的配置问题。
"""

import sys
import os
import subprocess
import json
from pathlib import Path

def print_header(title):
    """打印标题"""
    print(f"\n{'='*50}")
    print(f"🔍 {title}")
    print('='*50)

def print_success(message):
    """打印成功信息"""
    print(f"✅ {message}")

def print_error(message):
    """打印错误信息"""
    print(f"❌ {message}")

def print_warning(message):
    """打印警告信息"""
    print(f"⚠️  {message}")

def check_python_version():
    """检查Python版本"""
    print_header("检查 Python 环境")
    
    version = sys.version_info
    print(f"Python 版本: {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 12:
        print_success("Python 版本符合要求 (>=3.12)")
        return True
    else:
        print_error("Python 版本过低，需要 3.12 或更高版本")
        return False

def check_project_structure():
    """检查项目结构"""
    print_header("检查项目结构")
    
    current_dir = Path.cwd()
    print(f"当前目录: {current_dir}")
    
    required_files = [
        "pyproject.toml",
        "src/mcp_server.py",
        "src/__init__.py",
        "uv.lock"
    ]
    
    all_exist = True
    for file_path in required_files:
        full_path = current_dir / file_path
        if full_path.exists():
            print_success(f"找到文件: {file_path}")
        else:
            print_error(f"缺少文件: {file_path}")
            all_exist = False
    
    return all_exist

def check_uv_installation():
    """检查UV安装"""
    print_header("检查 UV 包管理器")
    
    try:
        result = subprocess.run(["uv", "--version"], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print_success(f"UV 已安装: {result.stdout.strip()}")
            return True
        else:
            print_error("UV 未正确安装")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print_error("UV 未安装或不在 PATH 中")
        return False

def test_uv_sync():
    """测试UV同步"""
    print_header("测试 UV 同步")
    
    try:
        print("正在运行 uv sync...")
        result = subprocess.run(["uv", "sync"], 
                              capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            print_success("UV 同步成功")
            return True
        else:
            print_error(f"UV 同步失败: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print_error("UV 同步超时")
        return False

def test_uvx_command():
    """测试UVX命令"""
    print_header("测试 UVX 命令")
    
    try:
        print("正在测试 uvx --from . stockreport-mcp --help...")
        result = subprocess.run(["uvx", "--from", ".", "stockreport-mcp", "--help"], 
                              capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print_success("UVX 命令测试成功")
            print("输出预览:")
            print(result.stdout[:200] + "..." if len(result.stdout) > 200 else result.stdout)
            return True
        else:
            print_error(f"UVX 命令测试失败: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print_error("UVX 命令测试超时")
        return False

def generate_cherry_config():
    """生成Cherry Studio配置"""
    print_header("生成 Cherry Studio 配置")
    
    current_dir = Path.cwd()
    
    configs = {
        "UV方案（推荐）": {
            "mcpServers": {
                "stockreport-mcp": {
                    "command": "uvx",
                    "args": ["--from", str(current_dir), "stockreport-mcp", "--data-source", "hybrid"]
                }
            }
        },
        "Python直接启动": {
            "mcpServers": {
                "stockreport-mcp": {
                    "command": "python",
                    "args": [str(current_dir / "src" / "mcp_server.py"), "--data-source", "hybrid"]
                }
            }
        }
    }
    
    print("推荐的 Cherry Studio 配置:")
    for name, config in configs.items():
        print(f"\n📋 {name}:")
        print("```json")
        print(json.dumps(config, indent=2, ensure_ascii=False))
        print("```")
    
    return configs

def main():
    """主函数"""
    print("🚀 Cherry Studio StockReport MCP 配置测试")
    print("此脚本将检查您的环境配置是否正确")
    
    checks = [
        ("Python 版本", check_python_version),
        ("项目结构", check_project_structure),
        ("UV 安装", check_uv_installation),
        ("UV 同步", test_uv_sync),
        ("UVX 命令", test_uvx_command)
    ]
    
    results = {}
    for name, check_func in checks:
        try:
            results[name] = check_func()
        except Exception as e:
            print_error(f"{name} 检查时出错: {e}")
            results[name] = False
    
    # 生成配置
    generate_cherry_config()
    
    # 总结
    print_header("检查结果总结")
    
    passed = sum(results.values())
    total = len(results)
    
    for name, result in results.items():
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{name}: {status}")
    
    print(f"\n总体结果: {passed}/{total} 项检查通过")
    
    if passed == total:
        print_success("🎉 所有检查都通过！您可以在 Cherry Studio 中使用推荐的配置。")
    elif passed >= total - 1:
        print_warning("⚠️  大部分检查通过，建议使用 Python 直接启动方案。")
    else:
        print_error("❌ 多项检查失败，请根据上述错误信息进行修复。")
    
    print("\n📚 更多帮助:")
    print("- 查看 CHERRY_STUDIO_GUIDE.md")
    print("- 查看 CHERRY_STUDIO_TROUBLESHOOTING.md")
    print("- 运行 'python test_cherry_config.py' 重新测试")

if __name__ == "__main__":
    main()