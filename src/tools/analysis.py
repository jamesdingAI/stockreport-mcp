"""
Analysis tools for MCP server.
Contains tools for generating stock analysis reports.
"""
import logging
from datetime import datetime, timedelta

from mcp.server.fastmcp import FastMCP
from src.data_source_interface import FinancialDataSource
from src.formatting.markdown_formatter import format_df_to_markdown
from src.tools.quarter_utils import (
    try_get_financial_data_with_fallback,
    get_data_freshness_note,
    format_financial_section
)

logger = logging.getLogger(__name__)


def register_analysis_tools(app: FastMCP, active_data_source: FinancialDataSource):
    """
    Register analysis tools with the MCP app.

    Args:
        app: The FastMCP app instance
        active_data_source: The active financial data source
    """

    @app.tool()
    def get_stock_analysis(code: str, analysis_type: str = "fundamental") -> str:
        """
        提供基于数据的股票分析报告，而非投资建议。

        Args:
            code: 股票代码，如'sh.600000'
            analysis_type: 分析类型，可选'fundamental'(基本面)、'technical'(技术面)或'comprehensive'(综合)

        Returns:
            数据驱动的分析报告，包含关键财务指标、历史表现和同行业比较
        """
        logger.info(
            f"Tool 'get_stock_analysis' called for {code}, type={analysis_type}")

        # 收集多个维度的实际数据
        try:
            # 获取基本信息
            basic_info = active_data_source.get_stock_basic_info(code=code)

            # 根据分析类型获取不同数据
            if analysis_type in ["fundamental", "comprehensive"]:
                # 使用智能季度回退机制获取最新可用的财务数据
                profit_data, data_year, data_quarter = try_get_financial_data_with_fallback(
                    active_data_source, code, "profit")
                growth_data, _, _ = try_get_financial_data_with_fallback(
                    active_data_source, code, "growth")
                balance_data, _, _ = try_get_financial_data_with_fallback(
                    active_data_source, code, "balance")
                dupont_data, _, _ = try_get_financial_data_with_fallback(
                    active_data_source, code, "dupont")

            if analysis_type in ["technical", "comprehensive"]:
                # 获取历史价格
                end_date = datetime.now().strftime("%Y-%m-%d")
                start_date = (datetime.now() - timedelta(days=180)
                              ).strftime("%Y-%m-%d")
                price_data = active_data_source.get_historical_k_data(
                    code=code, start_date=start_date, end_date=end_date
                )

            # 构建客观的数据分析报告
            report = f"# {basic_info['code_name'].values[0] if not basic_info.empty else code} 数据分析报告\n\n"
            report += "## 免责声明\n本报告基于公开数据生成，仅供参考，不构成投资建议。投资决策需基于个人风险承受能力和研究。\n\n"

            # 添加行业信息
            if not basic_info.empty:
                report += f"## 公司基本信息\n"
                report += f"- 股票代码: {code}\n"
                report += f"- 股票名称: {basic_info['code_name'].values[0]}\n"
                report += f"- 所属行业: {basic_info['industry'].values[0] if 'industry' in basic_info.columns else '未知'}\n"
                report += f"- 上市日期: {basic_info['ipoDate'].values[0] if 'ipoDate' in basic_info.columns else '未知'}\n\n"

            # 添加基本面分析
            if analysis_type in ["fundamental", "comprehensive"]:
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

                    # 偿债能力指标
                    balance_mappings = {
                        'currentRatio': '流动比率',
                        'assetLiabRatio': '资产负债率',
                        'quickRatio': '速动比率',
                        'cashRatio': '现金比率'
                    }
                    report += format_financial_section(
                        balance_data, "偿债能力指标", data_year, data_quarter, balance_mappings)
                else:
                    report += "## 基本面指标分析\n\n"
                    report += "⚠️ **数据获取失败**: 无法获取最新的财务数据，可能原因：\n"
                    report += "- 财务数据尚未发布（通常滞后1-3个月）\n"
                    report += "- 数据源暂时不可用\n"
                    report += "- 股票代码可能有误\n\n"

            # 添加技术面分析
            if analysis_type in ["technical", "comprehensive"] and not price_data.empty:
                report += "## 技术面分析\n\n"

                # 计算简单的技术指标
                # 假设price_data已经按日期排序
                if 'close' in price_data.columns and len(price_data) > 1:
                    latest_price = price_data['close'].iloc[-1]
                    start_price = price_data['close'].iloc[0]
                    price_change = (
                        (float(latest_price) / float(start_price)) - 1) * 100

                    report += f"- 最新收盘价: {latest_price}\n"
                    report += f"- 6个月价格变动: {price_change:.2f}%\n"

                    # 计算简单的均线
                    if len(price_data) >= 20:
                        ma20 = price_data['close'].astype(
                            float).tail(20).mean()
                        report += f"- 20日均价: {ma20:.2f}\n"
                        if float(latest_price) > ma20:
                            report += f"  (当前价格高于20日均线 {((float(latest_price)/ma20)-1)*100:.2f}%)\n"
                        else:
                            report += f"  (当前价格低于20日均线 {((ma20/float(latest_price))-1)*100:.2f}%)\n"

            # 添加行业比较分析
            try:
                if not basic_info.empty and 'industry' in basic_info.columns:
                    industry = basic_info['industry'].values[0]
                    industry_stocks = active_data_source.get_stock_industry(
                        date=None)
                    if not industry_stocks.empty:
                        same_industry = industry_stocks[industry_stocks['industry'] == industry]
                        report += f"\n## 行业比较 ({industry})\n"
                        report += f"- 同行业股票数量: {len(same_industry)}\n"

                        # 这里可以添加更多行业比较数据
            except Exception as e:
                logger.warning(f"获取行业比较数据失败: {e}")

            report += "\n## 数据解读建议\n"
            report += "- 以上数据仅供参考，建议结合公司公告、行业趋势和宏观环境进行综合分析\n"
            report += "- 个股表现受多种因素影响，历史数据不代表未来表现\n"
            report += "- 投资决策应基于个人风险承受能力和投资目标\n"

            logger.info(f"成功生成{code}的分析报告")
            return report

        except Exception as e:
            logger.exception(f"分析生成失败 for {code}: {e}")
            return f"分析生成失败: {e}"
