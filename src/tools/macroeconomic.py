"""
Macroeconomic data tools for MCP server.
Contains tools for fetching interest rates, money supply data, and more.
"""
import logging
from typing import Optional

from mcp.server.fastmcp import FastMCP
from src.data_source_interface import FinancialDataSource
from src.tools.base import call_macro_data_tool

logger = logging.getLogger(__name__)


def register_macroeconomic_tools(app: FastMCP, active_data_source: FinancialDataSource):
    """
    Register macroeconomic data tools with the MCP app.

    Args:
        app: The FastMCP app instance
        active_data_source: The active financial data source
    """

    @app.tool()
    def get_deposit_rate_data(start_date: Optional[str] = None, end_date: Optional[str] = None) -> str:
        """
        Fetches benchmark deposit rates (活期, 定期) within a date range.

        Args:
            start_date: Optional. Start date in 'YYYY-MM-DD' format.
            end_date: Optional. End date in 'YYYY-MM-DD' format.

        Returns:
            Markdown table with deposit rate data or an error message.
        """
        return call_macro_data_tool(
            "get_deposit_rate_data",
            active_data_source.get_deposit_rate_data,
            "Deposit Rate",
            start_date, end_date
        )

    @app.tool()
    def get_loan_rate_data(start_date: Optional[str] = None, end_date: Optional[str] = None) -> str:
        """
        Fetches benchmark loan rates (贷款利率) within a date range.

        Args:
            start_date: Optional. Start date in 'YYYY-MM-DD' format.
            end_date: Optional. End date in 'YYYY-MM-DD' format.

        Returns:
            Markdown table with loan rate data or an error message.
        """
        return call_macro_data_tool(
            "get_loan_rate_data",
            active_data_source.get_loan_rate_data,
            "Loan Rate",
            start_date, end_date
        )

    @app.tool()
    def get_required_reserve_ratio_data(start_date: Optional[str] = None, end_date: Optional[str] = None, year_type: str = '0') -> str:
        """
        Fetches required reserve ratio data (存款准备金率) within a date range.

        Args:
            start_date: Optional. Start date in 'YYYY-MM-DD' format.
            end_date: Optional. End date in 'YYYY-MM-DD' format.
            year_type: Optional. Year type for date filtering. '0' for announcement date (公告日期, default),
                    '1' for effective date (生效日期).

        Returns:
            Markdown table with required reserve ratio data or an error message.
        """
        # Basic validation for year_type
        if year_type not in ['0', '1']:
            logger.warning(f"Invalid year_type requested: {year_type}")
            return "Error: Invalid year_type '{year_type}'. Valid options are '0' (announcement date) or '1' (effective date)."

        return call_macro_data_tool(
            "get_required_reserve_ratio_data",
            active_data_source.get_required_reserve_ratio_data,
            "Required Reserve Ratio",
            start_date, end_date,
            yearType=year_type  # Pass the extra arg correctly named for Baostock
        )

    @app.tool()
    def get_money_supply_data_month(start_date: Optional[str] = None, end_date: Optional[str] = None) -> str:
        """
        Fetches monthly money supply data (M0, M1, M2) within a date range.

        Args:
            start_date: Optional. Start date in 'YYYY-MM' format.
            end_date: Optional. End date in 'YYYY-MM' format.

        Returns:
            Markdown table with monthly money supply data or an error message.
        """
        # Add specific validation for YYYY-MM format if desired
        return call_macro_data_tool(
            "get_money_supply_data_month",
            active_data_source.get_money_supply_data_month,
            "Monthly Money Supply",
            start_date, end_date
        )

    @app.tool()
    def get_money_supply_data_year(start_date: Optional[str] = None, end_date: Optional[str] = None) -> str:
        """
        Fetches yearly money supply data (M0, M1, M2 - year end balance) within a date range.

        Args:
            start_date: Optional. Start year in 'YYYY' format.
            end_date: Optional. End year in 'YYYY' format.

        Returns:
            Markdown table with yearly money supply data or an error message.
        """
        # Add specific validation for YYYY format if desired
        return call_macro_data_tool(
            "get_money_supply_data_year",
            active_data_source.get_money_supply_data_year,
            "Yearly Money Supply",
            start_date, end_date
        )

    @app.tool()
    def get_shibor_data(start_date: Optional[str] = None, end_date: Optional[str] = None) -> str:
        """
        Fetches SHIBOR (Shanghai Interbank Offered Rate) data within a date range.

        Args:
            start_date: Optional. Start date in 'YYYY-MM-DD' format.
            end_date: Optional. End date in 'YYYY-MM-DD' format.

        Returns:
            Markdown table with SHIBOR data or an error message.
        """
        return call_macro_data_tool(
            "get_shibor_data",
            active_data_source.get_shibor_data,
            "SHIBOR",
            start_date, end_date
        )
