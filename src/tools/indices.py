"""
Index related tools for MCP server.
Contains tools for fetching index constituent stocks.
"""
import logging
from typing import Optional

from mcp.server.fastmcp import FastMCP
from src.data_source_interface import FinancialDataSource
from src.tools.base import call_index_constituent_tool

logger = logging.getLogger(__name__)


def register_index_tools(app: FastMCP, active_data_source: FinancialDataSource):
    """
    Register index related tools with the MCP app.

    Args:
        app: The FastMCP app instance
        active_data_source: The active financial data source
    """

    @app.tool()
    def get_stock_industry(code: Optional[str] = None, date: Optional[str] = None) -> str:
        """
        Fetches industry classification for a specific stock or all stocks on a given date.

        Args:
            code: Optional. The stock code (e.g., 'sh.600000'). If None, fetches for all stocks.
            date: Optional. The date in 'YYYY-MM-DD' format. If None, uses the latest available date.

        Returns:
            Markdown table with industry classification data or an error message.
        """
        log_msg = f"Tool 'get_stock_industry' called for code={code or 'all'}, date={date or 'latest'}"
        logger.info(log_msg)
        try:
            # Add date validation if desired
            df = active_data_source.get_stock_industry(code=code, date=date)
            logger.info(
                f"Successfully retrieved industry data for {code or 'all'}, {date or 'latest'}.")
            from src.formatting.markdown_formatter import format_df_to_markdown
            return format_df_to_markdown(df)

        except Exception as e:
            logger.exception(
                f"Exception processing get_stock_industry: {e}")
            return f"Error: An unexpected error occurred: {e}"

    @app.tool()
    def get_sz50_stocks(date: Optional[str] = None) -> str:
        """
        Fetches the constituent stocks of the SZSE 50 Index for a given date.

        Args:
            date: Optional. The date in 'YYYY-MM-DD' format. If None, uses the latest available date.

        Returns:
            Markdown table with SZSE 50 constituent stocks or an error message.
        """
        return call_index_constituent_tool(
            "get_sz50_stocks",
            active_data_source.get_sz50_stocks,
            "SZSE 50",
            date
        )

    @app.tool()
    def get_hs300_stocks(date: Optional[str] = None) -> str:
        """
        Fetches the constituent stocks of the CSI 300 Index for a given date.

        Args:
            date: Optional. The date in 'YYYY-MM-DD' format. If None, uses the latest available date.

        Returns:
            Markdown table with CSI 300 constituent stocks or an error message.
        """
        return call_index_constituent_tool(
            "get_hs300_stocks",
            active_data_source.get_hs300_stocks,
            "CSI 300",
            date
        )

    @app.tool()
    def get_zz500_stocks(date: Optional[str] = None) -> str:
        """
        Fetches the constituent stocks of the CSI 500 Index for a given date.

        Args:
            date: Optional. The date in 'YYYY-MM-DD' format. If None, uses the latest available date.

        Returns:
            Markdown table with CSI 500 constituent stocks or an error message.
        """
        return call_index_constituent_tool(
            "get_zz500_stocks",
            active_data_source.get_zz500_stocks,
            "CSI 500",
            date
        )
