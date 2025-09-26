# Trae StockReport MCP配置修复指南

## 🚨 问题诊断

您遇到的错误：`c:\users\79475\没有mcpserver.py文件`

**原因分析**：
1. 配置文件中的路径不正确
2. 使用了旧的启动脚本路径
3. 缺少工作目录(cwd)配置

## ✅ 解决方案

### 方案一：使用简化配置（推荐）

在Trae AI中使用以下配置：

```json
{
  "mcpServers": {
    "stockreport-mcp": {
      "command": "python",
      "args": ["mcp_server.py", "--data-source", "hybrid"],
      "cwd": "D:\\stockreport-mcp"
    }
  }
}
```

**注意**：我们提供了兼容性的 `mcp_server.py` 文件在根目录，它会自动重定向到 `src/mcp_server.py`，确保向后兼容性。

### 方案二：使用完整配置

```json
{
  "mcpServers": {
    "stockreport-mcp": {
      "command": "python",
      "args": [
        "mcp_server.py",
        "--data-source",
        "hybrid"
      ],
      "cwd": "D:\\stockreport-mcp",
      "env": {
        "PYTHONIOENCODING": "utf-8",
        "PYTHONUNBUFFERED": "1"
      }
    }
  }
}
```

## 📁 配置文件位置

项目中提供了以下配置文件：

1. **`trae_config_simple.json`** - 简化配置（推荐）
2. **`trae_mcp_config.json`** - 完整配置（已更新）

## 🔧 配置步骤

### 1. 确认MCP服务器正在运行

首先确保MCP服务器已启动：

```bash
cd D:\stockreport-mcp
python mcp_server.py --data-source hybrid
```

您应该看到类似输出：
```
[OK] 使用数据源: HYBRID
[INFO] 智能混合数据源:
       - A股: Baostock (详细财务数据)
       - 港股/美股: AkShare (实时行情)
       - 宏观数据: Baostock (权威指标)
```

### 2. 在Trae AI中配置MCP

1. 打开Trae AI设置
2. 找到MCP服务器配置部分
3. 添加或更新配置，使用上述JSON配置
4. 保存并重启Trae AI

### 3. 验证连接

配置完成后，在Trae AI中应该能看到：
- StockReport MCP服务器已连接
- 可以使用股票查询功能
- 支持A股、港股、美股数据

## 🎯 关键配置要点

### ✅ 正确配置
- **command**: `"python"` - 使用Python解释器
- **args**: `["mcp_server.py", "--data-source", "hybrid"]` - 启动混合数据源
- **cwd**: `"D:\\stockreport-mcp"` - 设置正确的工作目录

### ❌ 常见错误
- 缺少`cwd`配置导致找不到文件
- 使用绝对路径而不是相对路径
- 使用旧的启动脚本路径

## 🔍 故障排除

### 问题1：找不到mcp_server.py
**解决方案**：确保`cwd`设置为`D:\stockreport-mcp`

### 问题2：Python模块导入错误
**解决方案**：确保在项目目录下运行，并且已安装依赖

### 问题3：数据源连接失败
**解决方案**：检查网络连接，确保Baostock和AkShare可以正常访问

## 📊 功能验证

配置成功后，您可以在Trae AI中测试：

1. **A股查询**：`获取平安银行(000001)的基本信息`
2. **港股查询**：`获取阿里巴巴(09988)的股价信息`
3. **美股查询**：`获取苹果(AAPL)的基本信息`

## 🆘 获取帮助

如果仍有问题：
1. 检查MCP服务器日志输出
2. 确认Python环境和依赖包
3. 验证项目路径是否正确

---

**最后更新**: 2025-09-23  
**适用版本**: Trae AI + StockReport MCP v1.0.0