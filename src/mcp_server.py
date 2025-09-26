"""StockReport MCP Server - 中国股市数据MCP服务器

这是一个基于Model Context Protocol (MCP)的股票数据服务器，提供对中国A股、港股、美股
以及宏观经济数据的访问接口。支持多种数据源，包括Baostock、AkShare和智能混合模式。

项目来源:
本项目基于 A-SHARE-MCP 进行重大改进和扩展，主要改进包括：
- 新增 AkShare 数据源支持
- 完整的港股分析功能
- 美股数据支持
- 财务数据分析矫正
- 智能混合数据源
- 多客户端兼容性优化

主要功能:
- A股历史数据和实时行情
- 港股、美股数据支持
- 宏观经济数据
- 财务指标分析
- 技术指标计算

支持的数据源:
- Baostock: 专注A股数据，稳定可靠
- AkShare: 支持A股、港股、美股，数据覆盖面广
- Hybrid: 智能混合模式，A股使用Baostock，港股美股使用AkShare

作者: StockReport MCP Project
版本: 1.0.0
许可证: MIT License
"""

import logging
import argparse
import sys
from datetime import datetime

try:
    from mcp.server.fastmcp import FastMCP
except ImportError as e:
    print("❌ 缺少 FastMCP 依赖")
    print("💡 请运行以下命令安装依赖:")
    print("   uv sync")
    print("   或者: pip install fastmcp")
    print(f"错误详情: {e}")
    sys.exit(1)

# Import the interface and the concrete implementations
from src.data_source_interface import FinancialDataSource
from src.baostock_data_source import BaostockDataSource
from src.akshare_data_source import AkshareDataSource
from src.hybrid_data_source import HybridDataSource
from src.utils import setup_logging

# 导入各模块工具的注册函数
from src.tools.stock_market import register_stock_market_tools
from src.tools.financial_reports import register_financial_report_tools
from src.tools.indices import register_index_tools
from src.tools.market_overview import register_market_overview_tools
from src.tools.macroeconomic import register_macroeconomic_tools
from src.tools.date_utils import register_date_utils_tools
from src.tools.analysis import register_analysis_tools
from src.tools.hk_stocks import register_hk_stock_tools
from src.tools.us_stocks import register_us_stock_tools

# --- Logging Setup ---
# Call the setup function from utils
# You can control the default level here (e.g., logging.DEBUG for more verbose logs)
setup_logging(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_data_source(source_type: str) -> FinancialDataSource:
    """
    根据数据源类型创建相应的数据源实例
    
    Args:
        source_type: 数据源类型 ('baostock', 'akshare', 或 'hybrid')
    
    Returns:
        FinancialDataSource: 数据源实例
    """
    if source_type.lower() == 'baostock':
        logger.info("Using Baostock data source")
        return BaostockDataSource()
    elif source_type.lower() == 'akshare':
        logger.info("Using AkShare data source")
        return AkshareDataSource()
    elif source_type.lower() == 'hybrid':
        logger.info("Using Hybrid data source (A-shares: Baostock, Others: AkShare)")
        return HybridDataSource()
    else:
        logger.warning(f"Unknown data source type: {source_type}, defaulting to Hybrid")
        return HybridDataSource()

def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='StockReport MCP Server')
    parser.add_argument(
        '--data-source', 
        choices=['baostock', 'akshare', 'hybrid'], 
        default='hybrid',
        help='选择数据源 (默认: hybrid - A股用Baostock，港股美股用AkShare)'
    )
    parser.add_argument(
        '--log-level',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        default='INFO',
        help='设置日志级别 (默认: INFO)'
    )
    
    # 如果是通过stdio运行（MCP模式），不解析命令行参数
    if len(sys.argv) == 1:
        return argparse.Namespace(data_source='hybrid', log_level='INFO')
    
    return parser.parse_args()

# --- Parse command line arguments ---
args = parse_arguments()

# --- Update logging level ---
setup_logging(level=getattr(logging, args.log_level))

# --- Dependency Injection ---
# Create data source based on command line argument
active_data_source: FinancialDataSource = create_data_source(args.data_source)

# --- Get current date for system prompt ---
current_date = datetime.now().strftime("%Y-%m-%d")

# --- Create system instructions based on data source ---
def create_system_instructions(data_source_type: str) -> str:
    """根据数据源类型创建系统指令"""
    base_instructions = f"""今天是{current_date}。提供金融市场数据分析工具。

⚠️ 重要说明:
1. 最新交易日不一定是今天，需要从 get_latest_trading_date() 获取
2. 请始终使用 get_latest_trading_date() 工具获取实际当前最近的交易日，不要依赖训练数据中的日期认知
3. 当分析"最近"或"近期"市场情况时，必须首先调用 get_market_analysis_timeframe() 工具确定实际的分析时间范围
4. 任何涉及日期的分析必须基于工具返回的实际数据，不得使用过时或假设的日期

📊 当前数据源: {data_source_type.upper()}
"""
    
    if data_source_type.lower() == 'baostock':
        return base_instructions + """
🎯 支持的市场:
- 中国A股市场 (上海、深圳交易所)
- 主要指数数据
- 宏观经济数据

📈 主要功能:
- 股票历史K线数据
- 财务报表数据
- 指数成分股信息
- 宏观经济指标
"""
    elif data_source_type.lower() == 'akshare':
        return base_instructions + """
🌍 支持的市场:
- 中国A股市场 (上海、深圳交易所)
- 港股市场 (香港交易所)
- 美股市场 (纽约证券交易所、纳斯达克)

📈 主要功能:
- 多市场股票历史K线数据
- 股票基本信息
- 实时行情数据
- 热门股票推荐
- 股票搜索功能

💡 使用提示:
- A股代码格式: sh.600000 或 sz.000001
- 港股代码格式: hk.00700 (腾讯)
- 美股代码格式: us.AAPL (苹果)
"""
    elif data_source_type.lower() == 'hybrid':
        return base_instructions + """
🚀 智能混合数据源:
- 🇨🇳 A股市场: 使用Baostock数据源 (高质量财务数据)
- 🇭🇰 港股市场: 使用AkShare数据源 (实时行情)
- 🇺🇸 美股市场: 使用AkShare数据源 (全球市场)
- 📊 宏观数据: 使用Baostock数据源 (权威经济指标)

🎯 自动识别市场类型:
- A股代码 (sh.600000, sz.000001) → Baostock
- 港股代码 (09988, 00700) → AkShare  
- 美股代码 (AAPL, TSLA) → AkShare
- 商品期货等 → AkShare

📈 全面功能支持:
- 股票历史K线数据 (所有市场)
- 财务报表分析 (A股详细，港美股基础)
- 实时行情数据 (港股、美股)
- 指数成分股信息 (A股指数)
- 宏观经济指标 (中国市场)

💡 最佳实践:
- 系统会根据股票代码自动选择最适合的数据源
- A股分析建议使用详细的财务数据工具
- 港股美股分析侧重技术面和基本面
- 跨市场对比分析时可同时使用多个数据源
"""
    else:
        return base_instructions

# --- FastMCP App Initialization ---
app = FastMCP(
    name="financial_data_provider",
    instructions=create_system_instructions(args.data_source),
    # Specify dependencies for installation if needed (e.g., when using `mcp install`)
    # dependencies=["baostock", "akshare", "pandas"]
)

# --- 注册各模块的工具 ---
def register_tools_based_on_data_source(app, data_source: FinancialDataSource, source_type: str):
    """根据数据源类型注册相应的工具"""
    # 基础工具 - 所有数据源都支持
    register_stock_market_tools(app, data_source)
    register_date_utils_tools(app, data_source)
    register_analysis_tools(app, data_source)
    
    if source_type.lower() == 'baostock':
        # Baostock特有的工具
        register_financial_report_tools(app, data_source)
        register_index_tools(app, data_source)
        register_market_overview_tools(app, data_source)
        register_macroeconomic_tools(app, data_source)
        logger.info("Registered Baostock-specific tools")
        
    elif source_type.lower() == 'akshare':
        # AkShare特有的工具 - 包括港股和美股
        register_hk_stock_tools(app, data_source)
        register_us_stock_tools(app, data_source)
        logger.info("Registered AkShare-specific tools (including HK and US stocks)")
        
        # 部分支持的工具（如果AkShare数据源实现了相应方法）
        try:
            register_financial_report_tools(app, data_source)
            register_index_tools(app, data_source)
            register_market_overview_tools(app, data_source)
            logger.info("Registered additional tools for AkShare")
        except Exception as e:
            logger.warning(f"Some tools not available for AkShare: {e}")
            
    elif source_type.lower() == 'hybrid':
        # 混合数据源 - 注册所有工具
        # A股相关工具 (通过Baostock)
        register_financial_report_tools(app, data_source)
        register_index_tools(app, data_source)
        register_market_overview_tools(app, data_source)
        register_macroeconomic_tools(app, data_source)
        
        # 港股和美股工具 (通过AkShare)
        register_hk_stock_tools(app, data_source)
        register_us_stock_tools(app, data_source)
        
        logger.info("Registered all tools for Hybrid data source (A-shares: Baostock, Others: AkShare)")

# 注册工具
register_tools_based_on_data_source(app, active_data_source, args.data_source)

# --- Main Execution Block ---
def main():
    """主函数入口点"""
    logger.info(
        f"Starting Financial Data MCP Server via stdio... "
        f"Data Source: {args.data_source.upper()}, Today is {current_date}")
    
    # 显示启动信息
    if len(sys.argv) > 1:
        print(f"[OK] 使用数据源: {args.data_source.upper()}")
        if args.data_source.lower() == 'akshare':
            print("[INFO] 支持市场: A股、港股、美股")
        elif args.data_source.lower() == 'hybrid':
            print("[INFO] 智能混合数据源:")
            print("       - A股: Baostock (详细财务数据)")
            print("       - 港股/美股: AkShare (实时行情)")
            print("       - 宏观数据: Baostock (权威指标)")
        else:
            print("[INFO] 支持市场: A股、指数、宏观数据")
        print("=" * 50)
    
    # 启动服务器
    app.run(transport='stdio')

if __name__ == "__main__":
    main()
