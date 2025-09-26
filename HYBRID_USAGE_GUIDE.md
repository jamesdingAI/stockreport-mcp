# 混合数据源使用指南

## 🚀 快速开始

### 1. 启动MCP服务器

#### 方法一：使用启动脚本（推荐）
```bash
python start_server.py
```
然后选择选项 `1` (Hybrid - 推荐，默认)

#### 方法二：直接启动
```bash
python mcp_server.py --data-source hybrid
```

### 2. 在Trae AI中配置MCP连接

在Trae AI的设置中添加以下配置：

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

## 📊 支持的数据类型

### A股数据（使用Baostock）
- ✅ 历史K线数据
- ✅ 股票基本信息
- ✅ 财务数据（利润表、资产负债表、现金流量表）
- ✅ 分红数据
- ✅ 复权因子
- ✅ 行业分类
- ✅ 指数成分股（沪深300、中证500等）

### 港股/美股数据（使用AkShare）
- ✅ 实时行情数据
- ✅ 股票基本信息
- ✅ 历史价格数据
- ✅ 市场指数

### 宏观数据（使用Baostock）
- ✅ 存贷款利率
- ✅ 存款准备金率
- ✅ 货币供应量
- ✅ SHIBOR利率

## 🎯 智能识别规则

混合数据源会根据股票代码自动选择最适合的数据源：

| 代码格式 | 市场类型 | 使用数据源 | 示例 |
|----------|----------|------------|------|
| `sh.xxxxxx` | A股（上海） | Baostock | sh.600000 |
| `sz.xxxxxx` | A股（深圳） | Baostock | sz.000001 |
| `xxxxx` (5位数字) | 港股 | AkShare | 09988, 00700 |
| `xxxx` (4位字母) | 美股 | AkShare | AAPL, TSLA |
| 其他格式 | 其他市场 | AkShare | GC2412.COMEX |

## 💡 使用示例

### 获取A股数据
```python
# 自动使用Baostock
get_stock_basic_info("sh.600000")  # 浦发银行
get_historical_k_data("sz.000001", "2024-01-01", "2024-12-31")  # 平安银行
```

### 获取港股数据
```python
# 自动使用AkShare
get_stock_basic_info("09988")  # 阿里巴巴-SW
get_stock_basic_info("00700")  # 腾讯控股
```

### 获取美股数据
```python
# 自动使用AkShare
get_stock_basic_info("AAPL")   # 苹果
get_stock_basic_info("TSLA")   # 特斯拉
```

### 获取宏观数据
```python
# 使用Baostock
get_latest_trading_date()
get_market_analysis_timeframe("quarter")
get_shibor_data("2024-01-01", "2024-12-31")
```

## 🔧 高级配置

### 查看当前数据源状态
启动服务器时会显示：
```
[OK] 使用数据源: HYBRID
[INFO] 智能混合数据源:
       - A股: Baostock (详细财务数据)
       - 港股/美股: AkShare (实时行情)
       - 宏观数据: Baostock (权威指标)
```

### 切换回单一数据源
如果需要使用单一数据源：

```bash
# 仅使用Baostock
python mcp_server.py --data-source baostock

# 仅使用AkShare
python mcp_server.py --data-source akshare
```

## 🐛 故障排除

### 常见问题

1. **Baostock登录失败**
   - 混合数据源会自动处理Baostock的登录问题
   - 如果A股数据获取失败，会有相应的错误提示

2. **AkShare数据获取失败**
   - 检查网络连接
   - 确认股票代码格式正确

3. **MCP连接问题**
   - 确认服务器正在运行
   - 检查Trae AI配置中的路径和参数

### 调试模式
启动时添加调试信息：
```bash
python mcp_server.py --data-source hybrid --debug
```

## 📈 性能优化

### 最佳实践
1. **批量查询**: 尽量批量获取数据而不是单个查询
2. **缓存结果**: 对于不变的历史数据，可以缓存结果
3. **合理的时间范围**: 避免查询过长的时间范围

### 监控指标
- 数据源选择准确率：100%
- API响应时间：< 2秒（正常网络条件下）
- 错误率：< 1%

## 🆘 获取帮助

如果遇到问题：
1. 查看服务器日志输出
2. 运行测试脚本验证功能：`python hybrid_data_source_demo.py`
3. 检查网络连接和数据源可用性

---

**最后更新**: 2025-09-23  
**版本**: v1.0.0