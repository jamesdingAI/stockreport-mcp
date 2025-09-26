<div align="center">

# 📊 stockreport-mcp 📈

<img src="https://img.shields.io/badge/A股数据-MCP%20工具-E6162D?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB2ZXJzaW9uPSIxLjEiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgd2lkdGg9IjI0IiBoZWlnaHQ9IjI0IiB2aWV3Qm94PSIwIDAgMjQgMjQiPg0KPHBhdGggZmlsbD0iI2ZmZiIgZD0iTTggMTAuOGMwIDAgMC44LTEuNSAyLjQtMS41IDEuNyAwIDIuOCAxLjUgNC44IDEuNSAxLjcgMCAyLjgtMC42IDIuOC0wLjZ2LTIuMmMwIDAtMS4xIDEuMS0yLjggMS4xLTIgMC0zLjEtMS41LTQuOC0xLjUtMS42IDAtMi40IDAuOS0yLjQgMC45djIuM3pNOCAxNC44YzAgMCAwLjgtMS41IDIuNC0xLjUgMS43IDAgMi44IDEuNSA0LjggMS41IDEuNyAwIDIuOC0wLjYgMi44LTAuNnYtMi4yYzAgMC0xLjEgMS4xLTIuOCAxLjEtMiAwLTMuMS0xLjUtNC44LTEuNS0xLjYgMC0yLjQgMC45LTIuNCAwLjl2Mi4zeiI+PC9wYXRoPg0KPC9zdmc+">

[![License](https://img.shields.io/badge/License-MIT-green.svg?style=flat-square&logo=opensourceinitiative)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg?style=flat-square&logo=python&logoColor=white)](https://www.python.org/downloads/)
[![Package Manager](https://img.shields.io/badge/uv-package%20manager-5A45FF?style=flat-square&logo=data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTEyIDEuNUwxIDEyLjVIMjNMMTIgMS41WiIgZmlsbD0id2hpdGUiLz4KPHBhdGggZD0iTTEyIDIyLjVMMSAxMS41SDIzTDEyIDIyLjVaIiBmaWxsPSJ3aGl0ZSIvPgo8L3N2Zz4K)](https://github.com/astral-sh/uv)
[![MCP](https://img.shields.io/badge/MCP-Protocol-FF6B00?style=flat-square&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgd2lkdGg9IjI0IiBoZWlnaHQ9IjI0Ij48cGF0aCBkPSJNMTIgMkM2LjQ4NiAyIDIgNi40ODYgMiAxMnM0LjQ4NiAxMCAxMCAxMHMxMC00LjQ4NiAxMC0xMFMxNy41MTQgMiAxMiAyem0tMSAxNHY1LjI1QTguMDA4IDguMDA4IDAgMCAxIDQuNzUgMTZ6bTIgMGg2LjI1QTguMDA4IDguMDA4IDAgMCAxIDEzIDE2em0xLTJWOWg1LjI1QTguMDIgOC4wMiAwIDAAxIDE0IDE0em0tMiAwSDYuNzVBOC4wMiA4LjAyIDAgMDEgMTEgMTR6bTAtNlY0Ljc1QTguMDA4IDguMDA4IDAgMCAxIDE5LjI1IDh6TTEwIDh2NUg0Ljc1QTguMDA3IDguMDA3IDAgMCAxIDEwIDh6IiBmaWxsPSJ3aGl0ZSIvPjwvc3ZnPg==)](https://github.com/model-context-protocol/mcp-spec)

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=12,15,20,24&height=200&section=header&text=A%20股%20MCP&fontSize=80&fontAlignY=35&desc=基于%20Model%20Context%20Protocol%20(MCP)&descAlignY=60&animation=fadeIn" />

</div>
StockReport MCP。

本项目是一个基于 Model Context Protocol (MCP) 的多市场股票数据服务器，支持 A 股、港股、美股等多个市场的数据查询。它提供股票基本信息、历史 K 线数据、财务指标、宏观经济数据等多种查询功能，理论上来说，可以回答有关股票市场的任何问题，无论是针对大盘还是特定股票。

## 📈 项目来源与改进

本项目基于 **A-SHARE-MCP** 项目进行了重大改进和扩展：

### 🔄 主要改进内容
- **🌐 新增 AkShare 数据源**：扩展了数据源支持，提供更丰富的市场数据
- **🇭🇰 港股分析功能**：完整支持港股市场数据查询和分析
- **🇺🇸 美股数据支持**：新增美股市场数据获取能力
- **📊 财务数据分析矫正**：修复和优化了财务指标计算逻辑
- **🔀 智能混合数据源**：实现多数据源智能切换，提供最优数据质量
- **📚 完善文档体系**：提供详细的配置指南和故障排除文档
- **🔧 多客户端兼容性**：支持 Trae AI、Claude Desktop、Cherry Studio 等多种 MCP 客户端

### 🎯 核心优势
- **多市场覆盖**：A股、港股、美股一站式数据服务
- **数据源冗余**：多数据源保证数据可靠性和完整性
- **智能路由**：根据查询类型自动选择最佳数据源
- **易于部署**：完整的安装和配置指南

## 数据源支持

本项目支持三种数据源模式，可在启动时选择：

- **Hybrid (推荐)**: 智能混合数据源，自动根据股票代码选择最佳数据源
  - **A股数据**: 使用 Baostock 提供详细的财务数据、历史K线、分红信息等
  - **港股数据**: 使用 AkShare 提供实时行情、历史数据、基本信息等
  - **美股数据**: 使用 AkShare 提供多市场数据支持
  - **宏观数据**: 使用 Baostock 提供权威的宏观经济指标
  - **智能切换**: 根据股票代码前缀自动选择最适合的数据源
- **Baostock**: 专注于 A 股市场数据，提供完整的财务指标和宏观经济数据
- **AkShare**: 支持 A 股、港股、美股等多市场数据，提供更广泛的市场覆盖

> **推荐使用 Hybrid 模式**：该模式结合了两个数据源的优势，为不同市场提供最优质的数据服务。

<div align="center">
<img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png" width="100%">
</div>

## 项目结构

```
stockreport-mcp/
│
├── mcp_server.py           # 主MCP服务器入口文件
├── simple_mcp_server.py    # 简化版MCP服务器
├── start_server.py         # 交互式启动脚本
├── start_server.bat        # Windows批处理启动脚本
├── system_start.py         # 系统启动脚本
├── pyproject.toml          # 项目依赖配置
├── uv.lock                 # UV包管理器锁定文件
├── README.md               # 项目说明文档
├── LICENSE                 # MIT许可证文件
│
├── 文档文件/                # 项目文档
│   ├── HK_STOCKS_FEATURES.md        # 港股功能说明
│   ├── HYBRID_DATA_SOURCE_SUMMARY.md # 混合数据源总结
│   ├── HYBRID_USAGE_GUIDE.md        # 混合数据源使用指南
│   ├── STARTUP_GUIDE.md             # 启动指南
│   ├── TRAE_CONFIG_FIX.md           # Trae配置修复指南
│   ├── TRAE_SETUP.md                # Trae设置指南
│   └── TRAE_UNIVERSAL_CONFIG.md     # Trae通用配置
│
├── src/                    # 源代码目录
│   ├── __init__.py
│   ├── baostock_data_source.py   # Baostock数据源实现
│   ├── akshare_data_source.py    # AkShare数据源实现
│   ├── hybrid_data_source.py     # 混合数据源实现
│   ├── data_source_interface.py  # 数据源接口定义
│   ├── utils.py                  # 通用工具函数
│   │
│   ├── formatting/         # 数据格式化模块
│   │   ├── __init__.py
│   │   └── markdown_formatter.py  # Markdown格式化工具
│   │
│   └── tools/              # MCP工具模块
│       ├── __init__.py
│       ├── base.py                # 基础工具函数
│       ├── stock_market.py        # 股票市场数据工具
│       ├── financial_reports.py   # 财务报表工具
│       ├── indices.py             # 指数相关工具
│       ├── market_overview.py     # 市场概览工具
│       ├── macroeconomic.py       # 宏观经济数据工具
│       ├── date_utils.py          # 日期工具
│       ├── analysis.py            # 分析工具
│       ├── hk_stocks.py           # 港股数据工具
│       └── us_stocks.py           # 美股数据工具
│
├── resource/               # 资源文件
│   └── img/                # 图片资源
│       ├── img_1.png       # CherryStudio配置示例
│       ├── img_2.png       # CherryStudio配置示例
│       ├── ali.png         # 支付宝收款码
│       ├── gzh_code.jpg    # 公众号二维码
│       └── planet.jpg      # 星球图片
│
└── 批处理脚本/              # Windows批处理脚本
    ├── start_mcp_server.bat     # 启动MCP服务器
    ├── start_mcp_system.bat     # 启动MCP系统
    └── reset_env.bat            # 重置环境
```

<div align="center">
<img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png" width="100%">
</div>

## 功能特点

<div align="center">
<table>
  <tr>
    <td align="center"><img src="https://img.icons8.com/fluency/48/null/stocks-growth.png" width="30px"/><br><b>股票基础数据</b></td>
    <td align="center"><img src="https://img.icons8.com/fluency/48/null/line-chart.png" width="30px"/><br><b>历史行情数据</b></td>
    <td align="center"><img src="https://img.icons8.com/fluency/48/null/bonds.png" width="30px"/><br><b>财务报表数据</b></td>
  </tr>
  <tr>
    <td align="center"><img src="https://img.icons8.com/fluency/48/null/economic-improvement.png" width="30px"/><br><b>宏观经济数据</b></td>
    <td align="center"><img src="https://img.icons8.com/fluency/48/null/statistics.png" width="30px"/><br><b>指数成分股</b></td>
    <td align="center"><img src="https://img.icons8.com/fluency/48/null/fine-print.png" width="30px"/><br><b>数据分析报告</b></td>
  </tr>
  <tr>
    <td align="center"><img src="https://img.icons8.com/fluency/48/null/globe.png" width="30px"/><br><b>多市场支持</b></td>
    <td align="center"><img src="https://img.icons8.com/fluency/48/null/switch.png" width="30px"/><br><b>数据源切换</b></td>
    <td align="center"><img src="https://img.icons8.com/fluency/48/null/test-passed.png" width="30px"/><br><b>功能测试</b></td>
  </tr>
</table>
</div>

### 支持的市场

- **A股市场**: 上海证券交易所、深圳证券交易所
- **港股市场**: 香港联合交易所 (使用AkShare数据源)
- **美股市场**: 纽约证券交易所、纳斯达克 (使用AkShare数据源)

## 先决条件

1. **Python 环境**: Python 3.10+
2. **依赖管理**: 使用 `uv` 包管理器安装依赖
3. **数据来源**: 
   - **Baostock**: 专注A股数据，无需付费账号。在此感谢 Baostock。
   - **AkShare**: 支持多市场数据，无需付费账号。在此感谢 AkShare。
4. 提醒：本项目于 Windows 环境下开发。

## 快速启动

### 方式一：交互式启动 (推荐)

```bash
# 运行交互式启动脚本
python start_server.py
```

或者在Windows上双击运行：
```bash
start_server.bat
```

### 方式二：命令行启动

```bash
# 使用混合数据源 (推荐，默认)
python mcp_server.py --data-source hybrid

# 使用Baostock数据源 (仅A股)
python mcp_server.py --data-source baostock

# 使用AkShare数据源 (多市场)
python mcp_server.py --data-source akshare

# 设置日志级别
python mcp_server.py --data-source hybrid --log-level DEBUG

# 使用简化版服务器
python simple_mcp_server.py
```

## 数据更新时间

> 以下是 Baostock 官方数据更新时间，请注意查询最新数据时的时间点 [Baostock 官网](http://baostock.com/baostock/index.php/%E9%A6%96%E9%A1%B5)

**每日数据更新时间：**

- 当前交易日 17:30，完成日 K 线数据入库
- 当前交易日 18:00，完成复权因子数据入库
- 第二自然日 11:00，完成分钟 K 线数据入库
- 第二自然日 1:30，完成前交易日"其它财务报告数据"入库
- 周六 17:30，完成周线数据入库

**每周数据更新时间：**

- 每周一下午，完成上证 50 成份股、沪深 300 成份股、中证 500 成份股信息数据入库

> 所以说，在交易日的当天，如果是在 17:30 之前询问当天的数据，是无法获取到的。

## 安装环境

在项目根目录下执行：

要启动 StockReport MCP 服务器，请按照以下步骤操作：

```bash
# 1. 创建虚拟环境（仅创建，不会安装任何包）
uv venv

# 2. 激活虚拟环境
# Windows
.venv\Scripts\activate
# macOS/Linux
# source .venv/bin/activate

# 3. 安装所有依赖（必须在激活的虚拟环境中执行）
uv sync
```

## 使用：在 MCP 客户端中配置服务器

在支持 MCP 的客户端（如 VS Code 插件、CherryStudio 等）中，你需要配置如何启动此服务器。 **推荐使用 `uv`**。

### 方法一：使用 JSON 配置的 IDE (例如 Cursor、VSCode、Trae 等)

对于需要编辑 JSON 文件来配置 MCP 服务器的客户端，你需要找到对应的能配置 MCP 的地方（各个 IDE 和桌面 MCP Client 可能都不一样），并在 `mcpServers` 对象中添加一个新的条目。

**JSON 配置示例 (请将路径替换为你的实际绝对路径):**

```json
{
  "mcpServers": {
    "stockreport-mcp": {
      "command": "uv", // 或者 uv.exe 的绝对路径, 例如: "C:\\path\\to\\uv.exe"
      "args": [
        "--directory",
        "C:\\Users\\YourName\\Projects\\stockreport_mcp", // 替换为你的项目根目录绝对路径，不一定是C盘，按实际的填写
        "run",
        "python",
        "mcp_server.py"
      ],
      "transport": "stdio"
      // "workingDirectory": "C:\\Users\\YourName\\Projects\\stockreport_mcp", // 使用 uv --directory 后，此项可能不再必需，但建议保留作为备用
    }
    // ... other servers ...
  }
}
```

**注意事项:**

- **`command`**: 确保填写的 `uv` 命令或 `uv.exe` 的绝对路径是客户端可以访问和执行的。
- **`args`**: 确保参数列表完整且顺序正确。
- **路径转义**: 路径需要写成双反斜杠 `\\`。
  > 这是 Windows 系统特有的情况。如果是在 macOS 或 Linux 系统中，路径使用正斜杠/作为目录分隔符，就不需要这种转义处理。
- **`workingDirectory`**: 虽然 `uv --directory` 应该能解决工作目录问题，但如果客户端仍然报错 `ModuleNotFoundError`，可以尝试在客户端配置中明确设置此项为项目根目录的绝对路径。

### 方法二：使用 CherryStudio

在 CherryStudio 的 MCP 服务器配置界面中，按如下方式填写：

- **名称**: `stockreport-mcp` (或自定义)
- **描述**: `本地 StockReport MCP 服务器` (或自定义)
- **类型**: 选择 **标准输入/输出 (stdio)**
- **命令**: `uv` (或者填系统中绝对路径下 uv.exe)
- **包管理源**: 默认
- **参数**:

  1. 第一个参数填: `--directory`
  2. 第二个参数填: `C:\\Users\\YourName\\Projects\\stockreport_mcp`
  3. 第三个参数填: `run`
  4. 第四个参数填: `python`
  5. 第五个参数填: `mcp_server.py`

  - _确保所有参数按下回车转行隔开的，否则报错（是不是手把手教学了？）_

- **环境变量**: (通常留空)

> Tricks（必看）:
> 有时候在 Cherrystudio 填写好参数后，点击右上方的开关按钮，会发现没任何反应，此时只要随便点击左侧目录任一按钮，跳出 mcp 设置界面，然后再回到 mcp 设置界面，就会发现 mcp 已经闪绿灯配置成功了。

**CherryStudio 使用示例:**
理论上来说，你可以问有关股票市场的任何问题 :)

![CherryStudio配置示例1](resource/img/img_1.png)

![CherryStudio配置示例2](resource/img/img_2.png)

**重要提示:**

- 确保**命令**字段中的 `uv` 或其绝对路径有效且可执行。
- 确保**参数**字段按顺序正确填写了五个参数。

## 工具列表

该 MCP 服务器提供以下工具：

<div align="center">
  <details>
    <summary><b>🔍 展开查看全部工具</b></summary>
    <br>
    <table>
      <tr>
        <th>🏛️ A股市场数据</th>
        <th>📊 A股财务报表</th>
        <th>🔎 市场概览数据</th>
      </tr>
      <tr valign="top">
        <td>
          <ul>
            <li><code>get_historical_k_data</code></li>
            <li><code>get_stock_basic_info</code></li>
            <li><code>get_dividend_data</code></li>
            <li><code>get_adjust_factor_data</code></li>
          </ul>
        </td>
        <td>
          <ul>
            <li><code>get_profit_data</code></li>
            <li><code>get_operation_data</code></li>
            <li><code>get_growth_data</code></li>
            <li><code>get_balance_data</code></li>
            <li><code>get_cash_flow_data</code></li>
            <li><code>get_dupont_data</code></li>
          </ul>
        </td>
        <td>
          <ul>
            <li><code>get_trade_dates</code></li>
            <li><code>get_all_stock</code></li>
          </ul>
        </td>
      </tr>
      <tr>
        <th>📈 指数相关数据</th>
        <th>🌐 宏观经济数据</th>
        <th>⏰ 日期工具 & 分析</th>
      </tr>
      <tr valign="top">
        <td>
          <ul>
            <li><code>get_stock_industry</code></li>
            <li><code>get_sz50_stocks</code></li>
            <li><code>get_hs300_stocks</code></li>
            <li><code>get_zz500_stocks</code></li>
          </ul>
        </td>
        <td>
          <ul>
            <li><code>get_deposit_rate_data</code></li>
            <li><code>get_loan_rate_data</code></li>
            <li><code>get_required_reserve_ratio_data</code></li>
            <li><code>get_money_supply_data_month</code></li>
            <li><code>get_money_supply_data_year</code></li>
            <li><code>get_shibor_data</code></li>
          </ul>
        </td>
        <td>
          <ul>
            <li><code>get_latest_trading_date</code></li>
            <li><code>get_market_analysis_timeframe</code></li>
            <li><code>get_stock_analysis</code></li>
          </ul>
        </td>
      </tr>
      <tr>
        <th>🇭🇰 港股市场数据</th>
        <th>🇭🇰 港股财务数据</th>
        <th>🇺🇸 美股市场数据</th>
      </tr>
      <tr valign="top">
        <td>
          <ul>
            <li><code>get_hk_historical_k_data</code></li>
            <li><code>get_hk_stock_basic_info</code></li>
            <li><code>get_hk_stock_realtime_data</code></li>
            <li><code>get_popular_hk_stocks</code></li>
            <li><code>search_hk_stocks</code></li>
            <li><code>get_hk_dividend_data</code></li>
          </ul>
        </td>
        <td>
          <ul>
            <li><code>get_hk_profit_data</code></li>
            <li><code>get_hk_operation_data</code></li>
            <li><code>get_hk_growth_data</code></li>
            <li><code>get_hk_balance_data</code></li>
            <li><code>get_hk_cash_flow_data</code></li>
            <li><code>get_hk_dupont_data</code></li>
            <li><code>get_hk_stock_analysis</code></li>
          </ul>
        </td>
        <td>
          <ul>
            <li><code>get_us_historical_k_data</code></li>
            <li><code>get_us_stock_basic_info</code></li>
            <li><code>get_us_stock_realtime_data</code></li>
            <li><code>get_popular_us_stocks</code></li>
            <li><code>search_us_stocks</code></li>
            <li><code>get_us_stock_analysis</code></li>
          </ul>
        </td>
      </tr>
    </table>
  </details>
</div>

## 贡献指南

欢迎提交 Issue 或 Pull Request 来帮助改进项目。贡献前请先查看现有 Issue 和文档。

## ☕️ 请作者喝杯咖啡

如果这个项目对你有帮助，欢迎请我喝杯咖啡 ❤️

<img src="resource/img/ali.png" alt="支付宝收款码" width="300"/>

## 许可证

本项目采用 MIT 许可证 - 详情请查看 LICENSE 文件

<div align="center">
<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=12,15,20,24&section=footer&height=100&animation=fadeIn" />
</div>
