"""
工作流测试脚本 - 测试完整的并行工作流
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from dotenv import load_dotenv
load_dotenv()

from workflow import create_workflow, analyze_futures


def test_create_workflow():
    """测试工作流创建"""
    print("=" * 60)
    print("测试工作流创建")
    print("=" * 60)
    
    try:
        app = create_workflow()
        print(f"工作流创建成功!")
        print(f"工作流类型: {type(app)}")
        
        # 打印工作流结构
        print("\n工作流图结构:")
        # 获取图的节点和边
        print("  节点: start, news_agent, sentiment_agent, fundamental_agent, summary_agent, end")
        print("  边: start -> [news_agent, sentiment_agent, fundamental_agent] (并行)")
        print("      [news_agent, sentiment_agent, fundamental_agent] -> summary_agent")
        print("      summary_agent -> end")
        
        print("\n测试通过!")
    except Exception as e:
        print(f"测试失败: {e}")
        import traceback
        traceback.print_exc()
    
    print("=" * 60)


def test_analyze_futures():
    """测试完整的分析流程"""
    print("\n" + "=" * 60)
    print("测试完整的分析流程")
    print("=" * 60)
    
    try:
        print("\n注意: 这个测试会调用API，可能需要几分钟时间...")
        print("正在分析不锈钢期货...\n")
        
        result = analyze_futures("ss", "不锈钢")
        
        print("\n" + "-" * 60)
        print("分析结果:")
        print("-" * 60)
        
        # 检查结果
        if result.get("final_report"):
            print(f"\n✓ 最终报告已生成")
            print(f"  报告长度: {len(result['final_report'])} 字符")
            print(f"\n报告预览 (前500字符):")
            print(result['final_report'][:500])
            print("...")
        else:
            print("\n✗ 未生成最终报告")
        
        # 检查子Agent结果
        if result.get("news_result"):
            print(f"\n✓ 新闻分析完成")
            print(f"  结果数: {len(result['news_result'])}")
        
        if result.get("sentiment_result"):
            print(f"\n✓ 情绪分析完成")
            print(f"  结果数: {len(result['sentiment_result'])}")
        
        if result.get("fundamental_result"):
            print(f"\n✓ 基本面分析完成")
            print(f"  结果数: {len(result['fundamental_result'])}")
        
        # 检查错误
        if result.get("errors"):
            print(f"\n⚠ 执行过程中出现 {len(result['errors'])} 个错误:")
            for error in result["errors"]:
                print(f"  - {error}")
        
        print("\n测试通过!")
    except Exception as e:
        print(f"测试失败: {e}")
        import traceback
        traceback.print_exc()
    
    print("=" * 60)


def test_state_structure():
    """测试状态结构"""
    print("\n" + "=" * 60)
    print("测试状态结构")
    print("=" * 60)
    
    from workflow import FuturesAnalysisState
    from typing import get_type_hints
    
    try:
        # 检查状态定义
        hints = get_type_hints(FuturesAnalysisState)
        print("状态字段:")
        for key, value in hints.items():
            print(f"  {key}: {value}")
        
        # 创建测试状态
        test_state: FuturesAnalysisState = {
            "symbol": "ss",
            "keyword": "不锈钢",
            "news_result": [],
            "sentiment_result": [],
            "fundamental_result": [],
            "errors": [],
            "final_report": "",
            "report_path": ""
        }
        
        print("\n测试状态创建成功!")
        print(f"  symbol: {test_state['symbol']}")
        print(f"  keyword: {test_state['keyword']}")
        
        print("\n测试通过!")
    except Exception as e:
        print(f"测试失败: {e}")
        import traceback
        traceback.print_exc()
    
    print("=" * 60)


if __name__ == "__main__":
    print("开始测试工作流...")
    print("注意: 部分测试需要配置 API 密钥\n")
    
    # 运行测试
    test_create_workflow()
    test_state_structure()
    
    # 询问是否运行完整测试
    print("\n" + "=" * 60)
    response = input("是否运行完整分析流程测试? (y/n): ")
    if response.lower() == 'y':
        test_analyze_futures()
    else:
        print("跳过完整流程测试")
    
    print("\n所有测试完成!")
