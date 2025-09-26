# Hong Kong Stock Market Tools
import logging
from typing import Optional, List
from datetime import datetime
from ..data_source_interface import FinancialDataSource, NoDataFoundError, DataSourceError
from ..formatting.markdown_formatter import format_df_to_markdown as format_dataframe_as_markdown
from .quarter_utils import (
    try_get_financial_data_with_fallback,
    get_data_freshness_note,
    format_financial_section
)

logger = logging.getLogger(__name__)

# 全局数据源变量，在注册时设置
_data_source: Optional[FinancialDataSource] = None

def _get_data_source() -> FinancialDataSource:
    """获取数据源实例"""
    if _data_source is None:
        raise RuntimeError("数据源未初始化，请先调用 register_hk_stock_tools")
    return _data_source

# 模块级别的函数定义，可以直接导入

def get_hk_historical_k_data(
    code: str,
    start_date: str,
    end_date: str,
    frequency: str = "d",
    fields: Optional[List[str]] = None,
) -> str:
    """
    获取港股历史K线数据
    
    Args:
        code: 港股代码 (如 'hk.00700' 表示腾讯)
        start_date: 开始日期 'YYYY-MM-DD'
        end_date: 结束日期 'YYYY-MM-DD'
        frequency: 数据频率，默认'd'(日线)
        fields: 可选的字段列表
    
    Returns:
        Markdown格式的K线数据表格
    """
    logger.info(f"Getting HK stock K data for {code}")
    try:
        data_source = _get_data_source()
        
        # 确保代码格式正确
        if not code.startswith("hk."):
            code = f"hk.{code}"
        
        df = data_source.get_historical_k_data(
            code=code,
            start_date=start_date,
            end_date=end_date,
            frequency=frequency,
            fields=fields
        )
        
        if df.empty:
            return f"未找到港股 {code} 在 {start_date} 到 {end_date} 期间的K线数据。"
        
        return format_dataframe_as_markdown(
            df, 
            title=f"港股 {code} K线数据 ({start_date} 到 {end_date})"
        )
        
    except NoDataFoundError as e:
        logger.warning(f"No HK stock K data found: {e}")
        return f"未找到港股K线数据: {str(e)}\n\n**说明**: 这可能是由于:\n- 股票代码不正确（请确保格式为 hk.XXXXX，如 hk.00700）\n- 查询的日期范围内没有交易数据（如节假日或该股票暂停交易）\n- 日期格式不正确（请使用 YYYY-MM-DD 格式）\n- 数据源暂时无法访问\n\n请检查参数或稍后重试。"
    except DataSourceError as e:
        logger.error(f"Data source error for HK stock K data: {e}")
        return f"港股K线数据获取错误: {str(e)}\n\n**说明**: 数据源连接出现问题，请稍后重试。如问题持续存在，可能是AkShare数据源服务暂时不可用。"
    except Exception as e:
        logger.exception(f"Unexpected error getting HK stock K data: {e}")
        return f"获取港股K线数据时发生意外错误: {str(e)}\n\n**说明**: 系统遇到未预期的错误，请联系技术支持或稍后重试。"

def get_hk_stock_basic_info(code: str, fields: Optional[List[str]] = None) -> str:
    """
    获取港股基本信息
    
    Args:
        code: 港股代码 (如 'hk.00700' 表示腾讯)
        fields: 可选的字段列表
    
    Returns:
        Markdown格式的基本信息表格
    """
    logger.info(f"Getting HK stock basic info for {code}")
    try:
        data_source = _get_data_source()
        
        # 确保代码格式正确
        if not code.startswith("hk."):
            code = f"hk.{code}"
        
        df = data_source.get_stock_basic_info(code=code, fields=fields)
        
        if df.empty:
            return f"未找到港股 {code} 的基本信息。"
        
        return format_dataframe_as_markdown(
            df, 
            title=f"港股 {code} 基本信息"
        )
        
    except NoDataFoundError as e:
        logger.warning(f"No HK stock basic info found: {e}")
        return f"未找到港股基本信息: {str(e)}\n\n**说明**: 这可能是由于:\n- 股票代码不正确（请确保格式为 hk.XXXXX，如 hk.00700）\n- 该股票已退市或暂停交易\n- 数据源暂时无法访问\n\n请检查股票代码或稍后重试。"
    except DataSourceError as e:
        logger.error(f"Data source error for HK stock basic info: {e}")
        return f"港股基本信息获取错误: {str(e)}\n\n**说明**: 数据源连接出现问题，请稍后重试。如问题持续存在，可能是AkShare数据源服务暂时不可用。"
    except Exception as e:
        logger.exception(f"Unexpected error getting HK stock basic info: {e}")
        return f"获取港股基本信息时发生意外错误: {str(e)}\n\n**说明**: 系统遇到未预期的错误，请联系技术支持或稍后重试。"

def get_hk_stock_realtime_data(code: str) -> str:
    """
    获取港股实时行情数据
    
    Args:
        code: 港股代码 (如 'hk.00700' 表示腾讯)
    
    Returns:
        Markdown格式的实时行情数据
    """
    logger.info(f"Getting HK stock realtime data for {code}")
    try:
        data_source = _get_data_source()
        
        # 确保代码格式正确
        if not code.startswith("hk."):
            code = f"hk.{code}"
        
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
            return f"未找到港股 {code} 的实时数据。"
        
        # 取最新的一条记录
        latest_data = df.tail(1)
        
        return format_dataframe_as_markdown(
            latest_data, 
            title=f"港股 {code} 最新行情数据"
        )
        
    except NoDataFoundError as e:
        logger.warning(f"No HK stock realtime data found: {e}")
        return f"未找到港股实时数据: {str(e)}\n\n**说明**: 港股实时数据可能缺失的原因:\n- 股票代码不正确（请确保格式为 hk.XXXXX）\n- 该股票当前暂停交易\n- 非交易时间（港股交易时间：周一至周五 9:30-12:00, 13:00-16:00 HKT）\n- 数据源暂时无法访问实时行情数据\n\n建议检查股票代码或在交易时间内重试。"
    except DataSourceError as e:
        logger.error(f"Data source error for HK stock realtime data: {e}")
        return f"港股实时数据获取错误: {str(e)}\n\n**说明**: 数据源连接出现问题，请稍后重试。港股实时数据通过AkShare获取，如问题持续存在，可能是数据源服务暂时不可用。"
    except Exception as e:
        logger.exception(f"Unexpected error getting HK stock realtime data: {e}")
        return f"获取港股实时数据时发生意外错误: {str(e)}\n\n**说明**: 系统遇到未预期的错误，请联系技术支持或稍后重试。"

def get_popular_hk_stocks(limit: int = 20) -> str:
    """
    获取热门港股列表
    
    Args:
        limit: 返回的股票数量限制，默认20
    
    Returns:
        Markdown格式的热门港股列表
    """
    logger.info(f"Getting popular HK stocks with limit {limit}")
    try:
        # 返回一些常见的港股代码作为示例
        popular_stocks = [
            {"code": "hk.00700", "name": "腾讯控股", "sector": "科技"},
            {"code": "hk.09988", "name": "阿里巴巴-SW", "sector": "科技"},
            {"code": "hk.03690", "name": "美团-W", "sector": "科技"},
            {"code": "hk.09618", "name": "京东集团-SW", "sector": "科技"},
            {"code": "hk.02318", "name": "中国平安", "sector": "金融"},
            {"code": "hk.00939", "name": "建设银行", "sector": "金融"},
            {"code": "hk.00941", "name": "中国移动", "sector": "电信"},
            {"code": "hk.00883", "name": "中国海洋石油", "sector": "能源"},
            {"code": "hk.01299", "name": "友邦保险", "sector": "金融"},
            {"code": "hk.00388", "name": "香港交易所", "sector": "金融"},
            {"code": "hk.00697", "name": "首程控股", "sector": "综合"},
            {"code": "hk.01810", "name": "小米集团-W", "sector": "科技"},
            {"code": "hk.09999", "name": "网易-S", "sector": "科技"},
            {"code": "hk.01024", "name": "快手-W", "sector": "科技"},
            {"code": "hk.01211", "name": "比亚迪股份", "sector": "汽车"},
        ]
        
        # 限制返回数量
        limited_stocks = popular_stocks[:limit]
        
        # 转换为DataFrame格式
        import pandas as pd
        df = pd.DataFrame(limited_stocks)
        
        return format_dataframe_as_markdown(
            df, 
            title=f"热门港股列表 (前{len(limited_stocks)}只)"
        )
        
    except Exception as e:
        logger.exception(f"Unexpected error getting popular HK stocks: {e}")
        return f"获取热门港股列表时发生意外错误: {str(e)}"

def search_hk_stocks(keyword: str) -> str:
    """
    搜索港股股票
    
    Args:
        keyword: 搜索关键词 (股票名称或代码)
    
    Returns:
        Markdown格式的搜索结果
    """
    logger.info(f"Searching HK stocks with keyword: {keyword}")
    try:
        # 简单的搜索逻辑，实际应该连接到数据源
        stock_database = [
            {"code": "hk.00700", "name": "腾讯控股", "sector": "科技"},
            {"code": "hk.09988", "name": "阿里巴巴-SW", "sector": "科技"},
            {"code": "hk.03690", "name": "美团-W", "sector": "科技"},
            {"code": "hk.00697", "name": "首程控股", "sector": "综合"},
        ]
        
        # 搜索匹配的股票
        results = []
        keyword_lower = keyword.lower()
        
        for stock in stock_database:
            if (keyword_lower in stock["name"].lower() or 
                keyword_lower in stock["code"].lower() or
                keyword_lower.replace("hk.", "") in stock["code"]):
                results.append(stock)
        
        if not results:
            return f"未找到与 '{keyword}' 相关的港股。"
        
        # 转换为DataFrame格式
        import pandas as pd
        df = pd.DataFrame(results)
        
        return format_dataframe_as_markdown(
            df, 
            title=f"港股搜索结果: '{keyword}'"
        )
        
    except Exception as e:
        logger.exception(f"Unexpected error searching HK stocks: {e}")
        return f"搜索港股时发生意外错误: {str(e)}"

# 财务分析函数

def get_hk_profit_data(code: str, year: str, quarter: int) -> str:
    """
    获取港股季度盈利能力数据 (如ROE、净利润率等)
    
    Args:
        code: 港股代码 (如 'hk.00700')
        year: 4位年份 (如 '2023')
        quarter: 季度 (1, 2, 3, 或 4)
    
    Returns:
        Markdown格式的盈利能力数据表格或错误信息
    """
    logger.info(f"Getting HK stock profit data for {code}")
    try:
        data_source = _get_data_source()
        
        # 确保代码格式正确
        if not code.startswith("hk."):
            code = f"hk.{code}"
        
        df = data_source.get_profit_data(code=code, year=year, quarter=quarter)
        
        if df.empty:
            return f"未找到港股 {code} 在 {year}年第{quarter}季度的盈利能力数据。"
        
        return format_dataframe_as_markdown(
            df, 
            title=f"港股 {code} 盈利能力数据 ({year}年第{quarter}季度)"
        )
        
    except NoDataFoundError as e:
        logger.warning(f"No HK stock profit data found: {e}")
        return f"未找到港股盈利数据: {str(e)}\n\n**说明**: 港股财务数据可能缺失的原因:\n- 该季度财报尚未发布（港股财报发布时间可能晚于A股）\n- 股票代码不正确（请确保格式为 hk.XXXXX）\n- 该公司可能不需要发布季度报告（部分港股公司只发布半年报和年报）\n- 数据源暂时无法访问相关财务数据\n\n建议查询最近已发布的财报期间或稍后重试。"
    except DataSourceError as e:
        logger.error(f"Data source error for HK stock profit data: {e}")
        return f"港股盈利数据获取错误: {str(e)}\n\n**说明**: 数据源连接出现问题，请稍后重试。港股财务数据通过AkShare获取，如问题持续存在，可能是数据源服务暂时不可用。"
    except Exception as e:
        logger.exception(f"Unexpected error getting HK stock profit data: {e}")
        return f"获取港股盈利数据时发生意外错误: {str(e)}\n\n**说明**: 系统遇到未预期的错误，请联系技术支持或稍后重试。"

def get_hk_operation_data(code: str, year: str, quarter: int) -> str:
    """
    获取港股季度运营能力数据 (如周转率等)
    
    Args:
        code: 港股代码 (如 'hk.00700')
        year: 4位年份 (如 '2023')
        quarter: 季度 (1, 2, 3, 或 4)
    
    Returns:
        Markdown格式的运营能力数据表格或错误信息
    """
    logger.info(f"Getting HK stock operation data for {code}")
    try:
        data_source = _get_data_source()
        
        # 确保代码格式正确
        if not code.startswith("hk."):
            code = f"hk.{code}"
        
        df = data_source.get_operation_data(code=code, year=year, quarter=quarter)
        
        if df.empty:
            return f"未找到港股 {code} 在 {year}年第{quarter}季度的运营能力数据。"
        
        return format_dataframe_as_markdown(
            df, 
            title=f"港股 {code} 运营能力数据 ({year}年第{quarter}季度)"
        )
        
    except NoDataFoundError as e:
        logger.warning(f"No HK stock operation data found: {e}")
        return f"未找到港股运营数据: {str(e)}\n\n**说明**: 港股财务数据可能缺失的原因:\n- 该季度财报尚未发布（港股财报发布时间可能晚于A股）\n- 股票代码不正确（请确保格式为 hk.XXXXX）\n- 该公司可能不需要发布季度报告（部分港股公司只发布半年报和年报）\n- 数据源暂时无法访问相关财务数据\n\n建议查询最近已发布的财报期间或稍后重试。"
    except DataSourceError as e:
        logger.error(f"Data source error for HK stock operation data: {e}")
        return f"港股运营数据获取错误: {str(e)}\n\n**说明**: 数据源连接出现问题，请稍后重试。港股财务数据通过AkShare获取，如问题持续存在，可能是数据源服务暂时不可用。"
    except Exception as e:
        logger.exception(f"Unexpected error getting HK stock operation data: {e}")
        return f"获取港股运营数据时发生意外错误: {str(e)}\n\n**说明**: 系统遇到未预期的错误，请联系技术支持或稍后重试。"

def get_hk_growth_data(code: str, year: str, quarter: int) -> str:
    """
    获取港股季度成长能力数据 (如同比增长率等)

    Args:
        code: 港股代码 (如 'hk.00700')
        year: 4位年份 (如 '2023')
        quarter: 季度 (1, 2, 3, 或 4)

    Returns:
        Markdown格式的成长能力数据表格或错误信息
    """
    logger.info(f"Getting HK stock growth data for {code}")
    try:
        data_source = _get_data_source()
        
        # 确保代码格式正确
        if not code.startswith("hk."):
            code = f"hk.{code}"
        
        df = data_source.get_growth_data(code=code, year=year, quarter=quarter)
        
        if df.empty:
            return f"未找到港股 {code} 在 {year}年第{quarter}季度的成长能力数据。"
        
        return format_dataframe_as_markdown(
            df, 
            title=f"港股 {code} 成长能力数据 ({year}年第{quarter}季度)"
        )
        
    except NoDataFoundError as e:
        logger.warning(f"No HK stock growth data found: {e}")
        return f"未找到港股成长数据: {str(e)}\n\n**说明**: 港股财务数据可能缺失的原因:\n- 该季度财报尚未发布（港股财报发布时间可能晚于A股）\n- 股票代码不正确（请确保格式为 hk.XXXXX）\n- 该公司可能不需要发布季度报告（部分港股公司只发布半年报和年报）\n- 数据源暂时无法访问相关财务数据\n\n建议查询最近已发布的财报期间或稍后重试。"
    except DataSourceError as e:
        logger.error(f"Data source error for HK stock growth data: {e}")
        return f"港股成长数据获取错误: {str(e)}\n\n**说明**: 数据源连接出现问题，请稍后重试。港股财务数据通过AkShare获取，如问题持续存在，可能是数据源服务暂时不可用。"
    except Exception as e:
        logger.exception(f"Unexpected error getting HK stock growth data: {e}")
        return f"获取港股成长数据时发生意外错误: {str(e)}\n\n**说明**: 系统遇到未预期的错误，请联系技术支持或稍后重试。"

def get_hk_balance_data(code: str, year: str, quarter: int) -> str:
    """
    获取港股季度资产负债表/偿债能力数据 (如流动比率、负债率等)
    
    Args:
        code: 港股代码 (如 'hk.00700')
        year: 4位年份 (如 '2023')
        quarter: 季度 (1, 2, 3, 或 4)
    
    Returns:
        Markdown格式的资产负债表数据表格或错误信息
    """
    logger.info(f"Getting HK stock balance data for {code}")
    try:
        data_source = _get_data_source()
        
        # 确保代码格式正确
        if not code.startswith("hk."):
            code = f"hk.{code}"
        
        df = data_source.get_balance_data(code=code, year=year, quarter=quarter)
        
        if df.empty:
            return f"未找到港股 {code} 在 {year}年第{quarter}季度的资产负债表数据。"
        
        return format_dataframe_as_markdown(
            df, 
            title=f"港股 {code} 资产负债表数据 ({year}年第{quarter}季度)"
        )
        
    except NoDataFoundError as e:
        logger.warning(f"No HK stock balance data found: {e}")
        return f"未找到港股资产负债数据: {str(e)}\n\n**说明**: 港股财务数据可能缺失的原因:\n- 该季度财报尚未发布（港股财报发布时间可能晚于A股）\n- 股票代码不正确（请确保格式为 hk.XXXXX）\n- 该公司可能不需要发布季度报告（部分港股公司只发布半年报和年报）\n- 数据源暂时无法访问相关财务数据\n\n建议查询最近已发布的财报期间或稍后重试。"
    except DataSourceError as e:
        logger.error(f"Data source error for HK stock balance data: {e}")
        return f"港股资产负债数据获取错误: {str(e)}\n\n**说明**: 数据源连接出现问题，请稍后重试。港股财务数据通过AkShare获取，如问题持续存在，可能是数据源服务暂时不可用。"
    except Exception as e:
        logger.exception(f"Unexpected error getting HK stock balance data: {e}")
        return f"获取港股资产负债数据时发生意外错误: {str(e)}\n\n**说明**: 系统遇到未预期的错误，请联系技术支持或稍后重试。"

def get_hk_cash_flow_data(code: str, year: str, quarter: int) -> str:
    """
    获取港股季度现金流数据 (如经营现金流/营业收入比率等)
    
    Args:
        code: 港股代码 (如 'hk.00700')
        year: 4位年份 (如 '2023')
        quarter: 季度 (1, 2, 3, 或 4)
    
    Returns:
        Markdown格式的现金流数据表格或错误信息
    """
    logger.info(f"Getting HK stock cash flow data for {code}")
    try:
        data_source = _get_data_source()
        
        # 确保代码格式正确
        if not code.startswith("hk."):
            code = f"hk.{code}"
        
        df = data_source.get_cash_flow_data(code=code, year=year, quarter=quarter)
        
        if df.empty:
            return f"未找到港股 {code} 在 {year}年第{quarter}季度的现金流数据。"
        
        return format_dataframe_as_markdown(
            df, 
            title=f"港股 {code} 现金流数据 ({year}年第{quarter}季度)"
        )
        
    except NoDataFoundError as e:
        logger.warning(f"No HK stock cash flow data found: {e}")
        return f"未找到港股现金流数据: {str(e)}\n\n**说明**: 港股财务数据可能缺失的原因:\n- 该季度财报尚未发布（港股财报发布时间可能晚于A股）\n- 股票代码不正确（请确保格式为 hk.XXXXX）\n- 该公司可能不需要发布季度报告（部分港股公司只发布半年报和年报）\n- 数据源暂时无法访问相关财务数据\n\n建议查询最近已发布的财报期间或稍后重试。"
    except DataSourceError as e:
        logger.error(f"Data source error for HK stock cash flow data: {e}")
        return f"港股现金流数据获取错误: {str(e)}\n\n**说明**: 数据源连接出现问题，请稍后重试。港股财务数据通过AkShare获取，如问题持续存在，可能是数据源服务暂时不可用。"
    except Exception as e:
        logger.exception(f"Unexpected error getting HK stock cash flow data: {e}")
        return f"获取港股现金流数据时发生意外错误: {str(e)}\n\n**说明**: 系统遇到未预期的错误，请联系技术支持或稍后重试。"

def get_hk_dupont_data(code: str, year: str, quarter: int) -> str:
    """
    获取港股季度杜邦分析数据 (ROE分解)
    
    Args:
        code: 港股代码 (如 'hk.00700')
        year: 4位年份 (如 '2023')
        quarter: 季度 (1, 2, 3, 或 4)
    
    Returns:
        Markdown格式的杜邦分析数据表格或错误信息
    """
    logger.info(f"Getting HK stock dupont data for {code}")
    try:
        data_source = _get_data_source()
        
        # 确保代码格式正确
        if not code.startswith("hk."):
            code = f"hk.{code}"
        
        df = data_source.get_dupont_data(code=code, year=year, quarter=quarter)
        
        if df.empty:
            return f"未找到港股 {code} 在 {year}年第{quarter}季度的杜邦分析数据。"
        
        return format_dataframe_as_markdown(
            df, 
            title=f"港股 {code} 杜邦分析数据 ({year}年第{quarter}季度)"
        )
        
    except NoDataFoundError as e:
        logger.warning(f"No HK stock dupont data found: {e}")
        return f"未找到港股杜邦分析数据: {str(e)}\n\n**说明**: 港股财务数据可能缺失的原因:\n- 该季度财报尚未发布（港股财报发布时间可能晚于A股）\n- 股票代码不正确（请确保格式为 hk.XXXXX）\n- 该公司可能不需要发布季度报告（部分港股公司只发布半年报和年报）\n- 数据源暂时无法访问相关财务数据\n\n建议查询最近已发布的财报期间或稍后重试。"
    except DataSourceError as e:
        logger.error(f"Data source error for HK stock dupont data: {e}")
        return f"港股杜邦分析数据获取错误: {str(e)}\n\n**说明**: 数据源连接出现问题，请稍后重试。港股财务数据通过AkShare获取，如问题持续存在，可能是数据源服务暂时不可用。"
    except Exception as e:
        logger.exception(f"Unexpected error getting HK stock dupont data: {e}")
        return f"获取港股杜邦分析数据时发生意外错误: {str(e)}\n\n**说明**: 系统遇到未预期的错误，请联系技术支持或稍后重试。"

def get_hk_dividend_data(code: str, year: str) -> str:
    """
    获取港股分红信息
    
    Args:
        code: 港股代码 (如 'hk.00700')
        year: 年份 (如 '2023')
    
    Returns:
        Markdown格式的分红数据表格或错误信息
    """
    logger.info(f"Getting HK stock dividend data for {code}")
    try:
        data_source = _get_data_source()
        
        # 确保代码格式正确
        if not code.startswith("hk."):
            code = f"hk.{code}"
        
        df = data_source.get_dividend_data(code=code, year=year)
        
        if df.empty:
            return f"未找到港股 {code} 在 {year}年的分红数据。"
        
        return format_dataframe_as_markdown(
            df, 
            title=f"港股 {code} 分红数据 ({year}年)"
        )
        
    except NoDataFoundError as e:
        logger.warning(f"No HK stock dividend data found: {e}")
        return f"未找到港股分红数据: {str(e)}\n\n**说明**: 港股分红数据可能缺失的原因:\n- 该年度尚未发布分红公告\n- 股票代码不正确（请确保格式为 hk.XXXXX）\n- 该公司当年未进行分红\n- 数据源暂时无法访问相关分红数据\n\n建议查询其他年份的分红记录或稍后重试。"
    except DataSourceError as e:
        logger.error(f"Data source error for HK stock dividend data: {e}")
        return f"港股分红数据获取错误: {str(e)}\n\n**说明**: 数据源连接出现问题，请稍后重试。港股分红数据通过AkShare获取，如问题持续存在，可能是数据源服务暂时不可用。"
    except Exception as e:
        logger.exception(f"Unexpected error getting HK stock dividend data: {e}")
        return f"获取港股分红数据时发生意外错误: {str(e)}\n\n**说明**: 系统遇到未预期的错误，请联系技术支持或稍后重试。"

def get_hk_stock_analysis(code: str, analysis_type: str = "fundamental") -> str:
    """
    提供基于数据的港股分析报告，而非投资建议
    
    Args:
        code: 港股代码，如'hk.00700'
        analysis_type: 分析类型，可选'fundamental'(基本面)、'technical'(技术面)或'comprehensive'(综合)
    
    Returns:
        数据驱动的分析报告，包含关键财务指标、历史表现和同行业比较
    """
    logger.info(f"Getting HK stock analysis for {code}")
    try:
        data_source = _get_data_source()
        
        # 确保代码格式正确
        if not code.startswith("hk."):
            code = f"hk.{code}"
        
        # 获取基本信息
        basic_info = None
        stock_name = code
        try:
            basic_info = data_source.get_stock_basic_info(code)
            if not basic_info.empty and 'code_name' in basic_info.columns:
                stock_name = basic_info['code_name'].values[0]
        except Exception as e:
            logger.warning(f"Failed to get basic info for {code}: {e}")
        
        # 构建分析报告 - 统一格式与A股报告
        report = f"# {stock_name} 数据分析报告\n\n"
        report += "## 免责声明\n本报告基于公开数据生成，仅供参考，不构成投资建议。投资决策需基于个人风险承受能力和研究。\n\n"
        report += "**数据源说明**: 港股数据通过AkShare获取，可能存在数据延迟或部分财务指标缺失的情况。\n\n"
        
        # 公司基本信息
        report += "## 公司基本信息\n"
        report += f"- 股票代码: {code}\n"
        
        if basic_info is not None and not basic_info.empty:
            if 'code_name' in basic_info.columns:
                report += f"- 股票名称: {basic_info['code_name'].values[0]}\n"
            if 'industry' in basic_info.columns:
                report += f"- 所属行业: {basic_info['industry'].values[0]}\n"
            if 'ipoDate' in basic_info.columns:
                report += f"- 上市日期: {basic_info['ipoDate'].values[0]}\n"
            if 'listStatus' in basic_info.columns:
                report += f"- 上市状态: {basic_info['listStatus'].values[0]}\n"
        else:
            report += "- 股票名称: 数据获取中...\n"
            report += "- 所属行业: 数据获取中...\n"
            report += "- 上市日期: 数据获取中...\n"
        
        report += "\n"
        
        # 获取历史价格数据用于技术分析
        price_data = None
        if analysis_type in ["technical", "comprehensive"]:
            try:
                from datetime import timedelta
                end_date = datetime.now().strftime("%Y-%m-%d")
                start_date = (datetime.now() - timedelta(days=180)).strftime("%Y-%m-%d")
                
                price_data = data_source.get_historical_k_data(code, start_date, end_date)
            except Exception as e:
                logger.warning(f"Failed to get price data for {code}: {e}")
        
        # 基本面指标分析
        if analysis_type in ["fundamental", "comprehensive"]:
            # 使用智能季度回退机制获取最新可用的财务数据
            profit_data, data_year, data_quarter = try_get_financial_data_with_fallback(
                data_source, code, "profit")
            growth_data, _, _ = try_get_financial_data_with_fallback(
                data_source, code, "growth")
            balance_data, _, _ = try_get_financial_data_with_fallback(
                data_source, code, "balance")
            
            if data_year and data_quarter:
                report += f"## 基本面指标分析 ({data_year}年第{data_quarter}季度)\n\n"
                
                # 添加数据时效性说明
                report += get_data_freshness_note(data_year, data_quarter)

                # 盈利能力指标
                profit_mappings = {
                    'roeAvg': 'ROE(净资产收益率)',
                    'npMargin': '销售净利率',
                    'grossProfitMargin': '毛利率',
                    'netProfit': '净利润'
                }
                report += format_financial_section(
                    profit_data, "盈利能力指标", data_year, data_quarter, profit_mappings)

                # 成长能力指标
                growth_mappings = {
                    'YOYEquity': '净资产同比增长',
                    'YOYAsset': '总资产同比增长',
                    'YOYNI': '净利润同比增长',
                    'YOYEPSBasic': '每股收益同比增长'
                }
                report += format_financial_section(
                    growth_data, "成长能力指标", data_year, data_quarter, growth_mappings)

                # 财务健康状况
                balance_mappings = {
                    'currentRatio': '流动比率',
                    'assetLiabRatio': '资产负债率',
                    'quickRatio': '速动比率',
                    'cashRatio': '现金比率'
                }
                report += format_financial_section(
                    balance_data, "财务健康状况", data_year, data_quarter, balance_mappings)
            else:
                report += "## 基本面指标分析\n\n"
                report += "⚠️ **数据获取失败**: 无法获取最新的财务数据，可能原因：\n"
                report += "- 财务数据尚未发布（通常滞后1-3个月）\n"
                report += "- 数据源暂时不可用\n"
                report += "- 股票代码可能有误\n\n"

            
            # 估值水平
            report += "\n### 估值水平\n"
            if price_data is not None and not price_data.empty:
                if 'peTTM' in price_data.columns:
                    latest_pe = price_data['peTTM'].iloc[-1]
                    if latest_pe and str(latest_pe) != 'nan':
                        report += f"- 市盈率(PE-TTM): {latest_pe:.2f}\n"
                if 'pbMRQ' in price_data.columns:
                    latest_pb = price_data['pbMRQ'].iloc[-1]
                    if latest_pb and str(latest_pb) != 'nan':
                        report += f"- 市净率(PB-MRQ): {latest_pb:.2f}\n"
                if 'psTTM' in price_data.columns:
                    latest_ps = price_data['psTTM'].iloc[-1]
                    if latest_ps and str(latest_ps) != 'nan':
                        report += f"- 市销率(PS-TTM): {latest_ps:.2f}\n"
            
            if 'latest_pe' not in locals() and 'latest_pb' not in locals():
                report += "- 暂无估值数据（可能由于数据源限制）\n"
        
        # 技术面分析
        if analysis_type in ["technical", "comprehensive"] and price_data is not None and not price_data.empty:
            report += "\n## 技术面分析\n\n"
            
            if 'close' in price_data.columns and len(price_data) > 1:
                latest_price = price_data['close'].iloc[-1]
                start_price = price_data['close'].iloc[0]
                price_change = ((float(latest_price) / float(start_price)) - 1) * 100
                
                report += f"- 最新收盘价: {latest_price}\n"
                report += f"- 6个月价格变动: {price_change:.2f}%\n"
                
                # 计算简单的均线
                if len(price_data) >= 20:
                    ma20 = price_data['close'].astype(float).tail(20).mean()
                    report += f"- 20日均价: {ma20:.2f}\n"
                    if float(latest_price) > ma20:
                        report += f"  (当前价格高于20日均线 {((float(latest_price)/ma20)-1)*100:.2f}%)\n"
                    else:
                        report += f"  (当前价格低于20日均线 {((ma20/float(latest_price))-1)*100:.2f}%)\n"
                
                # 价格波动率
                if len(price_data) >= 20:
                    returns = price_data['close'].pct_change().dropna()
                    if len(returns) > 0:
                        volatility = returns.std() * 100
                        report += f"- 价格波动率: {volatility:.2f}%\n"
        elif analysis_type in ["technical", "comprehensive"]:
            report += "\n## 技术面分析\n\n"
            report += "- 暂无足够的价格数据进行技术分析\n"
        
        # 投资要点总结
        report += "\n## 投资要点总结\n"
        report += "- 以上数据仅供参考，建议结合公司公告、行业趋势和宏观环境进行综合分析\n"
        report += "- 港股市场具有独特性，受汇率、流动性、监管环境等多重因素影响\n"
        report += "- 个股表现受多种因素影响，历史数据不代表未来表现\n"
        report += "- 投资决策应基于个人风险承受能力和投资目标\n"
        report += "- 港股财务数据可能存在发布时间差异，建议关注最新公司公告\n\n"
        
        # 数据源说明
        report += "## 数据源说明\n"
        report += "- 港股数据通过AkShare数据源获取\n"
        report += "- 部分财务指标可能因数据源限制而缺失\n"
        report += "- 建议结合多个数据源进行交叉验证\n"
        report += "- 实时数据可能存在15-20分钟延迟\n"
        
        return report
        
    except NoDataFoundError as e:
        logger.warning(f"No HK stock analysis data found: {e}")
        return f"未找到港股分析数据: {str(e)}\n\n**说明**: 这可能是由于:\n- 股票代码不正确\n- 该股票暂停交易\n- 数据源暂时无法访问\n\n请检查股票代码格式（如: hk.00700）或稍后重试。"
    except DataSourceError as e:
        logger.error(f"Data source error for HK stock analysis: {e}")
        return f"港股分析数据获取错误: {str(e)}\n\n**说明**: 数据源连接出现问题，请稍后重试。如问题持续存在，可能是数据源服务暂时不可用。"
    except Exception as e:
        logger.exception(f"Unexpected error getting HK stock analysis: {e}")
        return f"获取港股分析时发生意外错误: {str(e)}\n\n**说明**: 系统遇到未预期的错误，请联系技术支持或稍后重试。"

# 注册函数，用于MCP服务器

def register_hk_stock_tools(app, data_source: FinancialDataSource):
    """注册港股相关工具"""
    global _data_source
    _data_source = data_source
    
    # 注册所有工具函数
    app.tool()(get_hk_historical_k_data)
    app.tool()(get_hk_stock_basic_info)
    app.tool()(get_hk_stock_realtime_data)
    app.tool()(get_popular_hk_stocks)
    app.tool()(search_hk_stocks)
    app.tool()(get_hk_profit_data)
    app.tool()(get_hk_operation_data)
    app.tool()(get_hk_growth_data)
    app.tool()(get_hk_balance_data)
    app.tool()(get_hk_cash_flow_data)
    app.tool()(get_hk_dupont_data)
    app.tool()(get_hk_dividend_data)
    app.tool()(get_hk_stock_analysis)