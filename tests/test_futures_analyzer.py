"""
FuturesAnalyzer 测试脚本
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from tools.futures_analyzer import FuturesAnalyzer, analyze_futures_data


def test_futures_analyzer():
    """测试 FuturesAnalyzer 类"""
    print("=" * 60)
    print("测试 FuturesAnalyzer 类")
    print("=" * 60)
    
    # 测试不锈钢
    print("\n1. 测试不锈钢 (ss)")
    analyzer = FuturesAnalyzer("ss")
    print(f"品种代码: {analyzer.symbol}")
    print(f"中文名称: {analyzer.chinese_name}")
    print(f"交易所: {analyzer.exchange}")
    
    # 测试获取最近30天数据
    print("\n2. 获取最近30天数据")
    try:
        data = analyzer.get_recent_30_days()
        print(f"数据条数: {len(data)}")
        if len(data) > 0:
            print(f"最新日期: {data.iloc[-1]['date']}")
            print(f"最新收盘价: {data.iloc[-1]['close']}")
    except Exception as e:
        print(f"获取数据失败: {e}")
    
    # 测试获取关键指标
    print("\n3. 获取关键指标")
    try:
        indicators = analyzer.get_key_indicators()
        print(f"最新价: {indicators.get('最新价')}")
        print(f"涨跌幅: {indicators.get('涨跌幅%')}%")
        print(f"RSI: {indicators.get('RSI(14)')}")
        print(f"MA5: {indicators.get('MA5')}")
        print(f"MA20: {indicators.get('MA20')}")
    except Exception as e:
        print(f"获取指标失败: {e}")
    
    # 测试JSON输出
    print("\n4. 测试JSON输出")
    try:
        json_str = analyzer.to_json()
        print(f"JSON长度: {len(json_str)} 字符")
        print(f"JSON预览: {json_str[:200]}...")
    except Exception as e:
        print(f"JSON转换失败: {e}")
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)


def test_analyze_futures_data():
    """测试 analyze_futures_data 便捷函数"""
    print("\n" + "=" * 60)
    print("测试 analyze_futures_data 便捷函数")
    print("=" * 60)
    
    try:
        result = analyze_futures_data("ss")
        print(f"结果长度: {len(result)} 字符")
        print(f"结果预览: {result[:300]}...")
    except Exception as e:
        print(f"测试失败: {e}")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    test_futures_analyzer()
    test_analyze_futures_data()
