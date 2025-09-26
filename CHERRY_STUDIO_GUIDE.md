# 🍒 Cherry Studio StockReport MCP 配置指南

## 📋 概述

Cherry Studio 是一个支持多种大语言模型提供商的桌面客户端，兼容 Windows、Mac 和 Linux 系统。本指南将详细介绍如何在 Cherry Studio 中集成和使用 StockReport MCP 服务器。

## 🎯 Cherry Studio 简介

Cherry Studio 具有以下特点：
- **多模型支持**：支持 OpenAI、Gemini、Anthropic 等主流 LLM 服务商 <mcreference link="https://chat.mcp.so/client/cherry-studio/CherryHQ?tab=content" index="4">4</mcreference>
- **AI 助手**：提供 300+ 预配置 AI 助手和自定义助手创建功能 <mcreference link="https://chat.mcp.so/client/cherry-studio/CherryHQ?tab=content" index="4">4</mcreference>
- **MCP 协议支持**：原生支持 Model Context Protocol，可以无缝集成外部工具和数据源 <mcreference link="https://onedollarvps.com/blogs/how-to-use-mcp-in-cherry-studio" index="1">1</mcreference>
- **跨平台**：支持 Windows、Mac、Linux 系统 <mcreference link="https://chat.mcp.so/client/cherry-studio/CherryHQ?tab=content" index="4">4</mcreference>

## 🚀 快速开始

### 0. 配置测试（推荐）

在开始配置之前，建议先运行测试脚本来验证环境：

```bash
cd D:/stockreport-mcp
python test_cherry_config.py
```

这个脚本会：
- ✅ 检查 Python 版本和环境
- ✅ 验证项目结构完整性  
- ✅ 测试 UV 包管理器
- ✅ 生成正确的 JSON 配置
- ✅ 提供故障排除建议

如果所有检查都通过，您可以直接使用生成的配置。

### 前置要求

1. **Cherry Studio 版本**：确保使用最新版本的 Cherry Studio <mcreference link="https://onedollarvps.com/blogs/how-to-use-mcp-in-cherry-studio" index="1">1</mcreference>
2. **Python 环境**：确保系统已安装 Python 3.8+
3. **StockReport MCP 项目**：确保已下载并配置好 StockReport MCP 项目

### 安装 Cherry Studio

1. 访问 [Cherry Studio GitHub Releases](https://github.com/cherry-ai/cherry-studio/releases)
2. 下载适合你操作系统的安装包
3. 按照安装向导完成安装

## ⚙️ MCP 服务器配置

### 步骤 1：安装必要工具

Cherry Studio 需要 `uv` 和 `bun` 工具来管理 MCP 服务器： <mcreference link="https://onedollarvps.com/blogs/how-to-use-mcp-in-cherry-studio" index="1">1</mcreference>

1. 打开 Cherry Studio 设置
2. 找到 "MCP Servers" 部分
3. 点击 "Install" 按钮下载 uv 和 bun（此过程可能需要一些时间）

### 步骤 2：添加 StockReport MCP 服务器

在 Cherry Studio 中配置 StockReport MCP 服务器：

1. **打开设置**：在 Cherry Studio 中打开设置面板 <mcreference link="https://docs.cherry-ai.com/cherry-studio-wen-dang/en-us/advanced-basic/mcp/config" index="3">3</mcreference>
2. **找到 MCP Server 选项**：定位到 MCP Servers 设置部分 <mcreference link="https://docs.cherry-ai.com/cherry-studio-wen-dang/en-us/advanced-basic/mcp/config" index="3">3</mcreference>
3. **添加服务器**：点击 "Add Server" 按钮 <mcreference link="https://onedollarvps.com/blogs/how-to-use-mcp-in-cherry-studio" index="1">1</mcreference>

### 步骤 3：配置服务器参数

填写以下配置信息： <mcreference link="https://onedollarvps.com/blogs/how-to-use-mcp-in-cherry-studio" index="1">1</mcreference>

#### 方案一：基础配置

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

#### 方案二：使用虚拟环境

```json
{
  "mcpServers": {
    "stockreport-mcp": {
      "command": "D:/stockreport-mcp/.venv/Scripts/python.exe",
      "args": ["D:/stockreport-mcp/mcp_server.py", "--data-source", "hybrid"]
    }
  }
}
```

#### 方案三：使用 UV 包管理器（推荐）

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

**注意事项：**
- **重要**：Cherry Studio 需要完整的 `mcpServers` 对象结构，不能只配置单个服务器
- Cherry Studio 只支持 `command`、`args` 和 `env` 字段，不支持 `type`、`cwd`、`name` 等字段
- 必须使用完整的文件路径，因为 Cherry Studio 不支持 `cwd` 字段来指定工作目录
- 对于 UV 方案，使用 `--from` 参数指定完整的项目路径
- 如果遇到 "Invalid input: expected record, received undefined" 错误，通常是因为缺少 `mcpServers` 包装对象
  3. 是否已运行 `uv sync` 安装依赖

### 配置参数说明

- **name**：服务器显示名称，可自定义
- **type**：选择 "STDIO"，表示使用标准输入输出通信 <mcreference link="https://onedollarvps.com/blogs/how-to-use-mcp-in-cherry-studio" index="1">1</mcreference>
- **command**：启动命令
- **args**：命令参数，包括数据源选择
- **cwd**：工作目录，指向 StockReport MCP 项目路径

### 数据源选择

StockReport MCP 支持三种数据源模式：

- **hybrid**（推荐）：智能混合数据源，自动选择最佳数据源
- **baostock**：使用 Baostock 数据源
- **akshare**：使用 AkShare 数据源

## 🔧 启用和使用

### 启用 MCP 服务

1. **保存配置**：点击 "Confirm" 保存 MCP 服务器配置 <mcreference link="https://onedollarvps.com/blogs/how-to-use-mcp-in-cherry-studio" index="1">1</mcreference>
2. **启用服务**：在右上角点击按钮启用 MCP 服务 <mcreference link="https://mcp.ifuryst.com/en/client-usage/cherry-studio/" index="2">2</mcreference>
3. **查看工具**：点击 "Tools" 查看可用的 MCP 工具及其参数 <mcreference link="https://mcp.ifuryst.com/en/client-usage/cherry-studio/" index="2">2</mcreference>

### 在对话中使用

1. **开始对话**：在聊天窗口中开始新的对话
2. **工具调用**：如果支持函数调用，你会看到一个扳手图标 <mcreference link="https://onedollarvps.com/blogs/how-to-use-mcp-in-cherry-studio" index="1">1</mcreference>
3. **智能识别**：AI 会自动识别任务意图并选择合适的工具 <mcreference link="https://mcp.ifuryst.com/en/client-usage/cherry-studio/" index="2">2</mcreference>

## 📊 使用示例

### 股票数据查询

```
请帮我查询平安银行（000001）最近一个月的股价走势
```

### 市场分析

```
分析一下贵州茅台（600519）的基本面情况，包括财务指标和行业地位
```

### 港股查询

```
查询腾讯控股（00700）的最新股价和基本信息
```

### 宏观经济数据

```
获取最新的货币供应量数据和存款准备金率信息
```

## 🔍 验证配置

### 检查服务器状态

1. 在 MCP Servers 设置中查看服务器状态
2. 确保服务器显示为"运行中"或"已连接"
3. 检查是否有错误信息

### 测试功能

尝试以下测试命令：

```
请列出当前可用的股票数据工具
```

```
获取上证指数的最新信息
```

## 🛠️ 故障排除

### 常见问题

#### 1. 服务器无法启动

**症状**：MCP 服务器显示错误或无法连接

**解决方案**：
- 检查 Python 路径是否正确
- 确保 StockReport MCP 项目路径正确
- 验证依赖是否已安装：`pip install -r requirements.txt`

#### 2. 工具不可用

**症状**：在 Tools 中看不到 StockReport MCP 工具

**解决方案**：
- 重启 Cherry Studio
- 检查 MCP 服务器配置
- 查看 Cherry Studio 日志文件

#### 3. 数据获取失败

**症状**：工具调用成功但返回错误信息

**解决方案**：
- 检查网络连接
- 尝试切换数据源（hybrid → baostock 或 akshare）
- 查看 StockReport MCP 服务器日志

### 调试技巧

1. **查看日志**：检查 Cherry Studio 的日志输出
2. **测试命令**：在命令行中直接运行 MCP 服务器进行测试
3. **重启应用**：如果配置不成功，尝试重启计算机 <mcreference link="https://docs.cherry-ai.com/cherry-studio-wen-dang/en-us/advanced-basic/mcp/config" index="3">3</mcreference>

## 🌟 高级配置

### 环境变量设置

为了更好的性能和稳定性，可以添加环境变量：

```json
{
  "name": "StockReport MCP",
  "type": "STDIO",
  "command": "python",
  "args": ["mcp_server.py", "--data-source", "hybrid"],
  "cwd": "D:/stockreport-mcp",
  "env": {
    "PYTHONIOENCODING": "utf-8",
    "PYTHONUNBUFFERED": "1"
  }
}
```

### 多服务器配置

你可以同时配置多个 StockReport MCP 实例，使用不同的数据源：

```json
[
  {
    "name": "StockReport MCP (Hybrid)",
    "type": "STDIO",
    "command": "python",
    "args": ["mcp_server.py", "--data-source", "hybrid"],
    "cwd": "D:/stockreport-mcp"
  },
  {
    "name": "StockReport MCP (Baostock)",
    "type": "STDIO", 
    "command": "python",
    "args": ["mcp_server.py", "--data-source", "baostock"],
    "cwd": "D:/stockreport-mcp"
  }
]
```

## 📚 相关资源

- **Cherry Studio 官方文档**：https://docs.cherry-ai.com <mcreference link="https://mcp.ifuryst.com/en/client-usage/cherry-studio/" index="2">2</mcreference>
- **Cherry Studio GitHub**：https://github.com/cherry-ai/cherry-studio
- **MCP 协议文档**：https://modelcontextprotocol.io
- **StockReport MCP 项目**：当前项目的 README.md

## 🎉 总结

通过本指南，你应该能够成功在 Cherry Studio 中集成 StockReport MCP 服务器。这种集成使得 AI 助手能够访问丰富的中国股市数据，包括 A 股、港股以及宏观经济数据，大大增强了 AI 在金融分析领域的能力。 <mcreference link="https://onedollarvps.com/blogs/how-to-use-mcp-in-cherry-studio" index="1">1</mcreference>

如果遇到问题，请参考故障排除部分或查阅相关文档。祝你使用愉快！ 🚀