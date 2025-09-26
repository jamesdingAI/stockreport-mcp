"""
Stock market data tools for MCP server.
"""
import logging
from typing import List, Optional

from mcp.server.fastmcp import FastMCP
from src.data_source_interface import FinancialDataSource, NoDataFoundError, LoginError, DataSourceError
from src.formatting.markdown_formatter import format_df_to_markdown

logger = logging.getLogger(__name__)


def register_stock_market_tools(app: FastMCP, active_data_source: FinancialDataSource):
    """
    Register stock market data tools with the MCP app.

    Args:
        app: The FastMCP app instance
        active_data_source: The active financial data source
    """

    @app.tool()
    def get_historical_k_data(
        code: str,
        start_date: str,
        end_date: str,
        frequency: str = "d",
        adjust_flag: str = "3",
        fields: Optional[List[str]] = None,
    ) -> str:
        """
        Fetches historical K-line (OHLCV) data for a Chinese A-share stock.

        Args:
            code: The stock code in Baostock format (e.g., 'sh.600000', 'sz.000001').
            start_date: Start date in 'YYYY-MM-DD' format.
            end_date: End date in 'YYYY-MM-DD' format.
            frequency: Data frequency. Valid options (from Baostock):
                         'd': daily
                         'w': weekly
                         'm': monthly
                         '5': 5 minutes
                         '15': 15 minutes
                         '30': 30 minutes
                         '60': 60 minutes
                       Defaults to 'd'.
            adjust_flag: Adjustment flag for price/volume. Valid options (from Baostock):
                           '1': Forward adjusted (后复权)
                           '2': Backward adjusted (前复权)
                           '3': Non-adjusted (不复权)
                         Defaults to '3'.
            fields: Optional list of specific data fields to retrieve (must be valid Baostock fields).
                    If None or empty, default fields will be used (e.g., date, code, open, high, low, close, volume, amount, pctChg).

        Returns:
            A Markdown formatted string containing the K-line data table, or an error message.
            The table might be truncated if the result set is too large.
        """
        logger.info(
            f"Tool 'get_historical_k_data' called for {code} ({start_date}-{end_date}, freq={frequency}, adj={adjust_flag}, fields={fields})")
        try:
            # Validate frequency and adjust_flag if necessary (basic example)
            valid_freqs = ['d', 'w', 'm', '5', '15', '30', '60']
            valid_adjusts = ['1', '2', '3']
            if frequency not in valid_freqs:
                logger.warning(f"Invalid frequency requested: {frequency}")
                return f"Error: Invalid frequency '{frequency}'. Valid options are: {valid_freqs}"
            if adjust_flag not in valid_adjusts:
                logger.warning(f"Invalid adjust_flag requested: {adjust_flag}")
                return f"Error: Invalid adjust_flag '{adjust_flag}'. Valid options are: {valid_adjusts}"

            # Call the injected data source
            df = active_data_source.get_historical_k_data(
                code=code,
                start_date=start_date,
                end_date=end_date,
                frequency=frequency,
                adjust_flag=adjust_flag,
                fields=fields,
            )
            # Format the result
            logger.info(
                f"Successfully retrieved K-data for {code}, formatting to Markdown.")
            return format_df_to_markdown(df)

        except NoDataFoundError as e:
            logger.warning(f"NoDataFoundError for {code}: {e}")
            return f"Error: {e}"
        except LoginError as e:
            logger.error(f"LoginError for {code}: {e}")
            return f"Error: Could not connect to data source. {e}"
        except DataSourceError as e:
            logger.error(f"DataSourceError for {code}: {e}")
            return f"Error: An error occurred while fetching data. {e}"
        except ValueError as e:
            logger.warning(f"ValueError processing request for {code}: {e}")
            return f"Error: Invalid input parameter. {e}"
        except Exception as e:
            # Catch-all for unexpected errors
            logger.exception(
                f"Unexpected Exception processing get_historical_k_data for {code}: {e}")
            return f"Error: An unexpected error occurred: {e}"

    @app.tool()
    def get_stock_basic_info(code: str, fields: Optional[List[str]] = None) -> str:
        """
        Fetches basic information for a given Chinese A-share stock.

        Args:
            code: The stock code in Baostock format (e.g., 'sh.600000', 'sz.000001').
            fields: Optional list to select specific columns from the available basic info
                    (e.g., ['code', 'code_name', 'industry', 'listingDate']).
                    If None or empty, returns all available basic info columns from Baostock.

        Returns:
            A Markdown formatted string containing the basic stock information table,
            or an error message.
        """
        logger.info(
            f"Tool 'get_stock_basic_info' called for {code} (fields={fields})")
        try:
            # Call the injected data source
            # Pass fields along; BaostockDataSource implementation handles selection
            df = active_data_source.get_stock_basic_info(
                code=code, fields=fields)

            # Format the result (basic info usually small, use default truncation)
            logger.info(
                f"Successfully retrieved basic info for {code}, formatting to Markdown.")
            # Smaller limits for basic info
            return format_df_to_markdown(df)

        except NoDataFoundError as e:
            logger.warning(f"NoDataFoundError for {code}: {e}")
            return f"Error: {e}"
        except LoginError as e:
            logger.error(f"LoginError for {code}: {e}")
            return f"Error: Could not connect to data source. {e}"
        except DataSourceError as e:
            logger.error(f"DataSourceError for {code}: {e}")
            return f"Error: An error occurred while fetching data. {e}"
        except ValueError as e:
            logger.warning(f"ValueError processing request for {code}: {e}")
            return f"Error: Invalid input parameter or requested field not available. {e}"
        except Exception as e:
            logger.exception(
                f"Unexpected Exception processing get_stock_basic_info for {code}: {e}")
            return f"Error: An unexpected error occurred: {e}"

    @app.tool()
    def get_dividend_data(code: str, year: str, year_type: str = "report") -> str:
        """
        Fetches dividend information for a given stock code and year.

        Args:
            code: The stock code in Baostock format (e.g., 'sh.600000', 'sz.000001').
            year: The year to query (e.g., '2023').
            year_type: Type of year. Valid options (from Baostock):
                         'report': Announcement year (预案公告年份)
                         'operate': Ex-dividend year (除权除息年份)
                       Defaults to 'report'.

        Returns:
            A Markdown formatted string containing the dividend data table,
            or an error message.
        """
        logger.info(
            f"Tool 'get_dividend_data' called for {code}, year={year}, year_type={year_type}")
        try:
            # Basic validation
            if year_type not in ['report', 'operate']:
                logger.warning(f"Invalid year_type requested: {year_type}")
                return f"Error: Invalid year_type '{year_type}'. Valid options are: 'report', 'operate'"
            if not year.isdigit() or len(year) != 4:
                logger.warning(f"Invalid year format requested: {year}")
                return f"Error: Invalid year '{year}'. Please provide a 4-digit year."

            df = active_data_source.get_dividend_data(
                code=code, year=year, year_type=year_type)
            logger.info(
                f"Successfully retrieved dividend data for {code}, year {year}.")
            return format_df_to_markdown(df)

        except NoDataFoundError as e:
            logger.warning(f"NoDataFoundError for {code}, year {year}: {e}")
            return f"Error: {e}"
        except LoginError as e:
            logger.error(f"LoginError for {code}: {e}")
            return f"Error: Could not connect to data source. {e}"
        except DataSourceError as e:
            logger.error(f"DataSourceError for {code}: {e}")
            return f"Error: An error occurred while fetching data. {e}"
        except ValueError as e:
            logger.warning(f"ValueError processing request for {code}: {e}")
            return f"Error: Invalid input parameter. {e}"
        except Exception as e:
            logger.exception(
                f"Unexpected Exception processing get_dividend_data for {code}: {e}")
            return f"Error: An unexpected error occurred: {e}"

    @app.tool()
    def get_adjust_factor_data(code: str, start_date: str, end_date: str) -> str:
        """
        Fetches adjustment factor data for a given stock code and date range.
        Uses Baostock's "涨跌幅复权算法" factors. Useful for calculating adjusted prices.

        Args:
            code: The stock code in Baostock format (e.g., 'sh.600000', 'sz.000001').
            start_date: Start date in 'YYYY-MM-DD' format.
            end_date: End date in 'YYYY-MM-DD' format.

        Returns:
            A Markdown formatted string containing the adjustment factor data table,
            or an error message.
        """
        logger.info(
            f"Tool 'get_adjust_factor_data' called for {code} ({start_date} to {end_date})")
        try:
            # Basic date validation could be added here if desired
            df = active_data_source.get_adjust_factor_data(
                code=code, start_date=start_date, end_date=end_date)
            logger.info(
                f"Successfully retrieved adjustment factor data for {code}.")
            return format_df_to_markdown(df)

        except NoDataFoundError as e:
            logger.warning(f"NoDataFoundError for {code}: {e}")
            return f"Error: {e}"
        except LoginError as e:
            logger.error(f"LoginError for {code}: {e}")
            return f"Error: Could not connect to data source. {e}"
        except DataSourceError as e:
            logger.error(f"DataSourceError for {code}: {e}")
            return f"Error: An error occurred while fetching data. {e}"
        except ValueError as e:
            logger.warning(f"ValueError processing request for {code}: {e}")
            return f"Error: Invalid input parameter. {e}"
        except Exception as e:
            logger.exception(
                f"Unexpected Exception processing get_adjust_factor_data for {code}: {e}")
            return f"Error: An unexpected error occurred: {e}"
