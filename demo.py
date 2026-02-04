#!/usr/bin/env python3
"""
期货多智能体分析系统 - 演示脚本

这个脚本演示了工作流的结构和各个Agent的功能，
不需要实际的API密钥即可运行（使用模拟数据）。
"""
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(__file__))

from tools.futures_analyzer import FuturesAnalyzer


def demo_futures_analyzer():
    """演示期货数据分析"""
    print("=" * 70)
    print("演示 1: 期货数据分析 (FuturesAnalyzer)")
    print("=" * 70)
    
    # 创建分析器
    analyzer = FuturesAnalyzer("ss")  # 不锈钢
    
    print(f"\n品种信息:")
    info = analyzer.get_contract_info()
    for key, value in info.items():
        print(f"  {key}: {value}")
    
    print(f"\n关键指标:")
    indicators = analyzer.get_key_indicators()
    key_fields = ['最新价', '涨跌幅%', '成交量', '持仓量', 'RSI(14)', 'MA5', 'MA20']
    for field in key_fields:
        if field in indicators:
            print(f"  {field}: {indicators[field]}")
    
    print(f"\n最近5日数据:")
    data = analyzer.get_recent_30_days()
    print(data.tail(5)[['date', 'open', 'high', 'low', 'close', 'volume']].to_string(index=False))
    
    print("\n" + "=" * 70)


def demo_workflow_structure():
    """演示工作流结构"""
    print("\n" + "=" * 70)
    print("演示 2: 工作流结构")
    print("=" * 70)
    
    print("""
期货多智能体分析系统工作流（两阶段并行）:

    ┌─────────────────────────────────────────────────────────────┐
    │                         开始分析                             │
    └──────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
    ╔═════════════════════════════════════════════════════════════╗
    ║                    第一阶段：基础分析（并行）                  ║
    ║  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      ║
    ║  │  新闻搜集Agent │  │  情绪分析Agent │  │ 基本面分析Agent│      ║
    ║  │              │  │              │  │              │      ║
    ║  │ 1. 搜索新闻   │  │ 1. 分析情绪   │  │ 1. 获取数据   │      ║
    ║  │ 2. 分类整理   │  │ 2. 判断多空   │  │ 2. 计算指标   │      ║
    ║  │ 3. 保存报告   │  │ 3. 保存报告   │  │ 3. 保存报告   │      ║
    ║  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘      ║
    ╚═════════╧═════════════════╧═════════════════╧══════════════╝
                           │
                           ▼ （全部完成后触发）
    ╔═════════════════════════════════════════════════════════════╗
    ║                  第二阶段：观点分析（并行）                    ║
    ║                                                             ║
    ║  ┌─────────────────────┐    ┌─────────────────────┐        ║
    ║  │   看涨分析师Agent    │    │   看跌分析师Agent    │        ║
    ║  │                     │    │                     │        ║
    ║  │ • 挖掘多头逻辑       │    │ • 挖掘空头逻辑       │        ║
    ║  │ • 量化上行空间       │    │ • 量化下行风险       │        ║
    ║  │ • 给出做多策略       │    │ • 给出做空策略       │        ║
    ║  │ • 保存看涨报告       │    │ • 保存看跌报告       │        ║
    ║  └──────────┬──────────┘    └──────────┬──────────┘        ║
    ╚═════════════╧══════════════════════════╧══════════════════╝
                           │
                           ▼ （全部完成后触发）
    ┌─────────────────────────────────────────────────────────────┐
    │                      汇总报告Agent                           │
    │                                                              │
    │  1. 整合五方分析结果（基础分析×3 + 观点分析×2）               │
    │  2. 对比多头/空头观点，形成平衡判断                           │
    │  3. 生成综合投资报告                                          │
    │  4. 保存最终报告                                              │
    │                                                              │
    └──────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
    ┌─────────────────────────────────────────────────────────────┐
    │                         分析完成                             │
    │           7份报告保存至: reports/ 目录                        │
    │      (news + sentiment + fundamental + bullish + bearish + summary)
    └─────────────────────────────────────────────────────────────┘
    """)
    
    print("=" * 70)


def demo_agents():
    """演示各个Agent的功能"""
    print("\n" + "=" * 70)
    print("演示 3: Agent 功能介绍")
    print("=" * 70)
    
    agents = {
        "【第一阶段】新闻搜集Agent": {
            "功能": "搜索并整理期货相关新闻",
            "输入": "期货品种关键词",
            "输出": "分类整理的新闻报告（利好/利空）",
            "工具": ["web_search", "save_news_to_markdown"]
        },
        "【第一阶段】情绪分析Agent": {
            "功能": "分析期货市场情绪",
            "输入": "新闻内容和市场信息",
            "输出": "情绪分析报告（看涨/看跌/中性）",
            "工具": ["save_sentiment_to_markdown"]
        },
        "【第一阶段】基本面分析Agent": {
            "功能": "分析期货品种的技术面数据",
            "输入": "期货品种代码",
            "输出": "技术分析报告（指标/趋势/建议）",
            "工具": ["analyze_futures_data", "save_fundamental_to_markdown"]
        },
        "【第二阶段】看涨分析师Agent": {
            "功能": "基于第一阶段结果，深度挖掘多头逻辑",
            "输入": "三个基础分析Agent的结果",
            "输出": "看涨分析报告（做多策略/目标价位）",
            "工具": ["web_search", "save_bullish_to_markdown"]
        },
        "【第二阶段】看跌分析师Agent": {
            "功能": "基于第一阶段结果，深度挖掘空头逻辑",
            "输入": "三个基础分析Agent的结果",
            "输出": "看跌分析报告（做空策略/风险警示）",
            "工具": ["web_search", "save_bearish_to_markdown"]
        },
        "【第三阶段】汇总报告Agent": {
            "功能": "整合五方分析，生成平衡的投资建议",
            "输入": "三个基础分析 + 两个观点分析的结果",
            "输出": "综合投资报告（评级/建议/风险）",
            "工具": ["save_summary_to_markdown"]
        }
    }
    
    for name, info in agents.items():
        print(f"\n【{name}】")
        for key, value in info.items():
            if isinstance(value, list):
                print(f"  {key}: {', '.join(value)}")
            else:
                print(f"  {key}: {value}")
    
    print("\n" + "=" * 70)


def demo_usage():
    """演示使用方法"""
    print("\n" + "=" * 70)
    print("演示 4: 使用方法")
    print("=" * 70)
    
    print("""
1. 命令行使用:
   
   # 分析不锈钢期货
   python main.py --symbol ss
   
   # 分析铜期货
   python main.py --symbol cu --keyword 铜
   
   # 列出所有支持的品种
   python main.py --list-symbols

2. Python API 使用:
   
   from workflow import analyze_futures
   
   # 分析不锈钢期货
   result = analyze_futures(symbol="ss", keyword="不锈钢")
   
   # 获取最终报告
   final_report = result["final_report"]
   print(final_report)

3. 支持的期货品种:
   
   代码    品种        交易所
   ─────────────────────────
   ss      不锈钢      SHFE
   cu      铜          SHFE
   rb      螺纹钢      SHFE
   pb      铅          SHFE
   al      铝          SHFE
   ni      镍          SHFE
   au      黄金        SHFE
   ag      白银        SHFE
   sc      原油        INE
   m       豆粕        DCE
   ...     ...         ...
    """)
    
    print("=" * 70)


def main():
    """主函数"""
    print("\n" + "=" * 70)
    print(" " * 20 + "期货多智能体分析系统")
    print(" " * 15 + "Futures Multi-Agent Analysis System")
    print("=" * 70)
    
    # 运行各个演示
    demo_futures_analyzer()
    demo_workflow_structure()
    demo_agents()
    demo_usage()
    
    print("\n" + "=" * 70)
    print("演示完成!")
    print("=" * 70)
    print("\n提示: 要运行实际分析，请配置 API 密钥后执行:")
    print("  export DEEPSEEK_API_KEY='your_key'")
    print("  export ZHIPU_API_KEY='your_key'")
    print("  python main.py --symbol ss")
    print()


if __name__ == "__main__":
    main()
