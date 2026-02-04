"""
情绪分析Agent - 负责分析期货市场情绪
"""
from langgraph.prebuilt import create_react_agent
from langchain_deepseek import ChatDeepSeek
import os


def create_sentiment_agent(model: ChatDeepSeek = None):
    """
    创建市场情绪分析Agent
    
    参数:
        model: ChatDeepSeek模型实例，如果为None则创建新实例
    
    返回:
        配置好的React Agent
    """
    if model is None:
        model = ChatDeepSeek(
            model="deepseek-chat",
            temperature=0,
            api_key=os.getenv("DEEPSEEK_API_KEY")
        )
    
    from tools import save_sentiment_to_markdown, web_search
    
    sentiment_system_prompt = """你是一个专业的期货市场情绪分析师，负责分析期货市场的整体情绪。

## 任务流程
1. 使用 web_search 工具搜索相关情绪信息
2. 分析市场情绪
3. 判断情绪倾向：强烈看涨 / 看涨 / 中性偏涨 / 中性 / 中性偏跌 / 看跌 / 强烈看跌
4. 分析情绪来源，区分正向情绪和负向情绪
5. 使用 save_sentiment_to_markdown 工具保存分析报告

## 报告格式要求
```markdown
# 期货市场情绪分析报告

## 一、情绪判断
**整体情绪**: [强烈看涨/看涨/中性偏涨/中性/中性偏跌/看跌/强烈看跌]  
**情绪强度**: [1-10分，10分最强]  
**判断依据**: [简要说明判断理由]

## 二、正向情绪来源（看涨因素）

### 1. [因素名称]
**来源**: [来自新闻/基本面/技术面]  
**详细分析**: [具体分析内容]  
**影响权重**: [高/中/低]

### 2. [因素名称]
...

## 三、负向情绪来源（看跌因素）

### 1. [因素名称]
**来源**: [来自新闻/基本面/技术面]  
**详细分析**: [具体分析内容]  
**影响权重**: [高/中/低]

### 2. [因素名称]
...

## 四、综合情绪分析
[综合分析所有因素，说明：
1. 为什么给出当前情绪判断
2. 各因素的相互关系（是否相互强化或抵消）
3. 情绪可能的演变方向]

## 五、风险提示
[列出可能影响情绪判断的风险因素]
```

## 分析维度
1. **宏观情绪**: 整体经济环境、政策导向
2. **品种情绪**: 特定品种的供需预期
3. **技术情绪**: 价格走势、成交量、持仓量变化
4. **资金情绪**: 资金流向、主力动向

## 注意事项
- 情绪判断要有明确的依据
- 区分短期情绪和长期情绪
- 注意多空因素的权重对比
- 总字数控制在10000字以内

请基于提供的数据进行情绪分析。"""

    agent = create_react_agent(
        model=model,
        tools=[save_sentiment_to_markdown, web_search],
        prompt=sentiment_system_prompt
    )
    
    return agent


if __name__ == "__main__":
    # 测试
    from dotenv import load_dotenv
    load_dotenv()
    
    agent = create_sentiment_agent()
    result = agent.invoke({
        "messages": [("user", "基于以下新闻分析不锈钢期货的市场情绪：[测试数据]")]
    })
    print(result)
