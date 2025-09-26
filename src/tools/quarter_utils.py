"""
智能季度回退工具模块
提供财务数据查询的智能季度回退机制
"""
import logging
from datetime import datetime
from typing import Tuple, Optional, Any
from src.data_source_interface import FinancialDataSource

logger = logging.getLogger(__name__)


def get_latest_available_quarter() -> Tuple[int, int]:
    """
    获取最新可用的财务数据季度
    
    考虑财务数据发布滞后1-3个月的实际情况
    
    Returns:
        Tuple[int, int]: (年份, 季度)
    """
    current_date = datetime.now()
    current_year = current_date.year
    current_month = current_date.month
    
    # 根据当前月份推算最可能有数据的季度
    # 财务数据发布通常滞后1-3个月
    if current_month <= 4:  # 1-4月，Q4数据可能还未发布
        return current_year - 1, 4
    elif current_month <= 7:  # 5-7月，Q1数据应该可用
        return current_year, 1
    elif current_month <= 10:  # 8-10月，Q2数据应该可用
        return current_year, 2
    else:  # 11-12月，Q3数据应该可用
        return current_year, 3


def try_get_financial_data_with_fallback(
    data_source: FinancialDataSource,
    code: str,
    data_type: str,
    max_attempts: int = 4
) -> Tuple[Optional[Any], Optional[int], Optional[int]]:
    """
    尝试获取财务数据，如果失败则回退到上一季度
    
    Args:
        data_source: 数据源实例
        code: 股票代码
        data_type: 数据类型 ('profit', 'growth', 'balance', 'dupont', 'cash_flow')
        max_attempts: 最大尝试次数（季度数）
    
    Returns:
        Tuple[Optional[Any], Optional[int], Optional[int]]: (数据, 年份, 季度)
    """
    year, quarter = get_latest_available_quarter()
    
    for attempt in range(max_attempts):
        try:
            logger.info(f"尝试获取 {code} {year}年Q{quarter} {data_type} 数据 (第{attempt+1}次尝试)")
            
            # 根据数据类型调用相应的方法
            if data_type == "profit":
                data = data_source.get_profit_data(code, str(year), quarter)
            elif data_type == "growth":
                data = data_source.get_growth_data(code, str(year), quarter)
            elif data_type == "balance":
                data = data_source.get_balance_data(code, str(year), quarter)
            elif data_type == "dupont":
                data = data_source.get_dupont_data(code, str(year), quarter)
            elif data_type == "cash_flow":
                data = data_source.get_cash_flow_data(code, str(year), quarter)
            else:
                logger.error(f"不支持的数据类型: {data_type}")
                return None, None, None
            
            # 检查数据是否有效
            if data is not None and not data.empty and "暂无数据" not in str(data):
                logger.info(f"成功获取 {code} {year}年Q{quarter} {data_type} 数据")
                return data, year, quarter
            else:
                logger.warning(f"{code} {year}年Q{quarter} {data_type} 数据为空或无效")
                
        except Exception as e:
            logger.warning(f"获取 {code} {year}年Q{quarter} {data_type} 数据失败: {e}")
        
        # 回退到上一季度
        quarter -= 1
        if quarter < 1:
            quarter = 4
            year -= 1
        
        # 避免回退到过早的年份
        if year < datetime.now().year - 3:
            logger.warning(f"已回退到 {year} 年，停止尝试")
            break
    
    logger.error(f"无法获取 {code} 的 {data_type} 数据，已尝试 {max_attempts} 个季度")
    return None, None, None


def get_data_freshness_note(year: int, quarter: int) -> str:
    """
    生成数据时效性说明
    
    Args:
        year: 数据年份
        quarter: 数据季度
    
    Returns:
        str: 数据时效性说明文本
    """
    current_date = datetime.now()
    note = f"\n📊 **数据时效性说明**:\n"
    note += f"- 财务数据: {year}年第{quarter}季度（最新可用）\n"
    note += f"- 查询时间: {current_date.strftime('%Y-%m-%d')}\n"
    note += f"- 财务数据通常滞后1-3个月发布\n"
    
    # 计算数据新鲜度
    current_year = current_date.year
    current_quarter = (current_date.month - 1) // 3 + 1
    
    quarter_diff = (current_year - year) * 4 + (current_quarter - quarter)
    
    if quarter_diff <= 1:
        note += f"- 数据新鲜度: 最新 ✅\n"
    elif quarter_diff <= 2:
        note += f"- 数据新鲜度: 较新 ⚠️\n"
    else:
        note += f"- 数据新鲜度: 滞后{quarter_diff}个季度 ⚠️\n"
    
    note += "\n"
    return note


def format_financial_section(
    data: Any,
    section_title: str,
    year: int,
    quarter: int,
    field_mappings: dict
) -> str:
    """
    格式化财务数据段落
    
    Args:
        data: 财务数据
        section_title: 段落标题
        year: 数据年份
        quarter: 数据季度
        field_mappings: 字段映射字典 {字段名: 显示名称}
    
    Returns:
        str: 格式化的段落文本
    """
    if data is None or data.empty:
        return f"\n### {section_title}\n- 暂无数据（可能由于财报发布时间或数据源限制）\n"
    
    section = f"\n### {section_title}\n"
    
    for field, display_name in field_mappings.items():
        if field in data.columns:
            value = data[field].values[0]
            if value is not None and str(value) != 'nan' and str(value) != '':
                # 根据字段类型格式化数值
                if 'ratio' in field.lower() or 'margin' in field.lower() or 'roe' in field.lower():
                    section += f"- {display_name}: {value}%\n"
                elif 'profit' in field.lower() or 'asset' in field.lower():
                    section += f"- {display_name}: {value}万元\n"
                else:
                    section += f"- {display_name}: {value}\n"
    
    if section == f"\n### {section_title}\n":
        section += "- 暂无有效数据\n"
    
    return section