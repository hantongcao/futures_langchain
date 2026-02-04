"""
Agents 测试脚本
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from dotenv import load_dotenv
load_dotenv()

from langchain_deepseek import ChatDeepSeek
from agents import create_news_agent, create_sentiment_agent, create_fundamental_agent, create_summary_agent


def get_model():
    """获取模型实例"""
    return ChatDeepSeek(
        model="deepseek-chat",
        temperature=0,
        api_key=os.getenv("DEEPSEEK_API_KEY")
    )


def test_news_agent():
    """测试新闻搜集Agent"""
    print("=" * 60)
    print("测试新闻搜集Agent")
    print("=" * 60)
    
    try:
        model = get_model()
        agent = create_news_agent(model)
        
        result = agent.invoke({
            "messages": [("user", "搜索不锈钢期货的最新新闻")]
        })
        
        print("Agent响应:")
        for msg in result["messages"][-3:]:  # 只显示最后3条
            if hasattr(msg, 'content') and msg.content:
                print(f"  {msg.content[:200]}...")
        
        print("\n测试通过!")
    except Exception as e:
        print(f"测试失败: {e}")
        import traceback
        traceback.print_exc()
    
    print("=" * 60)


def test_sentiment_agent():
    """测试情绪分析Agent"""
    print("\n" + "=" * 60)
    print("测试情绪分析Agent")
    print("=" * 60)
    
    try:
        model = get_model()
        agent = create_sentiment_agent(model)
        
        result = agent.invoke({
            "messages": [("user", "分析不锈钢期货的市场情绪")]
        })
        
        print("Agent响应:")
        for msg in result["messages"][-3:]:
            if hasattr(msg, 'content') and msg.content:
                print(f"  {msg.content[:200]}...")
        
        print("\n测试通过!")
    except Exception as e:
        print(f"测试失败: {e}")
        import traceback
        traceback.print_exc()
    
    print("=" * 60)


def test_fundamental_agent():
    """测试基本面分析Agent"""
    print("\n" + "=" * 60)
    print("测试基本面分析Agent")
    print("=" * 60)
    
    try:
        model = get_model()
        agent = create_fundamental_agent(model)
        
        result = agent.invoke({
            "messages": [("user", "分析不锈钢(ss)期货的技术面数据")]
        })
        
        print("Agent响应:")
        for msg in result["messages"][-3:]:
            if hasattr(msg, 'content') and msg.content:
                print(f"  {msg.content[:200]}...")
        
        print("\n测试通过!")
    except Exception as e:
        print(f"测试失败: {e}")
        import traceback
        traceback.print_exc()
    
    print("=" * 60)


def test_summary_agent():
    """测试汇总报告Agent"""
    print("\n" + "=" * 60)
    print("测试汇总报告Agent")
    print("=" * 60)
    
    try:
        model = get_model()
        agent = create_summary_agent(model)
        
        # 模拟输入
        test_input = """
请基于以下三个分析报告生成综合投资报告：

【新闻分析报告】
不锈钢期货近期新闻偏正面，主要利好包括：1）钢厂减产保价；2）下游需求回暖；3）库存下降。

【情绪分析报告】
市场情绪中性偏多，投资者信心逐步恢复，但仍有谨慎情绪。

【技术分析报告】
不锈钢期货技术面呈现多头排列，RSI在55中性区域，MACD金叉，价格站上MA20。
"""
        
        result = agent.invoke({
            "messages": [("user", test_input)]
        })
        
        print("Agent响应:")
        for msg in result["messages"][-3:]:
            if hasattr(msg, 'content') and msg.content:
                print(f"  {msg.content[:200]}...")
        
        print("\n测试通过!")
    except Exception as e:
        print(f"测试失败: {e}")
        import traceback
        traceback.print_exc()
    
    print("=" * 60)


if __name__ == "__main__":
    print("开始测试 Agents...")
    print("注意: 测试需要配置 DEEPSEEK_API_KEY 环境变量\n")
    
    # 测试各个Agent
    test_news_agent()
    test_sentiment_agent()
    test_fundamental_agent()
    test_summary_agent()
    
    print("\n所有测试完成!")
