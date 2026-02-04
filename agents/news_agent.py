"""
新闻搜集Agent - 负责搜集和整理期货相关新闻
"""
from langgraph.prebuilt import create_react_agent
from langchain_deepseek import ChatDeepSeek
import os


def create_news_agent(model: ChatDeepSeek = None):
    """
    创建新闻搜集Agent
    
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
    
    from tools import web_search, save_news_to_markdown
    
    news_system_prompt = """你是一个专业的期货新闻分析师，负责搜集和整理期货相关新闻资讯。

## 任务流程
1. 使用 web_search 工具搜索相关新闻（搜索关键词应包含"期货"和具体品种名称）
2. 整理新闻内容，分类为正向新闻（利好）和负向新闻（利空）
3. 每个新闻总结为一段，包含：标题、来源、核心内容、对期货价格的影响分析
4. 使用 save_news_to_markdown 工具保存报告

## 报告格式要求
```markdown
# 期货新闻分析报告

## 一、新闻搜集概况
- 搜集时间: [时间]
- 关键词: [使用的关键词]
- 新闻来源: [主要来源]

## 二、正向新闻（利好因素）

### 1. [新闻标题]
**来源**: [来源]  
**核心内容**: [简要概括]  
**影响分析**: [对期货价格的影响，为什么利好]

### 2. [新闻标题]
...

## 三、负向新闻（利空因素）

### 1. [新闻标题]
**来源**: [来源]  
**核心内容**: [简要概括]  
**影响分析**: [对期货价格的影响，为什么利空]

### 2. [新闻标题]
...

## 四、新闻总结
[综合分析所有新闻，提炼关键信息，3000字以内]
```

## 注意事项
- 确保新闻来源可靠（优先选择官方媒体、交易所公告、权威财经媒体）
- 每条新闻都要有明确的影响分析（利好/利空）
- 总字数控制在10000字以内
- 搜索时多使用不同关键词组合，确保信息全面

现在请开始执行新闻搜集任务。"""

    agent = create_react_agent(
        model=model,
        tools=[web_search, save_news_to_markdown],
        prompt=news_system_prompt
    )
    
    return agent


if __name__ == "__main__":
    # 测试
    from dotenv import load_dotenv
    load_dotenv()
    
    agent = create_news_agent()
    result = agent.invoke({
        "messages": [("user", "分析不锈钢期货市场的新闻资讯")]
    })
    print(result)
