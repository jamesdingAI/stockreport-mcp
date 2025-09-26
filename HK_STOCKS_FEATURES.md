# 港股分析功能文档

## 概述

本项目已成功实现了完整的港股分析功能，通过MCP (Model Context Protocol) 服务器提供港股市场的全面数据分析服务。

## 功能特性

### 1. 基础数据查询
- **股票基本信息**: 获取港股的基本信息，包括股票名称、行业分类、上市日期等
- **历史价格数据**: 支持获取港股的历史K线数据，包括开盘价、收盘价、最高价、最低价、成交量等
- **实时行情数据**: 获取港股的实时交易数据

### 2. 财务分析功能
- **盈利能力分析**: ROE、ROA、销售净利率、毛利率等关键盈利指标
- **运营能力分析**: 总资产周转率、应收账款周转率、存货周转率等运营效率指标
- **成长能力分析**: 营业收入增长率、净利润增长率、总资产增长率等成长性指标
- **偿债能力分析**: 流动比率、速动比率、资产负债率等财务健康指标
- **现金流分析**: 经营现金流、投资现金流、筹资现金流等现金流量指标
- **杜邦分析**: ROE分解分析，包括销售净利率、总资产周转率、权益乘数

### 3. 投资分析功能
- **分红数据**: 历史分红记录、股息率、派息比率等股东回报信息
- **综合分析报告**: 基于多维度数据的综合投资分析报告

### 4. 市场工具
- **股票搜索**: 根据关键词搜索港股
- **热门股票**: 获取当前热门港股列表

## 技术架构

### 数据源
- 主要使用 **AkShare** 数据源，支持港股、A股、美股多市场数据
- 备用 **Baostock** 数据源，专注于A股和宏观经济数据

### 核心模块
```
src/
├── tools/
│   └── hk_stocks.py          # 港股工具函数
├── data_source_interface.py  # 数据源接口定义
├── akshare_data_source.py    # AkShare数据源实现
├── baostock_data_source.py   # Baostock数据源实现
└── formatting/
    └── markdown_formatter.py # Markdown格式化工具
```

### MCP工具注册
所有港股分析功能都通过MCP协议注册为可调用工具：

1. `get_hk_historical_k_data` - 历史K线数据
2. `get_hk_stock_basic_info` - 股票基本信息
3. `get_hk_stock_realtime_data` - 实时行情数据
4. `get_popular_hk_stocks` - 热门股票
5. `search_hk_stocks` - 股票搜索
6. `get_hk_profit_data` - 盈利能力数据
7. `get_hk_operation_data` - 运营能力数据
8. `get_hk_growth_data` - 成长能力数据
9. `get_hk_balance_data` - 偿债能力数据
10. `get_hk_cash_flow_data` - 现金流数据
11. `get_hk_dupont_data` - 杜邦分析数据
12. `get_hk_dividend_data` - 分红数据
13. `get_hk_stock_analysis` - 综合分析报告

## 使用示例

### 启动MCP服务器
```bash
python trae_unified.py
```

### 调用示例
```python
# 获取腾讯控股基本信息
basic_info = get_hk_stock_basic_info("hk.00700")

# 获取历史价格数据
historical_data = get_hk_historical_k_data(
    code="hk.00700",
    start_date="2024-01-01",
    end_date="2024-01-31",
    frequency="d"
)

# 获取财务分析数据
profit_data = get_hk_profit_data("hk.00700", "2023", 4)
```

## 测试验证

### 测试脚本
- `test_mcp_hk_stocks.py` - MCP港股功能测试
- `test_hk_tools.py` - 港股工具功能测试
- `demo_hk_complete.py` - 港股分析功能完整演示

### 测试结果
✅ 所有核心功能测试通过
✅ MCP服务器正常运行
✅ 数据格式化正确
✅ 错误处理完善

## 数据格式

所有返回数据均采用Markdown表格格式，便于阅读和展示：

```markdown
| 指标 | 值 |
|------|-----|
| 净资产收益率(ROE) | 15.2% |
| 总资产收益率(ROA) | 8.5% |
| 销售净利率 | 22.3% |
```

## 错误处理

- **数据源错误**: 自动重试和降级处理
- **网络连接错误**: 友好的错误提示
- **数据缺失**: 明确的缺失数据说明
- **参数验证**: 输入参数格式验证

## 扩展性

### 支持的股票代码格式
- 港股: `hk.00700` (腾讯控股)
- 自动格式化: `00700` → `hk.00700`

### 可扩展功能
- 技术指标分析
- 行业比较分析
- 估值模型分析
- 风险评估模型

## 部署说明

### 环境要求
- Python 3.8+
- 依赖包: akshare, baostock, pandas, mcp

### 配置选项
- 数据源选择: AkShare (默认) / Baostock
- 数据缓存: 可配置缓存策略
- 日志级别: 可调整日志详细程度

## 维护说明

### 定期维护
- 数据源API更新检查
- 依赖包版本更新
- 错误日志监控

### 性能优化
- 数据缓存机制
- 并发请求控制
- 内存使用优化

---

**最后更新**: 2024年1月
**版本**: 1.0.0
**状态**: 生产就绪 ✅