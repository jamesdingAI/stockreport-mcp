# Trae AI 通用MCP配置指南

## 问题解决

您遇到的 "No module named mcp_server" 错误已解决！我提供了两个解决方案：

### ✅ 解决方案1: 直接脚本启动 (推荐)

```json
{
  "mcpServers": {
    "stockreport-mcp": {
      "command": "python",
      "args": ["mcp_server.py", "--data-source", "hybrid"],
      "cwd": "D:/stockreport-mcp"
    }
  }
}
```

**优势**:
- ✅ 兼容性最好，适用于所有Python环境
- ✅ 无需额外的模块配置
- ✅ 已验证在您的环境中工作

### ✅ 解决方案2: 模块启动 (备选)

```json
{
  "mcpServers": {
    "stockreport-mcp": {
      "command": "python",
      "args": ["-m", "mcp_server", "--data-source", "hybrid"],
      "cwd": "D:/stockreport-mcp"
    }
  }
}
```

**说明**: 我已添加了 `__main__.py` 文件，现在模块启动方式也应该工作了。

## 快速配置步骤

### 1. 选择配置文件
使用更新后的配置文件：
- **推荐**: `trae_verified_config.json` (已更新为直接脚本启动)

### 2. 复制到Trae AI
1. 打开Trae AI设置
2. 找到MCP服务器配置
3. 复制以下配置：

```json
{
  "mcpServers": {
    "stockreport-mcp": {
      "command": "python",
      "args": ["mcp_server.py", "--data-source", "hybrid"],
      "cwd": "D:/stockreport-mcp"
    }
  }
}
```

### 3. 保存并重启
- 保存配置
- 重启Trae AI
- 验证连接

## 验证成功标志

启动后应该看到：
```
✅ StockReport MCP服务器已连接
✅ 混合数据源已激活 (A股: Baostock, 港股/美股: AkShare)
✅ 所有工具已注册
```

## 关键配置说明

### 路径配置
- **cwd**: `"D:/stockreport-mcp"` (必须是项目根目录)
- **脚本**: `"mcp_server.py"` (兼容性入口文件，自动重定向到 src/mcp_server.py)

### 数据源配置
- **参数**: `"--data-source", "hybrid"`
- **智能路由**: A股用Baostock，港股/美股用AkShare

## 故障排除

### 如果仍有问题
1. **检查路径**: 确保 `D:/stockreport-mcp` 是正确的项目路径
2. **检查文件**: 确认 `mcp_server.py` 存在
3. **检查Python**: 确认Python可以访问项目目录

### 测试命令
在项目目录下运行：
```bash
# 测试直接启动
python mcp_server.py --data-source hybrid

# 测试模块启动 (现在也应该工作)
python -m mcp_server --data-source hybrid
```

## 技术说明

### 为什么模块导入失败？
- Python模块导入需要特定的目录结构
- 不同的Python环境可能有不同的路径解析规则
- 直接脚本启动更加可靠和通用

### 添加的文件
- `__main__.py`: 使模块导入方式也能工作
- 更新的配置文件: 使用更可靠的直接启动方式

---

**状态**: ✅ 问题已解决
**推荐配置**: 直接脚本启动方式
**测试环境**: Python 3.13.7, Windows
**最后更新**: 2025-09-23