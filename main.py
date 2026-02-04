#!/usr/bin/env python3
"""
期货多智能体分析系统 - 主入口

使用方法:
    python main.py --symbol ss --keyword 不锈钢
    python main.py --symbol cu --keyword 铜
    python main.py --symbol rb --keyword 螺纹钢

支持品种:
    - ss: 不锈钢
    - cu: 铜
    - rb: 螺纹钢
    - pb: 铅
    - al: 铝
    - zn: 锌
    - ni: 镍
    - au: 黄金
    - ag: 白银
    - 等等...
"""
import argparse
import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from workflow import analyze_futures


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="期货多智能体分析系统",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python main.py --symbol ss                    # 分析不锈钢
  python main.py --symbol cu --keyword 铜        # 分析铜
  python main.py --symbol rb --keyword 螺纹钢    # 分析螺纹钢
        """
    )
    
    parser.add_argument(
        "--symbol",
        type=str,
        required=False,
        help="期货品种代码，如 ss (不锈钢), cu (铜), rb (螺纹钢)"
    )
    
    parser.add_argument(
        "--keyword",
        type=str,
        default=None,
        help="搜索关键词，如 '不锈钢'，默认为品种代码对应的中文名"
    )
    
    parser.add_argument(
        "--list-symbols",
        action="store_true",
        help="列出所有支持的品种代码"
    )
    
    args = parser.parse_args()
    
    # 列出支持的品种
    if args.list_symbols:
        # --list-symbols 不需要 symbol 参数
        from tools.futures_analyzer import FuturesAnalyzer
        print("\n支持的期货品种代码:")
        print("-" * 50)
        for code, name in sorted(FuturesAnalyzer.SYMBOL_TO_CHINESE.items()):
            exchange = FuturesAnalyzer.SYMBOL_TO_EXCHANGE.get(code, "UNKNOWN")
            print(f"  {code:6} - {name:10} ({exchange})")
        print()
        return
    
    # 检查 symbol 是否提供（除了 --list-symbols 之外都需要）
    if not args.symbol:
        parser.error("--symbol 是必需的参数（除非使用 --list-symbols）")
    
    # 执行分析
    print(f"\n{'='*60}")
    print(f"期货多智能体分析系统")
    print(f"{'='*60}")
    
    symbol = args.symbol.lower()
    keyword = args.keyword
    
    try:
        result = analyze_futures(symbol, keyword)
        
        # 打印结果摘要
        print("\n" + "="*60)
        print("分析完成!")
        print("="*60)
        
        if result.get("final_report"):
            print("\n最终报告已生成并保存到 reports/ 目录")
            print(f"报告长度: {len(result['final_report'])} 字符")
        
        if result.get("errors"):
            print(f"\n警告: 执行过程中出现 {len(result['errors'])} 个错误")
            for error in result["errors"]:
                print(f"  - {error}")
        
        return 0
        
    except Exception as e:
        print(f"\n错误: 分析过程出错 - {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
