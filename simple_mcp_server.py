#!/usr/bin/env python3
"""
简化版MCP服务器 - 用于快速测试和演示

这是一个简化版的MCP服务器，专门用于快速测试股票数据查询功能。
相比完整版服务器，这个版本只包含核心的股票查询功能，启动更快，
适合用于演示和调试。

主要功能:
- 股票基本信息查询
- 历史K线数据获取
- 支持多种数据源

支持的数据源:
- Baostock: 专注A股数据，稳定可靠
- AkShare: 支持A股、港股、美股数据

使用示例:
    python simple_mcp_server.py --stock 000001 --source akshare

作者: StockReport MCP Project
版本: 1.0.0
许可证: MIT License
"""
import json
import sys
import logging
import argparse
from datetime import datetime

# 尝试导入数据源
try:
    from src.akshare_data_source import AkshareDataSource
    AKSHARE_AVAILABLE = True
except ImportError:
    AKSHARE_AVAILABLE = False
    print("⚠️ AkShare 不可用")

try:
    from src.baostock_data_source import BaostockDataSource
    BAOSTOCK_AVAILABLE = True
except ImportError:
    BAOSTOCK_AVAILABLE = False
    print("⚠️ Baostock 不可用")

def setup_logging(level=logging.INFO):
    """设置日志"""
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def create_data_source(source_type: str):
    """创建数据源"""
    if source_type.lower() == "akshare" and AKSHARE_AVAILABLE:
        return AkshareDataSource()
    elif source_type.lower() == "baostock" and BAOSTOCK_AVAILABLE:
        return BaostockDataSource()
    else:
        raise ValueError(f"不支持的数据源: {source_type}")

def get_stock_info(data_source, stock_code: str):
    """获取股票信息"""
    try:
        # 获取股票基本信息
        basic_info = data_source.get_stock_basic_info(stock_code)
        
        # 获取最新价格
        latest_data = data_source.get_historical_k_data(
            stock_code, 
            start_date="2024-01-01", 
            end_date=datetime.now().strftime("%Y-%m-%d")
        )
        
        # 转换为JSON可序列化的格式
        basic_info_dict = basic_info.to_dict() if hasattr(basic_info, 'to_dict') else str(basic_info)
        latest_data_dict = latest_data.tail(5).to_dict() if hasattr(latest_data, 'to_dict') else str(latest_data)
        
        # 处理日期类型
        if isinstance(basic_info_dict, dict):
            for key, value in basic_info_dict.items():
                if hasattr(value, 'strftime'):  # 日期类型
                    basic_info_dict[key] = value.strftime('%Y-%m-%d')
                elif hasattr(value, 'isoformat'):  # datetime类型
                    basic_info_dict[key] = value.isoformat()
        
        if isinstance(latest_data_dict, dict):
            for key, value in latest_data_dict.items():
                if isinstance(value, dict):
                    for k, v in value.items():
                        if hasattr(v, 'strftime'):
                            value[k] = v.strftime('%Y-%m-%d')
                        elif hasattr(v, 'isoformat'):
                            value[k] = v.isoformat()
        
        result = {
            "stock_code": stock_code,
            "basic_info": basic_info_dict,
            "latest_data": latest_data_dict
        }
        
        return result
    except Exception as e:
        return {"error": str(e)}

def main():
    parser = argparse.ArgumentParser(description="简化的StockReport MCP服务器")
    parser.add_argument("--data-source", choices=["akshare", "baostock"], 
                       default="akshare", help="数据源选择")
    parser.add_argument("--stock", help="股票代码 (测试用)")
    parser.add_argument("--test", action="store_true", help="运行测试")
    
    args = parser.parse_args()
    
    setup_logging()
    logger = logging.getLogger(__name__)
    
    print("🚀 简化的StockReport MCP服务器")
    print("=" * 50)
    print(f"数据源: {args.data_source.upper()}")
    
    # 检查数据源可用性
    if args.data_source == "akshare" and not AKSHARE_AVAILABLE:
        print("❌ AkShare 不可用，请安装: pip install akshare")
        return
    elif args.data_source == "baostock" and not BAOSTOCK_AVAILABLE:
        print("❌ Baostock 不可用，请安装: pip install baostock")
        return
    
    try:
        data_source = create_data_source(args.data_source)
        print("✅ 数据源初始化成功")
        
        if args.test or args.stock:
            # 测试模式
            test_stock = args.stock or "000001"
            print(f"\n🔍 测试股票: {test_stock}")
            
            result = get_stock_info(data_source, test_stock)
            print("\n📊 结果:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            # 服务器模式
            print("\n🔄 服务器启动成功")
            print("💡 这是一个简化版本，主要用于测试数据源连接")
            print("📝 要使用完整的MCP功能，请解决FastMCP依赖问题")
            
            # 简单的交互式查询
            while True:
                try:
                    stock_code = input("\n请输入股票代码 (或 'quit' 退出): ").strip()
                    if stock_code.lower() in ['quit', 'exit', 'q']:
                        break
                    
                    if stock_code:
                        result = get_stock_info(data_source, stock_code)
                        print(json.dumps(result, indent=2, ensure_ascii=False))
                        
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    print(f"❌ 错误: {e}")
            
            print("\n👋 服务器已停止")
            
    except Exception as e:
        logger.error(f"服务器启动失败: {e}")
        print(f"❌ 启动失败: {e}")

if __name__ == "__main__":
    main()