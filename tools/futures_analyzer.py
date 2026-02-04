"""
期货数据分析类 - 基于akshare数据库

功能:
1. 获取指定期货品种的历史数据
2. 计算重要技术指标
3. 输出最近30天的数据

作者: 专业期货数据分析师
依赖: akshare, pandas, numpy
"""

import akshare as ak
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union
import json


class FuturesAnalyzer:
    """
    期货数据分析类 - 基于akshare数据库
    
    功能:
    1. 获取指定期货品种的历史数据
    2. 计算重要技术指标
    3. 输出最近30天的数据
    
    参数:
        symbol (str): 期货品种代码, 如 "pb" (铅), "rb" (螺纹钢), "cu" (铜) 等
        
    示例:
        >>> analyzer = FuturesAnalyzer("pb")
        >>> recent_data = analyzer.get_recent_30_days()
        >>> indicators = analyzer.get_key_indicators()
    """
    
    # 品种代码到中文名称的映射 (用于东方财富接口)
    SYMBOL_TO_CHINESE = {
        'pb': '铅', 'rb': '螺纹钢', 'cu': '铜', 'al': '铝', 'zn': '锌', 'ni': '镍', 'sn': '锡',
        'au': '黄金', 'ag': '白银', 'hc': '热轧卷板', 'fu': '燃料油', 'bu': '石油沥青',
        'ru': '天然橡胶', 'br': '合成橡胶', 'sp': '纸浆', 'wr': '线材', 'ss': '不锈钢',
        'ao': '氧化铝',
        # 能源
        'sc': '原油', 'nr': '20号胶', 'lu': '低硫燃料油', 'bc': '国际铜',
        # 大连商品
        'm': '豆粕', 'y': '豆油', 'a': '豆一', 'b': '豆二', 'p': '棕榈油', 'c': '玉米',
        'cs': '玉米淀粉', 'l': '聚乙烯', 'v': 'PVC', 'pp': '聚丙烯', 'j': '焦炭',
        'jm': '焦煤', 'i': '铁矿石', 'fb': '纤维板', 'bb': '胶合板', 'eg': '乙二醇',
        'rr': '粳米', 'eb': '苯乙烯', 'pg': '液化石油气', 'lh': '生猪', 'lg': '原木',
        # 郑州商品
        'sr': '白砂糖', 'cf': '棉花', 'ta': 'PTA', 'oi': '菜籽油', 'rm': '菜粕',
        'ma': '甲醇', 'fg': '玻璃', 'zc': '动力煤', 'sf': '硅铁', 'sm': '锰硅',
        'cy': '棉纱', 'ap': '苹果', 'cj': '红枣', 'ur': '尿素', 'sa': '纯碱',
        'pf': '短纤', 'pk': '花生', 'px': '对二甲苯', 'sh': '烧碱', 'pr': '瓶片',
        # 广州期货
        'si': '工业硅', 'lc': '碳酸锂', 'ps': '多晶硅',
        # 金融期货
        'if': '沪深300指数', 'ih': '上证50指数', 'ic': '中证500指数', 'im': '中证1000指数',
        'ts': '2年期国债', 'tf': '5年期国债', 't': '10年期国债', 'tl': '30年期国债',
    }
    
    # 品种代码到交易所的映射
    SYMBOL_TO_EXCHANGE = {
        # 上海期货交易所
        'pb': 'SHFE', 'rb': 'SHFE', 'cu': 'SHFE', 'al': 'SHFE', 'zn': 'SHFE', 
        'ni': 'SHFE', 'sn': 'SHFE', 'au': 'SHFE', 'ag': 'SHFE', 'hc': 'SHFE',
        'fu': 'SHFE', 'bu': 'SHFE', 'ru': 'SHFE', 'br': 'SHFE', 'sp': 'SHFE',
        'wr': 'SHFE', 'ss': 'SHFE', 'ao': 'SHFE',
        # 上海国际能源
        'sc': 'INE', 'nr': 'INE', 'lu': 'INE', 'bc': 'INE',
        # 大连商品
        'm': 'DCE', 'y': 'DCE', 'a': 'DCE', 'b': 'DCE', 'p': 'DCE', 'c': 'DCE',
        'cs': 'DCE', 'l': 'DCE', 'v': 'DCE', 'pp': 'DCE', 'j': 'DCE',
        'jm': 'DCE', 'i': 'DCE', 'fb': 'DCE', 'bb': 'DCE', 'eg': 'DCE',
        'rr': 'DCE', 'eb': 'DCE', 'pg': 'DCE', 'lh': 'DCE', 'lg': 'DCE',
        # 郑州商品
        'sr': 'CZCE', 'cf': 'CZCE', 'ta': 'CZCE', 'oi': 'CZCE', 'rm': 'CZCE',
        'ma': 'CZCE', 'fg': 'CZCE', 'zc': 'CZCE', 'sf': 'CZCE', 'sm': 'CZCE',
        'cy': 'CZCE', 'ap': 'CZCE', 'cj': 'CZCE', 'ur': 'CZCE', 'sa': 'CZCE',
        'pf': 'CZCE', 'pk': 'CZCE', 'px': 'CZCE', 'sh': 'CZCE', 'pr': 'CZCE',
        # 广州期货
        'si': 'GFEX', 'lc': 'GFEX', 'ps': 'GFEX',
        # 金融期货
        'if': 'CFFEX', 'ih': 'CFFEX', 'ic': 'CFFEX', 'im': 'CFFEX',
        'ts': 'CFFEX', 'tf': 'CFFEX', 't': 'CFFEX', 'tl': 'CFFEX',
    }
    
    def __init__(self, symbol: str):
        """
        初始化期货分析器
        
        参数:
            symbol (str): 期货品种代码, 如 "pb", "RB" 等 (不区分大小写)
        """
        self.symbol = symbol.lower()
        self.chinese_name = self.SYMBOL_TO_CHINESE.get(self.symbol, self.symbol)
        self.exchange = self.SYMBOL_TO_EXCHANGE.get(self.symbol, 'UNKNOWN')
        self._data_cache = None  # 缓存数据
        
    def _get_sina_symbol(self) -> str:
        """获取新浪接口的合约代码 (如 PB0)"""
        return f"{self.symbol.upper()}0"
    
    def _get_em_symbol(self) -> str:
        """获取东方财富接口的合约代码 (如 铅主连)"""
        return f"{self.chinese_name}主连"
    
    def get_recent_30_days(self, use_cache: bool = True) -> pd.DataFrame:
        """
        获取最近30天的期货数据
        
        参数:
            use_cache (bool): 是否使用缓存数据, 默认True
            
        返回:
            pd.DataFrame: 包含最近30天的期货数据
                - date: 日期
                - open: 开盘价
                - high: 最高价
                - low: 最低价
                - close: 收盘价
                - volume: 成交量
                - hold: 持仓量
                - settle: 结算价 (新浪数据)
                - change: 涨跌额 (东财数据)
                - change_pct: 涨跌幅% (东财数据)
                - amount: 成交额 (东财数据)
        """
        if use_cache and self._data_cache is not None:
            data = self._data_cache
        else:
            # 使用新浪接口获取数据
            try:
                sina_symbol = self._get_sina_symbol()
                data = ak.futures_zh_daily_sina(symbol=sina_symbol)
                data['date'] = pd.to_datetime(data['date'])
                self._data_cache = data
            except Exception as e:
                print(f"新浪接口获取失败, 尝试东财接口: {e}")
                try:
                    em_symbol = self._get_em_symbol()
                    data = ak.futures_hist_em(symbol=em_symbol, period="daily")
                    data.rename(columns={
                        '时间': 'date', '开盘': 'open', '最高': 'high', 
                        '最低': 'low', '收盘': 'close', '成交量': 'volume',
                        '持仓量': 'hold', '涨跌': 'change', '涨跌幅': 'change_pct',
                        '成交额': 'amount'
                    }, inplace=True)
                    data['date'] = pd.to_datetime(data['date'])
                    self._data_cache = data
                except Exception as e2:
                    raise ValueError(f"无法获取品种 {self.symbol} 的数据: {e2}")
        
        # 获取最近30天的数据
        end_date = datetime.now()
        start_date = end_date - timedelta(days=45)  # 多取一些天数确保包含交易日
        
        recent_data = data[data['date'] >= start_date].copy()
        recent_data = recent_data.tail(30)  # 取最近30条记录
        recent_data = recent_data.reset_index(drop=True)
        
        return recent_data
    
    def get_key_indicators(self) -> Dict[str, Union[float, int, str]]:
        """
        获取期货品种的重要技术指标
        
        返回:
            Dict: 包含以下重要指标:
                - 基础价格指标: 最新价、开盘价、最高价、最低价、结算价
                - 涨跌指标: 涨跌额、涨跌幅
                - 成交量指标: 成交量、持仓量、成交额
                - 技术指标: MA5, MA10, MA20, MA30, 波动率, RSI
                - 统计指标: 30日均价、30日最高、30日最低、振幅
        """
        data = self.get_recent_30_days()
        
        if len(data) == 0:
            return {"error": "无数据"}
        
        # 获取最新一天的数据
        latest = data.iloc[-1]
        prev = data.iloc[-2] if len(data) > 1 else latest
        
        # 计算技术指标
        indicators = {
            # 基础信息
            '品种代码': self.symbol.upper(),
            '品种名称': self.chinese_name,
            '交易所': self.exchange,
            '数据日期': latest['date'].strftime('%Y-%m-%d') if isinstance(latest['date'], pd.Timestamp) else str(latest['date']),
            
            # 最新价格数据
            '最新价': round(latest['close'], 2),
            '开盘价': round(latest['open'], 2),
            '最高价': round(latest['high'], 2),
            '最低价': round(latest['low'], 2),
            
            # 涨跌数据
            '涨跌额': round(latest['close'] - prev['close'], 2) if len(data) > 1 else 0,
            '涨跌幅%': round((latest['close'] - prev['close']) / prev['close'] * 100, 2) if len(data) > 1 else 0,
            
            # 成交量数据
            '成交量': int(latest['volume']),
            '持仓量': int(latest['hold']) if 'hold' in latest else None,
            '成交额': int(latest['amount']) if 'amount' in latest else None,
            
            # 结算价 (新浪数据)
            '结算价': round(latest['settle'], 2) if 'settle' in latest and pd.notna(latest['settle']) else None,
        }
        
        # 计算移动平均线
        data['MA5'] = data['close'].rolling(window=5).mean()
        data['MA10'] = data['close'].rolling(window=10).mean()
        data['MA20'] = data['close'].rolling(window=20).mean()
        data['MA30'] = data['close'].rolling(window=30).mean()
        
        # 计算RSI (相对强弱指标)
        delta = data['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        data['RSI'] = 100 - (100 / (1 + rs))
        
        # 计算波动率 (标准差)
        data['returns'] = data['close'].pct_change()
        volatility = data['returns'].std() * np.sqrt(252) * 100  # 年化波动率
        
        # 添加技术指标
        indicators.update({
            'MA5': round(data['MA5'].iloc[-1], 2) if pd.notna(data['MA5'].iloc[-1]) else None,
            'MA10': round(data['MA10'].iloc[-1], 2) if pd.notna(data['MA10'].iloc[-1]) else None,
            'MA20': round(data['MA20'].iloc[-1], 2) if pd.notna(data['MA20'].iloc[-1]) else None,
            'MA30': round(data['MA30'].iloc[-1], 2) if pd.notna(data['MA30'].iloc[-1]) else None,
            'RSI(14)': round(data['RSI'].iloc[-1], 2) if pd.notna(data['RSI'].iloc[-1]) else None,
            '年化波动率%': round(volatility, 2) if pd.notna(volatility) else None,
        })
        
        # 统计指标 (基于30天数据)
        indicators.update({
            '30日均价': round(data['close'].mean(), 2),
            '30日最高': round(data['high'].max(), 2),
            '30日最低': round(data['low'].min(), 2),
            '30日振幅%': round((data['high'].max() - data['low'].min()) / data['low'].min() * 100, 2),
            '30日总成交量': int(data['volume'].sum()),
            '30日平均成交量': int(data['volume'].mean()),
        })
        
        # 计算MACD
        exp1 = data['close'].ewm(span=12, adjust=False).mean()
        exp2 = data['close'].ewm(span=26, adjust=False).mean()
        data['MACD'] = exp1 - exp2
        data['Signal'] = data['MACD'].ewm(span=9, adjust=False).mean()
        data['Histogram'] = data['MACD'] - data['Signal']
        
        indicators.update({
            'MACD': round(data['MACD'].iloc[-1], 4) if pd.notna(data['MACD'].iloc[-1]) else None,
            'MACD_Signal': round(data['Signal'].iloc[-1], 4) if pd.notna(data['Signal'].iloc[-1]) else None,
            'MACD_Histogram': round(data['Histogram'].iloc[-1], 4) if pd.notna(data['Histogram'].iloc[-1]) else None,
        })
        
        return indicators
    
    def get_all_data(self, days: int = 365) -> pd.DataFrame:
        """
        获取指定天数的历史数据
        
        参数:
            days (int): 获取数据的天数, 默认365天
            
        返回:
            pd.DataFrame: 历史数据
        """
        try:
            sina_symbol = self._get_sina_symbol()
            data = ak.futures_zh_daily_sina(symbol=sina_symbol)
            data['date'] = pd.to_datetime(data['date'])
            
            # 过滤指定天数
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days + 30)
            data = data[data['date'] >= start_date].copy()
            data = data.tail(days)
            data = data.reset_index(drop=True)
            
            return data
        except Exception as e:
            raise ValueError(f"无法获取数据: {e}")
    
    def get_contract_info(self) -> Dict[str, str]:
        """
        获取品种基本信息
        
        返回:
            Dict: 品种基本信息
        """
        return {
            '品种代码': self.symbol.upper(),
            '品种名称': self.chinese_name,
            '交易所': self.exchange,
            '新浪合约代码': self._get_sina_symbol(),
            '东财合约代码': self._get_em_symbol(),
        }
    
    def to_json(self) -> str:
        """将关键指标转换为JSON字符串"""
        indicators = self.get_key_indicators()
        # 处理None值和特殊类型
        cleaned = {}
        for k, v in indicators.items():
            if v is None:
                cleaned[k] = None
            elif isinstance(v, (np.integer, np.floating)):
                cleaned[k] = float(v)
            else:
                cleaned[k] = v
        return json.dumps(cleaned, ensure_ascii=False, indent=2)
    
    def display_summary(self):
        """打印品种数据摘要"""
        info = self.get_contract_info()
        indicators = self.get_key_indicators()
        recent_data = self.get_recent_30_days()
        
        print("=" * 60)
        print(f"期货品种分析报告: {info['品种名称']} ({info['品种代码']})")
        print("=" * 60)
        print(f"\n【基本信息】")
        for key, value in info.items():
            print(f"  {key}: {value}")
        
        print(f"\n【最新行情】")
        key_price = ['最新价', '开盘价', '最高价', '最低价', '涨跌额', '涨跌幅%', '成交量', '持仓量']
        for key in key_price:
            if key in indicators and indicators[key] is not None:
                print(f"  {key}: {indicators[key]}")
        
        print(f"\n【技术指标】")
        key_tech = ['MA5', 'MA10', 'MA20', 'RSI(14)', 'MACD', '年化波动率%']
        for key in key_tech:
            if key in indicators and indicators[key] is not None:
                print(f"  {key}: {indicators[key]}")
        
        print(f"\n【30日统计】")
        key_stats = ['30日均价', '30日最高', '30日最低', '30日振幅%', '30日总成交量']
        for key in key_stats:
            if key in indicators and indicators[key] is not None:
                print(f"  {key}: {indicators[key]}")
        
        print(f"\n【最近5日数据】")
        display_cols = ['date', 'open', 'high', 'low', 'close', 'volume']
        if 'hold' in recent_data.columns:
            display_cols.append('hold')
        print(recent_data.tail(5)[display_cols].to_string(index=False))
        print("=" * 60)


# 便捷函数，供LangChain工具调用
def analyze_futures_data(symbol: str) -> str:
    """
    分析期货品种的基本面数据
    
    参数:
        symbol (str): 期货品种代码，如 "ss" (不锈钢), "cu" (铜), "rb" (螺纹钢) 等
    
    返回:
        str: JSON格式的基本面分析报告
    """
    try:
        analyzer = FuturesAnalyzer(symbol)
        return analyzer.to_json()
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)


if __name__ == "__main__":
    # 测试代码
    analyzer = FuturesAnalyzer("ss")  # 不锈钢
    analyzer.display_summary()
