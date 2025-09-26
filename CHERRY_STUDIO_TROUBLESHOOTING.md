# 🔧 Cherry Studio StockReport MCP 故障排除指南

## ⚠️ 重要提醒：客户端兼容性问题

**🚨 关键发现**：Cherry Studio 在 MCP 工具调用方面存在已知的兼容性问题。即使服务器配置正确且能正常启动，工具调用功能可能无法正常工作。

**推荐解决方案**：
- ✅ **推荐使用 Trae AI**：完全支持 MCP 工具调用，所有功能正常
- ✅ **推荐使用 Claude Desktop**：官方 MCP 支持，兼容性优秀
- ⚠️ **Cherry Studio 限制**：存在工具调用失败问题（参见 [GitHub Issue #3513](https://github.com/CherryHQ/cherry-studio/issues/3513)）

**详细兼容性信息**：请参阅 `MCP_CLIENT_COMPATIBILITY_GUIDE.md` 文档。

---

## 📖 概述

本文档提供了在 Cherry Studio 中使用 StockReport MCP 时可能遇到的常见问题及其解决方案。通过这个指南，你可以快速诊断和解决大部分配置和使用问题。

**注意**：由于 Cherry Studio 的 MCP 兼容性问题，建议优先考虑使用其他客户端。

## 🚨 常见问题分类

### 1. 配置问题
- MCP 服务器无法启动
- 配置文件错误
- 路径问题

### 2. 连接问题
- 服务器连接失败
- 超时错误
- 权限问题

### 3. 数据问题
- 数据获取失败
- 返回结果为空
- 数据格式错误

### 4. 性能问题
- 响应缓慢
- 内存占用过高
- 频繁崩溃

## 🔍 问题诊断流程

### 步骤1：检查基础配置
1. 确认 Python 环境是否正确安装
2. 验证依赖包是否完整
3. 检查配置文件语法

### 步骤2：验证网络连接
1. 测试网络连接
2. 检查防火墙设置
3. 验证代理配置

### 步骤3：查看日志信息
1. 检查 Cherry Studio 日志
2. 查看 MCP 服务器日志
3. 分析错误信息

## 🛠️ 具体问题解决方案

### 问题1：JSON 配置格式错误

#### 错误类型A：缺少 mcpServers 包装对象

**错误信息：**
```
无效输入，请检查json格式：mcp servers:invalid input:expected record,received undefined
```

**原因：**
- Cherry Studio 必须使用 `mcpServers` 对象包装所有服务器配置
- 不能直接配置单个服务器对象，这会导致 "expected record, received undefined" 错误

#### 错误类型B：不支持的配置字段

**错误信息：**
```
无效输入，请检查json格式：mcpservers.stockreport-mcp.type:invalid input mcpservers.stockreport-mcp:unrecognized key:"cwd"
```

**原因：**
- Cherry Studio 只支持 `command`、`args` 和 `env` 字段
- 不支持 `type`、`cwd`、`name` 等字段

#### 错误类型C：JSON 格式错误

**错误信息：**
```
Error Details: 
{ 
  "message": "无效输入，请检查 JSON 格式: \n: Invalid input: expected object, received null" 
}
Invalid input: expected object, received null
```

**原因分析：**
这个错误通常出现在使用 UV 包管理器配置时，主要原因包括：
1. **JSON 结构错误**：Cherry Studio 需要完整的 `mcpServers` 对象结构
2. 项目包结构配置问题
3. 入口点配置错误
4. UV 缓存问题

**解决方案：**

1. **使用正确的 JSON 配置格式**：

**UV 方案（推荐）：**
```json
{
  "mcpServers": {
    "stockreport-mcp": {
      "command": "uvx",
      "args": ["--from", "D:/stockreport-mcp", "stockreport-mcp", "--data-source", "hybrid"]
    }
  }
}
```

**直接 Python 启动方案**：
```json
{
  "mcpServers": {
    "stockreport-mcp": {
      "command": "python",
      "args": ["D:/stockreport-mcp/mcp_server.py", "--data-source", "hybrid"]
    }
  }
}
```

**重要提示：**
- Cherry Studio 必须使用 `mcpServers` 对象包装所有服务器配置
- Cherry Studio 只支持 `command`、`args` 和 `env` 字段，不支持 `type`、`cwd`、`name` 等字段
- 必须使用完整的文件路径，因为不支持 `cwd` 字段

3. **清理 UV 缓存**：
```bash
cd D:/stockreport-mcp
uv cache clean
uv sync
```

4. **验证配置**：
```bash
# 测试命令是否正常工作
uvx --from . stockreport-mcp --help
```

### 问题2：MCP 服务器无法启动

**错误信息：**
```
Failed to start MCP server
Server process exited with code 1
```

**可能原因：**
- Python 环境问题
- 依赖包缺失
- 配置文件错误
- 路径问题

**解决方案：**

#### 方案A：检查 Python 环境
```bash
# 验证 Python 版本
python --version

# 检查是否在正确的虚拟环境中
where python

# 重新激活虚拟环境
.\.venv\Scripts\Activate.ps1
```

#### 方案B：重新安装依赖
```bash
# 使用 pip 重新安装
pip install -r requirements.txt

# 或使用 uv（推荐）
uv sync
```

#### 方案C：修复配置文件
检查 Cherry Studio 配置中的路径是否正确：
```json
{
  "mcpServers": {
    "stockreport-mcp": {
      "command": "python",
      "args": ["mcp_server.py"],
      "cwd": "D:\\stockreport-mcp"
    }
  }
}
```

### 问题2：模块导入错误

**错误信息：**
```
ModuleNotFoundError: No module named 'mcp'
ImportError: No module named 'pandas'
```

**解决方案：**

#### 方案A：安装缺失的包
```bash
# 安装 MCP 相关包
pip install mcp

# 安装数据处理包
pip install pandas numpy

# 安装所有依赖
pip install -r requirements.txt
```

#### 方案B：使用虚拟环境
```bash
# 创建新的虚拟环境
python -m venv .venv

# 激活虚拟环境
.\.venv\Scripts\Activate.ps1

# 安装依赖
pip install -r requirements.txt
```

### 问题3：数据获取失败

**错误信息：**
```
Failed to fetch stock data
Connection timeout
API rate limit exceeded
```

**解决方案：**

#### 方案A：检查网络连接
```bash
# 测试网络连接
ping baidu.com

# 检查代理设置
echo $HTTP_PROXY
echo $HTTPS_PROXY
```

#### 方案B：配置数据源
在配置中指定备用数据源：
```json
{
  "data_sources": {
    "primary": "baostock",
    "fallback": ["tushare", "akshare"]
  }
}
```

#### 方案C：调整请求频率
```python
# 在代码中添加延迟
import time
time.sleep(1)  # 每次请求间隔1秒
```

### 问题4：权限问题

**错误信息：**
```
Permission denied
Access is denied
PermissionError: [Errno 13]
```

**解决方案：**

#### 方案A：以管理员身份运行
1. 右键点击 Cherry Studio
2. 选择"以管理员身份运行"

#### 方案B：修改文件权限
```bash
# 修改项目目录权限
icacls "D:\stockreport-mcp" /grant Users:F /T
```

#### 方案C：更改安装位置
将项目移动到用户目录下：
```bash
# 移动到用户目录
move "D:\stockreport-mcp" "%USERPROFILE%\stockreport-mcp"
```

### 问题5：配置文件语法错误

**错误信息：**
```
JSON parse error
Invalid configuration format
Unexpected token
```

**解决方案：**

#### 方案A：验证 JSON 语法
使用在线 JSON 验证器检查配置文件语法。

#### 方案B：使用标准配置模板
```json
{
  "mcpServers": {
    "stockreport-mcp": {
      "command": "python",
      "args": ["mcp_server.py"],
      "cwd": "D:\\stockreport-mcp",
      "env": {
        "PYTHONPATH": "D:\\stockreport-mcp"
      }
    }
  }
}
```

#### 方案C：逐步添加配置
从最简配置开始，逐步添加选项：
```json
{
  "mcpServers": {
    "stockreport-mcp": {
      "command": "python",
      "args": ["mcp_server.py"]
    }
  }
}
```

### 问题6：性能问题

**症状：**
- 响应缓慢
- 内存占用过高
- 频繁崩溃

**解决方案：**

#### 方案A：优化配置
```json
{
  "mcpServers": {
    "stockreport-mcp": {
      "command": "python",
      "args": ["mcp_server.py", "--max-workers", "2"],
      "cwd": "D:\\stockreport-mcp",
      "timeout": 30000
    }
  }
}
```

#### 方案B：限制并发请求
在代码中添加并发控制：
```python
import asyncio
semaphore = asyncio.Semaphore(5)  # 限制并发数为5
```

#### 方案C：清理缓存
```bash
# 清理 Python 缓存
find . -name "*.pyc" -delete
find . -name "__pycache__" -type d -exec rm -rf {} +

# 清理临时文件
del /s /q *.tmp
```

## 🔧 高级故障排除

### 调试模式启动

#### 启用详细日志
```json
{
  "mcpServers": {
    "stockreport-mcp": {
      "command": "python",
      "args": ["mcp_server.py", "--debug", "--verbose"],
      "cwd": "D:\\stockreport-mcp"
    }
  }
}
```

#### 使用调试脚本
创建 `debug_mcp.py`：
```python
import sys
import traceback
from mcp_server import main

try:
    main()
except Exception as e:
    print(f"Error: {e}")
    traceback.print_exc()
    input("Press Enter to exit...")
```

### 环境隔离测试

#### 创建测试环境
```bash
# 创建独立的测试环境
python -m venv test_env
test_env\Scripts\activate
pip install -r requirements.txt

# 测试基本功能
python -c "import mcp; print('MCP imported successfully')"
```

#### 最小化配置测试
使用最简配置进行测试：
```json
{
  "mcpServers": {
    "test-mcp": {
      "command": "python",
      "args": ["simple_mcp_server.py"]
    }
  }
}
```

## 📊 性能监控

### 系统资源监控
```bash
# 监控 CPU 和内存使用
Get-Process python | Select-Object ProcessName, CPU, WorkingSet

# 监控网络连接
netstat -an | findstr :8000
```

### 日志分析
```bash
# 查看最近的错误日志
Get-Content -Path "cherry_studio.log" -Tail 50 | Select-String "ERROR"

# 监控实时日志
Get-Content -Path "cherry_studio.log" -Wait
```

## 🆘 紧急恢复方案

### 完全重置配置
1. 备份当前配置
2. 删除 Cherry Studio 配置文件
3. 重新启动 Cherry Studio
4. 重新添加 MCP 服务器

### 重新安装 MCP 服务器
```bash
# 备份数据
copy "D:\stockreport-mcp\*.json" "D:\backup\"

# 重新克隆项目
git clone https://github.com/your-repo/stockreport-mcp.git

# 恢复配置
copy "D:\backup\*.json" "D:\stockreport-mcp\"

# 重新安装依赖
cd stockreport-mcp
pip install -r requirements.txt
```

## 📞 获取帮助

### 自助诊断清单
- [ ] Python 环境正确
- [ ] 依赖包完整
- [ ] 配置文件语法正确
- [ ] 网络连接正常
- [ ] 权限设置正确
- [ ] 日志信息已检查

### 问题报告模板
当需要寻求帮助时，请提供以下信息：

```
**环境信息：**
- 操作系统：Windows 11
- Python 版本：3.11.0
- Cherry Studio 版本：1.0.0
- MCP 版本：1.0.0

**问题描述：**
[详细描述遇到的问题]

**错误信息：**
[完整的错误信息和堆栈跟踪]

**重现步骤：**
1. [步骤1]
2. [步骤2]
3. [步骤3]

**已尝试的解决方案：**
[列出已经尝试过的解决方法]

**配置文件：**
[相关的配置文件内容]
```

### 社区资源
- GitHub Issues
- 官方文档
- 社区论坛
- 技术博客

## ✅ 预防措施

### 定期维护
1. 定期更新依赖包
2. 清理临时文件
3. 备份配置文件
4. 监控系统资源

### 最佳实践
1. 使用虚拟环境
2. 版本控制配置
3. 监控日志文件
4. 定期测试功能

### 配置备份
```bash
# 创建配置备份脚本
@echo off
set backup_dir=D:\backup\cherry_studio_%date:~0,4%%date:~5,2%%date:~8,2%
mkdir "%backup_dir%"
copy "%APPDATA%\cherry-studio\config.json" "%backup_dir%\"
copy "D:\stockreport-mcp\*.json" "%backup_dir%\"
```

## 🔄 客户端兼容性问题详解

### Cherry Studio MCP 工具调用问题

#### 问题现象
- ✅ MCP 服务器启动正常
- ✅ 工具列表显示正常
- ❌ 工具调用失败或无响应
- ❌ 出现 `tool_call_id` 相关错误

#### 根本原因
Cherry Studio 的 MCP 实现存在以下已知问题：

1. **工具调用机制缺陷**（GitHub Issue #3513）
   - 服务器虽然连接成功，但工具调用请求无法正确传递
   - 影响所有 MCP 服务器，不仅限于 stockreport-mcp

2. **tool_call_id 参数处理错误**（GitHub Issue #4274）
   - 使用 OpenAI GPT-4o-mini 时出现参数缺失错误
   - 工具调用格式与标准 MCP 协议不兼容

3. **XML 格式兼容性问题**
   - Cherry Studio 使用非标准的 XML 工具调用格式
   - 与其他 MCP 客户端的 JSON 格式不兼容

#### 临时解决方案

**方案1：切换到兼容客户端（强烈推荐）**
```
推荐客户端：
• Trae AI - 完全兼容，所有功能正常
• Claude Desktop - 官方支持，稳定可靠
• VS Code (with MCP extension) - 良好兼容性
```

**方案2：Cherry Studio 优化尝试**
```
1. 更新到最新版本的 Cherry Studio
2. 使用 Claude 3.5 Sonnet 而非 GPT-4o-mini
3. 检查模型设置中的工具调用选项
4. 清除 Cherry Studio 缓存并重启
```

#### 兼容性测试方法

**快速测试脚本**：
```bash
# 在项目目录运行
python test_client_compatibility.py
```

**手动测试步骤**：
1. 在 Cherry Studio 中尝试调用：`获取最新交易日期`
2. 在 Trae AI 中尝试相同调用
3. 比较结果差异

#### 监控和更新

**关注以下资源获取最新进展**：
- [Cherry Studio GitHub Issues](https://github.com/CherryHQ/cherry-studio/issues)
- [MCP 官方文档更新](https://modelcontextprotocol.io/)
- 项目的 `MCP_CLIENT_COMPATIBILITY_GUIDE.md` 文档

#### 报告问题

如果发现新的兼容性问题，请：
1. 记录详细的错误信息
2. 提供完整的配置文件
3. 在 Cherry Studio GitHub 仓库提交 Issue
4. 同时在本项目报告以便更新文档

---

**最后更新**：2024年12月  
**兼容性状态**：Cherry Studio 存在已知问题，推荐使用其他客户端echo Backup completed: %backup_dir%
```

## 🎯 总结

通过本故障排除指南，你应该能够解决大部分在 Cherry Studio 中使用 StockReport MCP 时遇到的问题。记住：

1. **系统性诊断**：按照流程逐步排查
2. **详细记录**：保存错误信息和解决过程
3. **预防为主**：定期维护和备份
4. **寻求帮助**：遇到复杂问题及时求助

如果问题仍然无法解决，请参考问题报告模板提供详细信息，以便获得更好的技术支持。

祝你使用愉快！ 🚀