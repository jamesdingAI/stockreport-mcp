"""
Financial report related tools for MCP server.
"""
import logging
from typing import List, Optional

from mcp.server.fastmcp import FastMCP
from src.data_source_interface import FinancialDataSource
from src.tools.base import call_financial_data_tool

logger = logging.getLogger(__name__)


def register_financial_report_tools(app: FastMCP, active_data_source: FinancialDataSource):
    """
    Register financial report related tools with the MCP app.

    Args:
        app: The FastMCP app instance
        active_data_source: The active financial data source
    """

    @app.tool()
    def get_profit_data(code: str, year: str, quarter: int) -> str:
        """
        Fetches quarterly profitability data (e.g., ROE, net profit margin) for a stock.

        Args:
            code: The stock code (e.g., 'sh.600000').
            year: The 4-digit year (e.g., '2023').
            quarter: The quarter (1, 2, 3, or 4).

        Returns:
            Markdown table with profitability data or an error message.
        """
        return call_financial_data_tool(
            "get_profit_data",
            active_data_source.get_profit_data,
            "Profitability",
            code, year, quarter
        )

    @app.tool()
    def get_operation_data(code: str, year: str, quarter: int) -> str:
        """
        Fetches quarterly operation capability data (e.g., turnover ratios) for a stock.

        Args:
            code: The stock code (e.g., 'sh.600000').
            year: The 4-digit year (e.g., '2023').
            quarter: The quarter (1, 2, 3, or 4).

        Returns:
            Markdown table with operation capability data or an error message.
        """
        return call_financial_data_tool(
            "get_operation_data",
            active_data_source.get_operation_data,
            "Operation Capability",
            code, year, quarter
        )

    @app.tool()
    def get_growth_data(code: str, year: str, quarter: int) -> str:
        """
        Fetches quarterly growth capability data (e.g., YOY growth rates) for a stock.

        Args:
            code: The stock code (e.g., 'sh.600000').
            year: The 4-digit year (e.g., '2023').
            quarter: The quarter (1, 2, 3, or 4).

        Returns:
            Markdown table with growth capability data or an error message.
        """
        return call_financial_data_tool(
            "get_growth_data",
            active_data_source.get_growth_data,
            "Growth Capability",
            code, year, quarter
        )

    @app.tool()
    def get_balance_data(code: str, year: str, quarter: int) -> str:
        """
        Fetches quarterly balance sheet / solvency data (e.g., current ratio, debt ratio) for a stock.

        Args:
            code: The stock code (e.g., 'sh.600000').
            year: The 4-digit year (e.g., '2023').
            quarter: The quarter (1, 2, 3, or 4).

        Returns:
            Markdown table with balance sheet data or an error message.
        """
        return call_financial_data_tool(
            "get_balance_data",
            active_data_source.get_balance_data,
            "Balance Sheet",
            code, year, quarter
        )

    @app.tool()
    def get_cash_flow_data(code: str, year: str, quarter: int) -> str:
        """
        Fetches quarterly cash flow data (e.g., CFO/Operating Revenue ratio) for a stock.

        Args:
            code: The stock code (e.g., 'sh.600000').
            year: The 4-digit year (e.g., '2023').
            quarter: The quarter (1, 2, 3, or 4).

        Returns:
            Markdown table with cash flow data or an error message.
        """
        return call_financial_data_tool(
            "get_cash_flow_data",
            active_data_source.get_cash_flow_data,
            "Cash Flow",
            code, year, quarter
        )

    @app.tool()
    def get_dupont_data(code: str, year: str, quarter: int) -> str:
        """
        Fetches quarterly DuPont analysis data (ROE decomposition) for a stock.

        Args:
            code: The stock code (e.g., 'sh.600000').
            year: The 4-digit year (e.g., '2023').
            quarter: The quarter (1, 2, 3, or 4).

        Returns:
            Markdown table with DuPont analysis data or an error message.
        """
        return call_financial_data_tool(
            "get_dupont_data",
            active_data_source.get_dupont_data,
            "DuPont Analysis",
            code, year, quarter
        )

    @app.tool()
    def get_performance_express_report(code: str, start_date: str, end_date: str) -> str:
        """
        Fetches performance express reports (业绩快报) for a stock within a date range.
        Note: Companies are not required to publish these except in specific cases.

        Args:
            code: The stock code (e.g., 'sh.600000').
            start_date: Start date (for report publication/update) in 'YYYY-MM-DD' format.
            end_date: End date (for report publication/update) in 'YYYY-MM-DD' format.

        Returns:
            Markdown table with performance express report data or an error message.
        """
        logger.info(
            f"Tool 'get_performance_express_report' called for {code} ({start_date} to {end_date})")
        try:
            # Add date validation if desired
            df = active_data_source.get_performance_express_report(
                code=code, start_date=start_date, end_date=end_date)
            logger.info(
                f"Successfully retrieved performance express reports for {code}.")
            from src.formatting.markdown_formatter import format_df_to_markdown
            return format_df_to_markdown(df)

        except Exception as e:
            logger.exception(
                f"Exception processing get_performance_express_report for {code}: {e}")
            return f"Error: An unexpected error occurred: {e}"

    @app.tool()
    def get_forecast_report(code: str, start_date: str, end_date: str) -> str:
        """
        Fetches performance forecast reports (业绩预告) for a stock within a date range.
        Note: Companies are not required to publish these except in specific cases.

        Args:
            code: The stock code (e.g., 'sh.600000').
            start_date: Start date (for report publication/update) in 'YYYY-MM-DD' format.
            end_date: End date (for report publication/update) in 'YYYY-MM-DD' format.

        Returns:
            Markdown table with performance forecast report data or an error message.
        """
        logger.info(
            f"Tool 'get_forecast_report' called for {code} ({start_date} to {end_date})")
        try:
            # Add date validation if desired
            df = active_data_source.get_forecast_report(
                code=code, start_date=start_date, end_date=end_date)
            logger.info(
                f"Successfully retrieved performance forecast reports for {code}.")
            from src.formatting.markdown_formatter import format_df_to_markdown
            return format_df_to_markdown(df)

        except Exception as e:
            logger.exception(
                f"Exception processing get_forecast_report for {code}: {e}")
            return f"Error: An unexpected error occurred: {e}"
