#!/usr/bin/env python3
"""
MCP Server 兼容性入口文件

为了保持向后兼容性，这个文件重定向到 src/mcp_server.py
这样既支持新的包结构（用于 UV 包管理器），也支持旧的直接启动方式（用于 Trae AI）

使用方式:
- Trae AI: python mcp_server.py --data-source hybrid
- Cherry Studio (UV): uvx --from . stockreport-mcp --data-source hybrid

作者: StockReport MCP Project
版本: 1.0.0
许可证: MIT License
"""

import sys
import os

# 添加 src 目录到 Python 路径
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

# 导入并运行实际的 MCP 服务器
if __name__ == "__main__":
    try:
        # 从 src 目录导入主服务器
        from src.mcp_server import main
        main()
    except ImportError as e:
        print(f"❌ 导入错误: {e}")
        print("💡 请确保 src/mcp_server.py 文件存在")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        sys.exit(1)