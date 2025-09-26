# StockReport MCP 启动指南

## ✅ 问题已解决！

MCP 服务器现在可以正常启动了。主要问题是虚拟环境中的依赖冲突，已通过使用系统 Python 解决。

## 🚀 推荐启动方式

### 方式一：使用系统级启动脚本（推荐）
```bash
start_mcp_system.bat
```

### 方式二：直接命令行启动
```bash
python mcp_server.py --data-source akshare
```

### 方式三：使用简化版服务器（备用）
```bash
python simple_mcp_server.py --data-source akshare
```

## 📋 已修复的问题

1. **依赖导入错误**：修复了 `format_dataframe_as_markdown` 函数名不匹配的问题
2. **虚拟环境冲突**：绕过虚拟环境，使用系统 Python 直接运行
3. **包依赖缺失**：确保所有必需的包都已正确安装

## 🔧 功能验证

MCP 服务器现在支持：
- ✅ A股数据查询（AkShare 数据源）
- ✅ 港股数据查询
- ✅ 美股数据查询
- ✅ 完整的 FastMCP 功能
- ✅ 交互式查询界面

## 📊 数据源选择

- **AkShare**（推荐）：支持 A股、港股、美股，数据丰富
- **Baostock**：主要支持 A股，在 Windows 上可能有输出问题

## 🛠️ 故障排除

如果遇到问题：

1. **检查 Python 版本**：确保使用 Python 3.8+
2. **检查包安装**：运行 `python -c "import fastmcp, akshare"`
3. **使用备用方案**：运行 `simple_mcp_server.py`

## 📞 技术支持

如需进一步帮助，请提供：
- 错误信息截图
- Python 版本信息
- 操作系统信息

---
*最后更新：2025-09-22*