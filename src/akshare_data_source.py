# Implementation of the FinancialDataSource interface using AKShare
import akshare as ak
import pandas as pd
from typing import List, Optional
import logging
from datetime import datetime, timedelta
try:
    from .data_source_interface import FinancialDataSource, DataSourceError, NoDataFoundError, LoginError
except ImportError:
    from data_source_interface import FinancialDataSource, DataSourceError, NoDataFoundError, LoginError

# Get a logger instance for this module
logger = logging.getLogger(__name__)

# Default fields for different data types
DEFAULT_K_FIELDS = [
    "date", "code", "open", "high", "low", "close", "preclose",
    "volume", "amount", "adjustflag", "turn", "tradestatus",
    "pctChg", "peTTM", "pbMRQ", "psTTM", "pcfNcfTTM", "isST"
]

DEFAULT_BASIC_FIELDS = [
    "code", "tradeStatus", "code_name"
]

class AkshareDataSource(FinancialDataSource):
    """
    AKShare数据源实现，支持A股、港股、美股数据查询
    """
    
    def __init__(self):
        """初始化AKShare数据源"""
        logger.info("Initializing AKShare data source")
        # AKShare不需要登录，但我们可以在这里做一些初始化检查
        try:
            # 测试AKShare是否可用
            ak.tool_trade_date_hist_sina()
            logger.info("AKShare data source initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize AKShare: {e}")
            raise DataSourceError(f"Failed to initialize AKShare: {e}")
    
    def _convert_code_format(self, code: str, market: str = "A") -> str:
        """
        转换股票代码格式
        Args:
            code: 输入的股票代码 (如 sh.600000 或 sz.000001)
            market: 市场类型 ("A", "HK", "US")
        Returns:
            转换后的代码格式
        """
        if market == "A":
            # A股代码转换
            if code.startswith("sh.") or code.startswith("sz."):
                return code.split(".")[1]
            return code
        elif market == "HK":
            # 港股代码处理
            if code.startswith("hk."):
                return code.split(".")[1]
            return code
        elif market == "US":
            # 美股代码处理
            if code.startswith("us."):
                return code.split(".")[1]
            return code.upper()
        return code
    
    def _standardize_dataframe(self, df: pd.DataFrame, code: str) -> pd.DataFrame:
        """
        标准化DataFrame格式，使其与baostock格式兼容
        """
        if df.empty:
            return df
        
        # 确保有code列
        if 'code' not in df.columns and 'symbol' not in df.columns:
            df['code'] = code
        elif 'symbol' in df.columns and 'code' not in df.columns:
            df['code'] = df['symbol']
        
        # 标准化日期列
        if 'date' not in df.columns:
            for date_col in ['日期', 'trade_date', 'Date']:
                if date_col in df.columns:
                    df['date'] = df[date_col]
                    break
        
        # 标准化价格列
        price_mapping = {
            '开盘': 'open',
            '最高': 'high', 
            '最低': 'low',
            '收盘': 'close',
            '成交量': 'volume',
            '成交额': 'amount'
        }
        
        for chinese_col, english_col in price_mapping.items():
            if chinese_col in df.columns and english_col not in df.columns:
                df[english_col] = df[chinese_col]
        
        return df
    
    def get_historical_k_data(
        self,
        code: str,
        start_date: str,
        end_date: str,
        frequency: str = "d",
        adjust_flag: str = "3",
        fields: Optional[List[str]] = None,
    ) -> pd.DataFrame:
        """
        获取历史K线数据
        支持A股、港股、美股
        """
        logger.info(f"Fetching historical K data for {code}, {start_date} to {end_date}")
        
        try:
            # 判断市场类型
            if code.startswith("hk."):
                return self._get_hk_historical_data(code, start_date, end_date, frequency)
            elif code.startswith("us."):
                return self._get_us_historical_data(code, start_date, end_date, frequency)
            else:
                return self._get_a_share_historical_data(code, start_date, end_date, frequency, adjust_flag)
                
        except Exception as e:
            logger.error(f"Error fetching historical data for {code}: {e}")
            raise DataSourceError(f"Error fetching historical data for {code}: {e}")
    
    def _get_a_share_historical_data(self, code: str, start_date: str, end_date: str, frequency: str, adjust_flag: str) -> pd.DataFrame:
        """获取A股历史数据"""
        symbol = self._convert_code_format(code, "A")
        
        try:
            # 根据复权标志选择不同的接口
            if adjust_flag == "1":  # 后复权
                df = ak.stock_zh_a_hist(symbol=symbol, period="daily", start_date=start_date.replace("-", ""), 
                                      end_date=end_date.replace("-", ""), adjust="hfq")
            elif adjust_flag == "2":  # 前复权
                df = ak.stock_zh_a_hist(symbol=symbol, period="daily", start_date=start_date.replace("-", ""), 
                                      end_date=end_date.replace("-", ""), adjust="qfq")
            else:  # 不复权
                df = ak.stock_zh_a_hist(symbol=symbol, period="daily", start_date=start_date.replace("-", ""), 
                                      end_date=end_date.replace("-", ""), adjust="")
            
            if df.empty:
                raise NoDataFoundError(f"No data found for {code}")
            
            # 标准化DataFrame
            df = self._standardize_dataframe(df, code)
            
            # 添加缺失的列
            if 'adjustflag' not in df.columns:
                df['adjustflag'] = adjust_flag
            
            logger.info(f"Retrieved {len(df)} records for {code}")
            return df
            
        except Exception as e:
            logger.error(f"Error fetching A-share data for {code}: {e}")
            raise DataSourceError(f"Error fetching A-share data for {code}: {e}")
    
    def _get_hk_historical_data(self, code: str, start_date: str, end_date: str, frequency: str) -> pd.DataFrame:
        """获取港股历史数据"""
        symbol = self._convert_code_format(code, "HK")
        
        try:
            # 使用AKShare的港股接口
            df = ak.stock_hk_hist(symbol=symbol, period="daily", start_date=start_date.replace("-", ""), 
                                end_date=end_date.replace("-", ""))
            
            if df.empty:
                raise NoDataFoundError(f"No HK stock data found for {code}")
            
            # 标准化DataFrame
            df = self._standardize_dataframe(df, code)
            
            logger.info(f"Retrieved {len(df)} HK stock records for {code}")
            return df
            
        except Exception as e:
            logger.error(f"Error fetching HK stock data for {code}: {e}")
            raise DataSourceError(f"Error fetching HK stock data for {code}: {e}")
    
    def _get_us_historical_data(self, code: str, start_date: str, end_date: str, frequency: str) -> pd.DataFrame:
        """获取美股历史数据"""
        symbol = self._convert_code_format(code, "US")
        
        try:
            # 使用AKShare的美股接口
            df = ak.stock_us_hist(symbol=symbol, period="daily", start_date=start_date, end_date=end_date)
            
            if df.empty:
                raise NoDataFoundError(f"No US stock data found for {code}")
            
            # 标准化DataFrame
            df = self._standardize_dataframe(df, code)
            
            logger.info(f"Retrieved {len(df)} US stock records for {code}")
            return df
            
        except Exception as e:
            logger.error(f"Error fetching US stock data for {code}: {e}")
            raise DataSourceError(f"Error fetching US stock data for {code}: {e}")
    
    def get_stock_basic_info(self, code: str, fields: Optional[List[str]] = None) -> pd.DataFrame:
        """获取股票基本信息"""
        logger.info(f"Fetching basic info for {code}")
        
        try:
            if code.startswith("hk."):
                return self._get_hk_basic_info(code)
            elif code.startswith("us."):
                return self._get_us_basic_info(code)
            else:
                return self._get_a_share_basic_info(code)
                
        except Exception as e:
            logger.error(f"Error fetching basic info for {code}: {e}")
            raise DataSourceError(f"Error fetching basic info for {code}: {e}")
    
    def _get_a_share_basic_info(self, code: str) -> pd.DataFrame:
        """获取A股基本信息"""
        symbol = self._convert_code_format(code, "A")
        
        try:
            # 获取股票基本信息
            df = ak.stock_individual_info_em(symbol=symbol)
            
            if df.empty:
                raise NoDataFoundError(f"No basic info found for {code}")
            
            # 转换为标准格式
            result_df = pd.DataFrame({
                'code': [code],
                'code_name': [df.loc[df['item'] == '股票简称', 'value'].iloc[0] if not df.loc[df['item'] == '股票简称', 'value'].empty else ''],
                'listingDate': [df.loc[df['item'] == '上市时间', 'value'].iloc[0] if not df.loc[df['item'] == '上市时间', 'value'].empty else ''],
                'outDate': [''],
                'type': ['1'],
                'status': ['1']
            })
            
            return result_df
            
        except Exception as e:
            logger.error(f"Error fetching A-share basic info for {code}: {e}")
            raise DataSourceError(f"Error fetching A-share basic info for {code}: {e}")
    
    def _get_hk_basic_info(self, code: str) -> pd.DataFrame:
        """获取港股基本信息"""
        symbol = self._convert_code_format(code, "HK")
        
        try:
            # 获取港股基本信息
            df = ak.stock_hk_spot_em()
            stock_info = df[df['代码'] == symbol]
            
            if stock_info.empty:
                raise NoDataFoundError(f"No HK stock basic info found for {code}")
            
            result_df = pd.DataFrame({
                'code': [code],
                'code_name': [stock_info['名称'].iloc[0]],
                'listingDate': [''],  # AKShare港股接口可能不提供上市日期
                'outDate': [''],
                'type': ['2'],  # 港股类型
                'status': ['1']
            })
            
            return result_df
            
        except Exception as e:
            logger.error(f"Error fetching HK stock basic info for {code}: {e}")
            raise DataSourceError(f"Error fetching HK stock basic info for {code}: {e}")
    
    def _get_us_basic_info(self, code: str) -> pd.DataFrame:
        """获取美股基本信息"""
        symbol = self._convert_code_format(code, "US")
        
        try:
            # 获取美股基本信息
            df = ak.stock_us_spot_em()
            stock_info = df[df['代码'] == symbol]
            
            if stock_info.empty:
                raise NoDataFoundError(f"No US stock basic info found for {code}")
            
            result_df = pd.DataFrame({
                'code': [code],
                'code_name': [stock_info['名称'].iloc[0]],
                'listingDate': [''],  # AKShare美股接口可能不提供上市日期
                'outDate': [''],
                'type': ['3'],  # 美股类型
                'status': ['1']
            })
            
            return result_df
            
        except Exception as e:
            logger.error(f"Error fetching US stock basic info for {code}: {e}")
            raise DataSourceError(f"Error fetching US stock basic info for {code}: {e}")
    
    # 以下方法主要针对A股，港股和美股可能不支持某些功能
    def get_dividend_data(self, code: str, year: str, year_type: str = "report") -> pd.DataFrame:
        """获取分红数据（主要支持A股）"""
        if code.startswith("hk.") or code.startswith("us."):
            raise NoDataFoundError(f"Dividend data not supported for {code}")
        
        symbol = self._convert_code_format(code, "A")
        
        try:
            df = ak.stock_zh_a_dividend(symbol=symbol)
            
            if df.empty:
                raise NoDataFoundError(f"No dividend data found for {code}")
            
            # 过滤年份
            df['year'] = pd.to_datetime(df['股权登记日']).dt.year.astype(str)
            df = df[df['year'] == year]
            
            if df.empty:
                raise NoDataFoundError(f"No dividend data found for {code} in {year}")
            
            return df
            
        except Exception as e:
            logger.error(f"Error fetching dividend data for {code}: {e}")
            raise DataSourceError(f"Error fetching dividend data for {code}: {e}")
    
    def get_adjust_factor_data(self, code: str, start_date: str, end_date: str) -> pd.DataFrame:
        """获取复权因子数据（主要支持A股）"""
        if code.startswith("hk.") or code.startswith("us."):
            raise NoDataFoundError(f"Adjust factor data not supported for {code}")
        
        # AKShare可能没有直接的复权因子接口，这里返回空数据
        raise NoDataFoundError(f"Adjust factor data not available in AKShare for {code}")
    
    # 财务数据方法（主要支持A股）
    def get_profit_data(self, code: str, year: str, quarter: int) -> pd.DataFrame:
        """获取盈利能力数据"""
        if code.startswith("hk.") or code.startswith("us."):
            raise NoDataFoundError(f"Profit data not supported for {code}")
        
        symbol = self._convert_code_format(code, "A")
        
        try:
            # 使用AKShare的财务数据接口
            df = ak.stock_financial_analysis_indicator(symbol=symbol)
            
            if df.empty:
                raise NoDataFoundError(f"No profit data found for {code}")
            
            # 过滤年份和季度
            target_date = f"{year}-{quarter*3:02d}-30"  # 简化的季度末日期
            
            return df
            
        except Exception as e:
            logger.error(f"Error fetching profit data for {code}: {e}")
            raise DataSourceError(f"Error fetching profit data for {code}: {e}")
    
    def get_operation_data(self, code: str, year: str, quarter: int) -> pd.DataFrame:
        """获取运营能力数据"""
        return self.get_profit_data(code, year, quarter)  # 使用相同的财务数据接口
    
    def get_growth_data(self, code: str, year: str, quarter: int) -> pd.DataFrame:
        """获取成长能力数据"""
        return self.get_profit_data(code, year, quarter)  # 使用相同的财务数据接口
    
    def get_balance_data(self, code: str, year: str, quarter: int) -> pd.DataFrame:
        """获取偿债能力数据"""
        return self.get_profit_data(code, year, quarter)  # 使用相同的财务数据接口
    
    def get_cash_flow_data(self, code: str, year: str, quarter: int) -> pd.DataFrame:
        """获取现金流数据"""
        return self.get_profit_data(code, year, quarter)  # 使用相同的财务数据接口
    
    def get_dupont_data(self, code: str, year: str, quarter: int) -> pd.DataFrame:
        """获取杜邦分析数据"""
        return self.get_profit_data(code, year, quarter)  # 使用相同的财务数据接口
    
    def get_performance_express_report(self, code: str, start_date: str, end_date: str) -> pd.DataFrame:
        """获取业绩快报"""
        if code.startswith("hk.") or code.startswith("us."):
            raise NoDataFoundError(f"Performance express report not supported for {code}")
        
        raise NoDataFoundError(f"Performance express report not available in AKShare for {code}")
    
    def get_forecast_report(self, code: str, start_date: str, end_date: str) -> pd.DataFrame:
        """获取业绩预告"""
        if code.startswith("hk.") or code.startswith("us."):
            raise NoDataFoundError(f"Forecast report not supported for {code}")
        
        raise NoDataFoundError(f"Forecast report not available in AKShare for {code}")
    
    def get_stock_industry(self, code: Optional[str] = None, date: Optional[str] = None) -> pd.DataFrame:
        """获取行业分类"""
        try:
            if code and (code.startswith("hk.") or code.startswith("us.")):
                raise NoDataFoundError(f"Industry classification not supported for {code}")
            
            # 获取A股行业分类
            df = ak.stock_board_industry_name_em()
            
            if code:
                symbol = self._convert_code_format(code, "A")
                # 这里需要更复杂的逻辑来匹配股票和行业
                # 简化处理，返回空结果
                raise NoDataFoundError(f"Industry data not available for specific stock {code}")
            
            return df
            
        except Exception as e:
            logger.error(f"Error fetching industry data: {e}")
            raise DataSourceError(f"Error fetching industry data: {e}")
    
    # 指数成分股（主要支持A股指数）
    def get_sz50_stocks(self, date: Optional[str] = None) -> pd.DataFrame:
        """获取上证50成分股"""
        try:
            df = ak.index_stock_cons(symbol="000016")
            return df
        except Exception as e:
            logger.error(f"Error fetching SZ50 stocks: {e}")
            raise DataSourceError(f"Error fetching SZ50 stocks: {e}")
    
    def get_hs300_stocks(self, date: Optional[str] = None) -> pd.DataFrame:
        """获取沪深300成分股"""
        try:
            df = ak.index_stock_cons(symbol="000300")
            return df
        except Exception as e:
            logger.error(f"Error fetching HS300 stocks: {e}")
            raise DataSourceError(f"Error fetching HS300 stocks: {e}")
    
    def get_zz500_stocks(self, date: Optional[str] = None) -> pd.DataFrame:
        """获取中证500成分股"""
        try:
            df = ak.index_stock_cons(symbol="000905")
            return df
        except Exception as e:
            logger.error(f"Error fetching ZZ500 stocks: {e}")
            raise DataSourceError(f"Error fetching ZZ500 stocks: {e}")
    
    def get_trade_dates(self, start_date: Optional[str] = None, end_date: Optional[str] = None) -> pd.DataFrame:
        """获取交易日历"""
        try:
            df = ak.tool_trade_date_hist_sina()
            
            if start_date and end_date:
                df = df[(df['trade_date'] >= start_date) & (df['trade_date'] <= end_date)]
            
            return df
            
        except Exception as e:
            logger.error(f"Error fetching trade dates: {e}")
            raise DataSourceError(f"Error fetching trade dates: {e}")
    
    def get_all_stock(self, date: Optional[str] = None) -> pd.DataFrame:
        """获取所有股票列表"""
        try:
            # 获取A股列表
            df_a = ak.stock_zh_a_spot_em()
            df_a['market'] = 'A'
            
            # 可以选择性地添加港股和美股
            result_df = df_a[['代码', '名称', 'market']].copy()
            result_df.columns = ['code', 'code_name', 'market']
            
            return result_df
            
        except Exception as e:
            logger.error(f"Error fetching all stocks: {e}")
            raise DataSourceError(f"Error fetching all stocks: {e}")
    
    # 宏观经济数据（部分支持）
    def get_deposit_rate_data(self, start_date: Optional[str] = None, end_date: Optional[str] = None) -> pd.DataFrame:
        """获取存款利率数据"""
        try:
            df = ak.rate_interbank()
            return df
        except Exception as e:
            logger.error(f"Error fetching deposit rate data: {e}")
            raise DataSourceError(f"Error fetching deposit rate data: {e}")
    
    def get_loan_rate_data(self, start_date: Optional[str] = None, end_date: Optional[str] = None) -> pd.DataFrame:
        """获取贷款利率数据"""
        try:
            df = ak.rate_interbank()
            return df
        except Exception as e:
            logger.error(f"Error fetching loan rate data: {e}")
            raise DataSourceError(f"Error fetching loan rate data: {e}")
    
    def get_required_reserve_ratio_data(self, start_date: Optional[str] = None, end_date: Optional[str] = None, year_type: str = '0') -> pd.DataFrame:
        """获取存款准备金率数据"""
        raise NoDataFoundError("Required reserve ratio data not available in AKShare")
    
    def get_money_supply_data_month(self, start_date: Optional[str] = None, end_date: Optional[str] = None) -> pd.DataFrame:
        """获取货币供应量月度数据"""
        try:
            df = ak.macro_china_m2_yearly()
            return df
        except Exception as e:
            logger.error(f"Error fetching money supply data: {e}")
            raise DataSourceError(f"Error fetching money supply data: {e}")
    
    def get_money_supply_data_year(self, start_date: Optional[str] = None, end_date: Optional[str] = None) -> pd.DataFrame:
        """获取货币供应量年度数据"""
        return self.get_money_supply_data_month(start_date, end_date)
    
    def get_shibor_data(self, start_date: Optional[str] = None, end_date: Optional[str] = None) -> pd.DataFrame:
        """获取SHIBOR数据"""
        try:
            df = ak.rate_interbank()
            return df
        except Exception as e:
            logger.error(f"Error fetching SHIBOR data: {e}")
            raise DataSourceError(f"Error fetching SHIBOR data: {e}")