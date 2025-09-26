#!/usr/bin/env python3
"""
MCP Server 模块入口点
允许使用 python -m mcp_server 启动服务器
"""

import sys
import os

# 添加当前目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# 导入并运行主服务器
if __name__ == "__main__":
    from mcp_server import main
    main()