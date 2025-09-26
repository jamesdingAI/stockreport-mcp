"""
混合数据源管理器

本模块实现了智能混合数据源，根据股票代码自动选择最适合的数据源：
- A股数据使用Baostock（数据质量高，财务数据完整）
- 港股、美股数据使用AkShare（覆盖面广，实时性好）
- 宏观经济数据优先使用Baostock（权威性强）

核心特性:
- 自动市场识别：根据股票代码格式自动判断所属市场
- 智能路由：将请求路由到最合适的数据源
- 统一接口：对外提供一致的API接口
- 错误处理：优雅处理数据源切换和异常情况

支持的市场:
- A股：上海证券交易所、深圳证券交易所
- 港股：香港联合交易所
- 美股：纽约证券交易所、纳斯达克
- 宏观数据：中国人民银行、国家统计局等

代码识别规则:
- A股：sh.600000, sz.000001 等格式
- 港股：00700, 09988, 03690 等格式
- 美股：AAPL, TSLA, MSFT 等格式

作者: StockReport MCP Project
许可证: MIT License
"""

import logging
import re
from typing import Optional, Dict, Any, List
from datetime import datetime

from .data_source_interface import FinancialDataSource
from .baostock_data_source import BaostockDataSource
from .akshare_data_source import AkshareDataSource

logger = logging.getLogger(__name__)

class HybridDataSource(FinancialDataSource):
    """
    混合数据源管理器
    - A股使用Baostock数据源
    - 港股、美股、商品等使用AkShare数据源
    """
    
    def __init__(self):
        """初始化混合数据源"""
        self.baostock_source = BaostockDataSource()
        self.akshare_source = AkshareDataSource()
        logger.info("Initialized Hybrid Data Source (A-shares: Baostock, Others: AkShare)")
    
    def _detect_market_type(self, code: str) -> str:
        """
        检测股票代码对应的市场类型
        
        Args:
            code: 股票代码
            
        Returns:
            str: 市场类型 ('a_share', 'hk_stock', 'us_stock', 'commodity', 'unknown')
        """
        if not code:
            return 'unknown'
        
        code = code.upper().strip()
        
        # A股代码模式
        # sh.600000, sz.000001, sh.000001, sz.300001 等
        if re.match(r'^(SH|SZ)\.\d{6}$', code):
            return 'a_share'
        
        # 港股代码模式
        # 09988, 00700, 03690 等 (4-5位数字)
        # 或者 09988.HK, 00700.HK 格式
        if re.match(r'^\d{4,5}(\.HK)?$', code):
            return 'hk_stock'
        
        # 美股代码模式
        # AAPL, TSLA, BABA 等 (字母组合)
        # 或者 AAPL.US 格式
        if re.match(r'^[A-Z]{1,5}(\.US)?$', code):
            return 'us_stock'
        
        # 商品期货等其他代码
        # 如果包含特定关键词或格式
        commodity_patterns = [
            r'.*GOLD.*', r'.*OIL.*', r'.*SILVER.*',  # 贵金属、原油
            r'^[A-Z]{2}\d{4}$',  # 期货合约格式
        ]
        
        for pattern in commodity_patterns:
            if re.match(pattern, code):
                return 'commodity'
        
        logger.warning(f"Unknown market type for code: {code}")
        return 'unknown'
    
    def _get_appropriate_source(self, code: str) -> FinancialDataSource:
        """
        根据股票代码获取合适的数据源
        
        Args:
            code: 股票代码
            
        Returns:
            FinancialDataSource: 对应的数据源实例
        """
        market_type = self._detect_market_type(code)
        
        if market_type == 'a_share':
            logger.debug(f"Using Baostock for A-share: {code}")
            return self.baostock_source
        else:
            logger.debug(f"Using AkShare for {market_type}: {code}")
            return self.akshare_source
    
    # 实现FinancialDataSource接口的所有方法
    
    def get_historical_k_data(self, code: str, start_date: str, end_date: str, 
                            frequency: str = 'd', adjust_flag: str = '3', 
                            fields: Optional[List[str]] = None) -> str:
        """获取历史K线数据"""
        source = self._get_appropriate_source(code)
        return source.get_historical_k_data(code, start_date, end_date, frequency, adjust_flag, fields)
    
    def get_stock_basic_info(self, code: str, fields: Optional[List[str]] = None) -> str:
        """获取股票基本信息"""
        source = self._get_appropriate_source(code)
        return source.get_stock_basic_info(code, fields)
    
    def get_dividend_data(self, code: str, year: str, year_type: str = 'report') -> str:
        """获取分红数据"""
        source = self._get_appropriate_source(code)
        return source.get_dividend_data(code, year, year_type)
    
    def get_adjust_factor_data(self, code: str, start_date: str, end_date: str) -> str:
        """获取复权因子数据"""
        source = self._get_appropriate_source(code)
        return source.get_adjust_factor_data(code, start_date, end_date)
    
    def get_latest_trading_date(self) -> str:
        """获取最新交易日期 - 使用工具层实现"""
        from datetime import datetime, timedelta
        
        # 简单实现：返回最近的工作日
        today = datetime.now()
        
        # 如果是周末，返回上周五
        if today.weekday() == 5:  # 周六
            latest_date = today - timedelta(days=1)
        elif today.weekday() == 6:  # 周日
            latest_date = today - timedelta(days=2)
        else:
            latest_date = today
        
        return latest_date.strftime('%Y-%m-%d')
    
    def get_market_analysis_timeframe(self, period: str = "recent") -> str:
        """获取市场分析时间范围 - 使用工具层实现"""
        from datetime import datetime, timedelta
        
        end_date = datetime.now()
        
        if period == "recent":
            start_date = end_date - timedelta(days=60)  # 最近2个月
        elif period == "quarter":
            start_date = end_date - timedelta(days=90)  # 最近一个季度
        elif period == "half_year":
            start_date = end_date - timedelta(days=180)  # 最近半年
        elif period == "year":
            start_date = end_date - timedelta(days=365)  # 最近一年
        else:
            start_date = end_date - timedelta(days=60)  # 默认最近2个月
        
        return f"{start_date.strftime('%Y年%m月')}-{end_date.strftime('%Y年%m月')}"
    
    def get_stock_analysis(self, code: str, analysis_type: str = "fundamental") -> str:
        """获取股票分析"""
        source = self._get_appropriate_source(code)
        return source.get_stock_analysis(code, analysis_type)
    
    # 财务数据相关方法 - 主要针对A股
    def get_profit_data(self, code: str, year: str, quarter: int) -> str:
        """获取盈利能力数据"""
        source = self._get_appropriate_source(code)
        return source.get_profit_data(code, year, quarter)
    
    def get_operation_data(self, code: str, year: str, quarter: int) -> str:
        """获取运营能力数据"""
        source = self._get_appropriate_source(code)
        return source.get_operation_data(code, year, quarter)
    
    def get_growth_data(self, code: str, year: str, quarter: int) -> str:
        """获取成长能力数据"""
        source = self._get_appropriate_source(code)
        return source.get_growth_data(code, year, quarter)
    
    def get_balance_data(self, code: str, year: str, quarter: int) -> str:
        """获取偿债能力数据"""
        source = self._get_appropriate_source(code)
        return source.get_balance_data(code, year, quarter)
    
    def get_cash_flow_data(self, code: str, year: str, quarter: int) -> str:
        """获取现金流数据"""
        source = self._get_appropriate_source(code)
        return source.get_cash_flow_data(code, year, quarter)
    
    def get_dupont_data(self, code: str, year: str, quarter: int) -> str:
        """获取杜邦分析数据"""
        source = self._get_appropriate_source(code)
        return source.get_dupont_data(code, year, quarter)
    
    # 其他方法 - 使用默认数据源或根据需要选择
    def get_performance_express_report(self, code: str, start_date: str, end_date: str) -> str:
        """获取业绩快报"""
        source = self._get_appropriate_source(code)
        return source.get_performance_express_report(code, start_date, end_date)
    
    def get_forecast_report(self, code: str, start_date: str, end_date: str) -> str:
        """获取业绩预告"""
        source = self._get_appropriate_source(code)
        return source.get_forecast_report(code, start_date, end_date)
    
    # 市场概览和宏观数据 - 使用Baostock
    def get_stock_industry(self, code: Optional[str] = None, date: Optional[str] = None) -> str:
        """获取行业分类"""
        return self.baostock_source.get_stock_industry(code, date)
    
    def get_sz50_stocks(self, date: Optional[str] = None) -> str:
        """获取上证50成分股"""
        return self.baostock_source.get_sz50_stocks(date)
    
    def get_hs300_stocks(self, date: Optional[str] = None) -> str:
        """获取沪深300成分股"""
        return self.baostock_source.get_hs300_stocks(date)
    
    def get_zz500_stocks(self, date: Optional[str] = None) -> str:
        """获取中证500成分股"""
        return self.baostock_source.get_zz500_stocks(date)
    
    def get_all_stock(self, date: Optional[str] = None) -> str:
        """获取所有股票列表"""
        return self.baostock_source.get_all_stock(date)
    
    def get_trade_dates(self, start_date: Optional[str] = None, end_date: Optional[str] = None) -> str:
        """获取交易日历"""
        return self.baostock_source.get_trade_dates(start_date, end_date)
    
    # 宏观经济数据 - 使用Baostock
    def get_deposit_rate_data(self, start_date: Optional[str] = None, end_date: Optional[str] = None) -> str:
        """获取存款利率数据"""
        return self.baostock_source.get_deposit_rate_data(start_date, end_date)
    
    def get_loan_rate_data(self, start_date: Optional[str] = None, end_date: Optional[str] = None) -> str:
        """获取贷款利率数据"""
        return self.baostock_source.get_loan_rate_data(start_date, end_date)
    
    def get_required_reserve_ratio_data(self, start_date: Optional[str] = None, 
                                      end_date: Optional[str] = None, year_type: str = "0") -> str:
        """获取存款准备金率数据"""
        return self.baostock_source.get_required_reserve_ratio_data(start_date, end_date, year_type)
    
    def get_money_supply_data_month(self, start_date: Optional[str] = None, end_date: Optional[str] = None) -> str:
        """获取月度货币供应量数据"""
        return self.baostock_source.get_money_supply_data_month(start_date, end_date)
    
    def get_money_supply_data_year(self, start_date: Optional[str] = None, end_date: Optional[str] = None) -> str:
        """获取年度货币供应量数据"""
        return self.baostock_source.get_money_supply_data_year(start_date, end_date)
    
    def get_shibor_data(self, start_date: Optional[str] = None, end_date: Optional[str] = None) -> str:
        """获取SHIBOR数据"""
        return self.baostock_source.get_shibor_data(start_date, end_date)
    
    def get_market_type_info(self, code: str) -> Dict[str, Any]:
        """
        获取股票代码的市场类型信息
        
        Args:
            code: 股票代码
            
        Returns:
            Dict: 包含市场类型和数据源信息
        """
        market_type = self._detect_market_type(code)
        data_source = "baostock" if market_type == 'a_share' else "akshare"
        
        # 映射内部市场类型到用户友好的名称
        market_type_mapping = {
            'a_share': 'A股',
            'hk_stock': '港股',
            'us_stock': '美股',
            'commodity': '商品',
            'unknown': '其他'
        }
        
        return {
            "code": code,
            "market_type": market_type_mapping.get(market_type, '其他'),
            "data_source": data_source,
            "description": {
                'a_share': 'A股市场 (上海/深圳)',
                'hk_stock': '港股市场',
                'us_stock': '美股市场',
                'commodity': '商品期货',
                'unknown': '未知市场类型'
            }.get(market_type, '未知')
        }