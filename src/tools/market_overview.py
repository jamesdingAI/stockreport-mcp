"""
Market overview tools for MCP server.
Contains tools for fetching trading dates and all stock data.
"""
import logging
from typing import Optional

from mcp.server.fastmcp import FastMCP
from src.data_source_interface import FinancialDataSource, NoDataFoundError, LoginError, DataSourceError
from src.formatting.markdown_formatter import format_df_to_markdown

logger = logging.getLogger(__name__)


def register_market_overview_tools(app: FastMCP, active_data_source: FinancialDataSource):
    """
    Register market overview tools with the MCP app.

    Args:
        app: The FastMCP app instance
        active_data_source: The active financial data source
    """

    @app.tool()
    def get_trade_dates(start_date: Optional[str] = None, end_date: Optional[str] = None) -> str:
        """
        Fetches trading dates information within a specified range.

        Args:
            start_date: Optional. Start date in 'YYYY-MM-DD' format. Defaults to 2015-01-01 if None.
            end_date: Optional. End date in 'YYYY-MM-DD' format. Defaults to the current date if None.

        Returns:
            Markdown table indicating whether each date in the range was a trading day (1) or not (0).
        """
        logger.info(
            f"Tool 'get_trade_dates' called for range {start_date or 'default'} to {end_date or 'default'}")
        try:
            # Add date validation if desired
            df = active_data_source.get_trade_dates(
                start_date=start_date, end_date=end_date)
            logger.info("Successfully retrieved trade dates.")
            # Trade dates table can be long, apply standard truncation
            return format_df_to_markdown(df)

        except NoDataFoundError as e:
            logger.warning(f"NoDataFoundError: {e}")
            return f"Error: {e}"
        except LoginError as e:
            logger.error(f"LoginError: {e}")
            return f"Error: Could not connect to data source. {e}"
        except DataSourceError as e:
            logger.error(f"DataSourceError: {e}")
            return f"Error: An error occurred while fetching data. {e}"
        except ValueError as e:
            logger.warning(f"ValueError: {e}")
            return f"Error: Invalid input parameter. {e}"
        except Exception as e:
            logger.exception(
                f"Unexpected Exception processing get_trade_dates: {e}")
            return f"Error: An unexpected error occurred: {e}"

    @app.tool()
    def get_all_stock(date: Optional[str] = None) -> str:
        """
        Fetches a list of all stocks (A-shares and indices) and their trading status for a given date.

        Args:
            date: Optional. The date in 'YYYY-MM-DD' format. If None, uses the current date.

        Returns:
            Markdown table listing stock codes, names, and their trading status (1=trading, 0=suspended).
        """
        logger.info(
            f"Tool 'get_all_stock' called for date={date or 'default'}")
        try:
            # Add date validation if desired
            df = active_data_source.get_all_stock(date=date)
            logger.info(
                f"Successfully retrieved stock list for {date or 'default'}.")
            # This list can be very long, apply standard truncation
            return format_df_to_markdown(df)

        except NoDataFoundError as e:
            logger.warning(f"NoDataFoundError: {e}")
            return f"Error: {e}"
        except LoginError as e:
            logger.error(f"LoginError: {e}")
            return f"Error: Could not connect to data source. {e}"
        except DataSourceError as e:
            logger.error(f"DataSourceError: {e}")
            return f"Error: An error occurred while fetching data. {e}"
        except ValueError as e:
            logger.warning(f"ValueError: {e}")
            return f"Error: Invalid input parameter. {e}"
        except Exception as e:
            logger.exception(
                f"Unexpected Exception processing get_all_stock: {e}")
            return f"Error: An unexpected error occurred: {e}"
