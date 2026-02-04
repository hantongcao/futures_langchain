"""
网络搜索工具 - 基于智谱AI
"""
import os
from typing import Optional
from langchain_core.tools import tool

try:
    from zhipuai import ZhipuAI
    HAS_ZHIPUAI = True
except ImportError:
    HAS_ZHIPUAI = False


@tool
def web_search(query: str, count: int = 10) -> str:
    """
    互联网搜索，用于获取期货相关新闻资讯
    
    参数:
        query (str): 搜索关键词，如"不锈钢期货 新闻"
        count (int): 返回结果数量，默认10条
    
    返回:
        str: 搜索结果，包含标题、链接和摘要
    """
    # 检查是否安装了zhipuai
    if not HAS_ZHIPUAI:
        return f"""【模拟搜索结果】关键词: {query}

由于未安装zhipuai包，返回模拟数据。实际使用时请安装: pip install zhipuai

1. 不锈钢期货价格企稳回升
   近期不锈钢期货价格出现企稳迹象，市场情绪有所改善。钢厂减产保价措施见效，库存持续下降。

2. 下游需求逐步恢复
   随着制造业复苏，不锈钢下游需求呈现回暖态势，订单量有所增加。

3. 原材料成本支撑
   镍价走势坚挺，为不锈钢价格提供成本支撑，限制了价格下跌空间。
"""
    
    try:
        api_key = os.getenv("ZHIPU_API_KEY")
        if not api_key:
            return "错误：未设置ZHIPU_API_KEY环境变量"
        
        client = ZhipuAI(api_key=api_key)
        
        # 使用智谱AI的web_search工具
        response = client.chat.completions.create(
            model="glm-4-flash",
            messages=[
                {"role": "user", "content": f"请搜索以下内容的最新资讯：{query}"}
            ],
            tools=[
                {
                    "type": "web_search",
                    "web_search": {
                        "enable": True,
                        "search_query": query
                    }
                }
            ]
        )
        
        # 提取搜索结果
        results = []
        for choice in response.choices:
            if hasattr(choice.message, 'content') and choice.message.content:
                results.append(choice.message.content)
        
        if results:
            return "\n\n".join(results)
        else:
            return "未找到相关搜索结果"
            
    except Exception as e:
        return f"搜索出错：{str(e)}"


if __name__ == "__main__":
    # 测试
    result = web_search.invoke({"query": "不锈钢期货 最新行情", "count": 5})
    print(result)
