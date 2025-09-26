"""
工具函数模块

本模块提供了项目中使用的各种工具函数，主要包括：
- 日志配置管理
- Baostock数据源的登录上下文管理器
- 其他通用工具函数

主要功能:
- setup_logging(): 配置应用程序的日志系统
- baostock_login_context(): Baostock登录/登出的上下文管理器，自动处理连接生命周期

设计特点:
- 使用上下文管理器确保资源正确释放
- 抑制第三方库的冗余输出信息
- 统一的日志格式和级别管理
- 优雅的错误处理和异常传播

作者: StockReport MCP Project
许可证: MIT License
"""

import baostock as bs
import os
import sys
import logging
from contextlib import contextmanager
try:
    from .data_source_interface import LoginError
except ImportError:
    from data_source_interface import LoginError

# --- Logging Setup ---
def setup_logging(level=logging.INFO):
    """Configures basic logging for the application."""
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    # Optionally silence logs from dependencies if they are too verbose
    # logging.getLogger("mcp").setLevel(logging.WARNING)

# Get a logger instance for this module (optional, but good practice)
logger = logging.getLogger(__name__)

# --- Baostock Context Manager ---
@contextmanager
def baostock_login_context():
    """Context manager to handle Baostock login and logout, suppressing stdout messages."""
    # Redirect stdout to suppress login/logout messages
    original_stdout_fd = sys.stdout.fileno()
    saved_stdout_fd = os.dup(original_stdout_fd)
    devnull_fd = os.open(os.devnull, os.O_WRONLY)

    os.dup2(devnull_fd, original_stdout_fd)
    os.close(devnull_fd)

    logger.debug("Attempting Baostock login...")
    lg = bs.login()
    logger.debug(f"Login result: code={lg.error_code}, msg={lg.error_msg}")

    # Restore stdout
    os.dup2(saved_stdout_fd, original_stdout_fd)
    os.close(saved_stdout_fd)

    if lg.error_code != '0':
        # Log error before raising
        logger.error(f"Baostock login failed: {lg.error_msg}")
        raise LoginError(f"Baostock login failed: {lg.error_msg}")

    logger.info("Baostock login successful.")
    try:
        yield  # API calls happen here
    finally:
        # Redirect stdout again for logout
        original_stdout_fd = sys.stdout.fileno()
        saved_stdout_fd = os.dup(original_stdout_fd)
        devnull_fd = os.open(os.devnull, os.O_WRONLY)

        os.dup2(devnull_fd, original_stdout_fd)
        os.close(devnull_fd)

        logger.debug("Attempting Baostock logout...")
        bs.logout()
        logger.debug("Logout completed.")

        # Restore stdout
        os.dup2(saved_stdout_fd, original_stdout_fd)
        os.close(saved_stdout_fd)
        logger.info("Baostock logout successful.")

# You can add other utility functions or classes here if needed
