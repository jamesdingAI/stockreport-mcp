# US Stock Market Tools
import logging
from typing import Optional, List
from ..data_source_interface import FinancialDataSource, NoDataFoundError, DataSourceError
from ..formatting.markdown_formatter import format_df_to_markdown as format_dataframe_as_markdown

logger = logging.getLogger(__name__)

def register_us_stock_tools(app, data_source: FinancialDataSource):
    """注册美股相关工具"""
    
    @app.tool()
    def get_us_historical_k_data(
        code: str,
        start_date: str,
        end_date: str,
        frequency: str = "d",
        fields: Optional[List[str]] = None,
    ) -> str:
        """
        获取美股历史K线数据
        
        Args:
            code: 美股代码 (如 'us.AAPL' 表示苹果公司)
            start_date: 开始日期 'YYYY-MM-DD'
            end_date: 结束日期 'YYYY-MM-DD'
            frequency: 数据频率，默认'd'(日线)
            fields: 可选的字段列表
        
        Returns:
            Markdown格式的K线数据表格
        """
        logger.info(f"Getting US stock K data for {code}")
        try:
            # 确保代码格式正确
            if not code.startswith("us."):
                code = f"us.{code.upper()}"
            
            df = data_source.get_historical_k_data(
                code=code,
                start_date=start_date,
                end_date=end_date,
                frequency=frequency,
                fields=fields
            )
            
            if df.empty:
                return f"未找到美股 {code} 在 {start_date} 到 {end_date} 期间的K线数据。"
            
            return format_dataframe_as_markdown(
                df, 
                f"美股 {code} 历史K线数据 ({start_date} 至 {end_date})"
            )
            
        except NoDataFoundError as e:
            logger.warning(f"No US stock data found: {e}")
            return f"未找到美股数据: {str(e)}"
        except DataSourceError as e:
            logger.error(f"Data source error for US stock: {e}")
            return f"美股数据获取错误: {str(e)}"
        except Exception as e:
            logger.exception(f"Unexpected error getting US stock data: {e}")
            return f"获取美股数据时发生意外错误: {str(e)}"
    
    @app.tool()
    def get_us_stock_basic_info(code: str, fields: Optional[List[str]] = None) -> str:
        """
        获取美股基本信息
        
        Args:
            code: 美股代码 (如 'us.AAPL' 表示苹果公司)
            fields: 可选的字段列表
        
        Returns:
            Markdown格式的基本信息表格
        """
        logger.info(f"Getting US stock basic info for {code}")
        try:
            # 确保代码格式正确
            if not code.startswith("us."):
                code = f"us.{code.upper()}"
            
            df = data_source.get_stock_basic_info(code=code, fields=fields)
            
            if df.empty:
                return f"未找到美股 {code} 的基本信息。"
            
            return format_dataframe_as_markdown(
                df, 
                f"美股 {code} 基本信息"
            )
            
        except NoDataFoundError as e:
            logger.warning(f"No US stock basic info found: {e}")
            return f"未找到美股基本信息: {str(e)}"
        except DataSourceError as e:
            logger.error(f"Data source error for US stock basic info: {e}")
            return f"美股基本信息获取错误: {str(e)}"
        except Exception as e:
            logger.exception(f"Unexpected error getting US stock basic info: {e}")
            return f"获取美股基本信息时发生意外错误: {str(e)}"
    
    @app.tool()
    def get_us_stock_realtime_data(code: str) -> str:
        """
        获取美股实时行情数据
        
        Args:
            code: 美股代码 (如 'us.AAPL' 表示苹果公司)
        
        Returns:
            Markdown格式的实时行情数据
        """
        logger.info(f"Getting US stock realtime data for {code}")
        try:
            # 确保代码格式正确
            if not code.startswith("us."):
                code = f"us.{code.upper()}"
            
            # 获取最近一天的数据作为实时数据的替代
            from datetime import datetime, timedelta
            end_date = datetime.now().strftime("%Y-%m-%d")
            start_date = (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d")
            
            df = data_source.get_historical_k_data(
                code=code,
                start_date=start_date,
                end_date=end_date,
                frequency="d"
            )
            
            if df.empty:
                return f"未找到美股 {code} 的实时数据。"
            
            # 取最新的一条记录
            latest_data = df.tail(1)
            
            return format_dataframe_as_markdown(
                latest_data, 
                f"美股 {code} 最新行情数据"
            )
            
        except NoDataFoundError as e:
            logger.warning(f"No US stock realtime data found: {e}")
            return f"未找到美股实时数据: {str(e)}"
        except DataSourceError as e:
            logger.error(f"Data source error for US stock realtime data: {e}")
            return f"美股实时数据获取错误: {str(e)}"
        except Exception as e:
            logger.exception(f"Unexpected error getting US stock realtime data: {e}")
            return f"获取美股实时数据时发生意外错误: {str(e)}"
    
    @app.tool()
    def get_popular_us_stocks() -> str:
        """
        获取热门美股列表
        
        Returns:
            Markdown格式的热门美股列表
        """
        logger.info("Getting popular US stocks")
        try:
            # 返回一些知名的美股代码和名称
            popular_stocks = [
                {"code": "us.AAPL", "name": "苹果公司", "sector": "科技"},
                {"code": "us.MSFT", "name": "微软", "sector": "科技"},
                {"code": "us.GOOGL", "name": "谷歌", "sector": "科技"},
                {"code": "us.AMZN", "name": "亚马逊", "sector": "科技"},
                {"code": "us.TSLA", "name": "特斯拉", "sector": "汽车"},
                {"code": "us.META", "name": "Meta", "sector": "科技"},
                {"code": "us.NVDA", "name": "英伟达", "sector": "科技"},
                {"code": "us.NFLX", "name": "奈飞", "sector": "媒体"},
                {"code": "us.JPM", "name": "摩根大通", "sector": "金融"},
                {"code": "us.JNJ", "name": "强生", "sector": "医疗"}
            ]
            
            import pandas as pd
            df = pd.DataFrame(popular_stocks)
            
            return format_dataframe_as_markdown(
                df, 
                "热门美股列表"
            )
            
        except Exception as e:
            logger.exception(f"Unexpected error getting popular US stocks: {e}")
            return f"获取热门美股列表时发生意外错误: {str(e)}"
    
    @app.tool()
    def search_us_stocks(keyword: str) -> str:
        """
        搜索美股股票
        
        Args:
            keyword: 搜索关键词（股票名称或代码）
        
        Returns:
            Markdown格式的搜索结果
        """
        logger.info(f"Searching US stocks with keyword: {keyword}")
        try:
            # 预定义的一些美股数据用于搜索
            all_stocks = [
                {"code": "us.AAPL", "name": "苹果公司", "sector": "科技"},
                {"code": "us.MSFT", "name": "微软", "sector": "科技"},
                {"code": "us.GOOGL", "name": "谷歌", "sector": "科技"},
                {"code": "us.AMZN", "name": "亚马逊", "sector": "科技"},
                {"code": "us.TSLA", "name": "特斯拉", "sector": "汽车"},
                {"code": "us.META", "name": "Meta", "sector": "科技"},
                {"code": "us.NVDA", "name": "英伟达", "sector": "科技"},
                {"code": "us.NFLX", "name": "奈飞", "sector": "媒体"},
                {"code": "us.JPM", "name": "摩根大通", "sector": "金融"},
                {"code": "us.JNJ", "name": "强生", "sector": "医疗"},
                {"code": "us.V", "name": "Visa", "sector": "金融"},
                {"code": "us.WMT", "name": "沃尔玛", "sector": "零售"},
                {"code": "us.PG", "name": "宝洁", "sector": "消费品"},
                {"code": "us.UNH", "name": "联合健康", "sector": "医疗"},
                {"code": "us.HD", "name": "家得宝", "sector": "零售"}
            ]
            
            # 搜索匹配的股票
            keyword_lower = keyword.lower()
            matched_stocks = []
            
            for stock in all_stocks:
                if (keyword_lower in stock["code"].lower() or 
                    keyword_lower in stock["name"].lower() or
                    keyword_lower in stock["sector"].lower()):
                    matched_stocks.append(stock)
            
            if not matched_stocks:
                return f"未找到与关键词 '{keyword}' 匹配的美股。"
            
            import pandas as pd
            df = pd.DataFrame(matched_stocks)
            
            return format_dataframe_as_markdown(
                df, 
                f"美股搜索结果 (关键词: {keyword})"
            )
            
        except Exception as e:
            logger.exception(f"Unexpected error searching US stocks: {e}")
            return f"搜索美股时发生意外错误: {str(e)}"
    
    @app.tool()
    def get_us_market_indices() -> str:
        """
        获取美股主要指数信息
        
        Returns:
            Markdown格式的美股指数列表
        """
        logger.info("Getting US market indices")
        try:
            # 美股主要指数
            indices = [
                {"code": "us.^DJI", "name": "道琼斯工业平均指数", "description": "30只大型蓝筹股"},
                {"code": "us.^GSPC", "name": "标普500指数", "description": "500只大中型股票"},
                {"code": "us.^IXIC", "name": "纳斯达克综合指数", "description": "科技股为主的综合指数"},
                {"code": "us.^RUT", "name": "罗素2000指数", "description": "小盘股指数"},
                {"code": "us.^VIX", "name": "恐慌指数", "description": "市场波动率指数"}
            ]
            
            import pandas as pd
            df = pd.DataFrame(indices)
            
            return format_dataframe_as_markdown(
                df, 
                "美股主要指数"
            )
            
        except Exception as e:
            logger.exception(f"Unexpected error getting US market indices: {e}")
            return f"获取美股指数信息时发生意外错误: {str(e)}"
    
    @app.tool()
    def get_us_sector_performance() -> str:
        """
        获取美股行业表现
        
        Returns:
            Markdown格式的行业表现数据
        """
        logger.info("Getting US sector performance")
        try:
            # 美股主要行业ETF
            sectors = [
                {"code": "us.XLK", "name": "科技行业ETF", "sector": "Technology"},
                {"code": "us.XLF", "name": "金融行业ETF", "sector": "Financial"},
                {"code": "us.XLV", "name": "医疗行业ETF", "sector": "Healthcare"},
                {"code": "us.XLE", "name": "能源行业ETF", "sector": "Energy"},
                {"code": "us.XLI", "name": "工业行业ETF", "sector": "Industrial"},
                {"code": "us.XLP", "name": "消费必需品ETF", "sector": "Consumer Staples"},
                {"code": "us.XLY", "name": "消费可选ETF", "sector": "Consumer Discretionary"},
                {"code": "us.XLU", "name": "公用事业ETF", "sector": "Utilities"},
                {"code": "us.XLB", "name": "材料行业ETF", "sector": "Materials"},
                {"code": "us.XLRE", "name": "房地产ETF", "sector": "Real Estate"}
            ]
            
            import pandas as pd
            df = pd.DataFrame(sectors)
            
            return format_dataframe_as_markdown(
                df, 
                "美股行业ETF列表"
            )
            
        except Exception as e:
            logger.exception(f"Unexpected error getting US sector performance: {e}")
            return f"获取美股行业表现时发生意外错误: {str(e)}"