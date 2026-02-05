"""
期货多智能体分析工作流

工作流结构:
1. 第一阶段 - 三个基础Agent并行执行:
   - 新闻搜集Agent (news_agent)
   - 情绪分析Agent (sentiment_agent)
   - 基本面分析Agent (fundamental_agent)
   
2. 第二阶段 - 两个观点分析师并行执行:
   - 看涨分析师 (bullish_agent)
   - 看跌分析师 (bearish_agent)
   
3. 第三阶段 - 汇总Agent整合所有结果 (summary_agent)

使用LangGraph的Send机制实现并行执行
"""
from langgraph.types import Command
import os
from typing import TypedDict, Annotated, List, Dict, Any
from datetime import datetime
import operator
import logging
from dotenv import load_dotenv

from langgraph.graph import StateGraph, END
from langgraph.types import Send
from langchain_deepseek import ChatDeepSeek

from agents import (
    create_news_agent, create_sentiment_agent, create_fundamental_agent,
    create_bullish_agent, create_bearish_agent, create_summary_agent
)

# 加载环境变量
load_dotenv()

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


# ============== 状态定义 ==============
class FuturesAnalysisState(TypedDict):
    """工作流状态"""
    # 输入参数
    symbol: str  # 期货品种代码，如 "ss"
    keyword: str  # 搜索关键词，如 "不锈钢"
    
    # 第一阶段 - 基础分析Agent的输出结果
    news_result: Annotated[List[Dict], operator.add]  # 新闻分析结果
    sentiment_result: Annotated[List[Dict], operator.add]  # 情绪分析结果
    fundamental_result: Annotated[List[Dict], operator.add]  # 基本面分析结果
    
    # 第二阶段 - 观点分析师的输出结果
    bullish_result: Annotated[List[Dict], operator.add]  # 看涨分析报告
    bearish_result: Annotated[List[Dict], operator.add]  # 看跌分析报告
    
    # 中间状态
    errors: Annotated[List[str], operator.add]  # 错误信息
    first_phase_ready: bool  # 第一阶段是否完成
    second_phase_ready: bool  # 第二阶段是否完成
    
    # 最终结果
    final_report: str  # 汇总报告
    report_path: str  # 报告保存路径


# ============== 初始化模型和Agents ==============
def get_model():
    """获取LLM模型实例"""
    return ChatDeepSeek(
        model="deepseek-chat",
        temperature=0,
        api_key=os.getenv("DEEPSEEK_API_KEY")
    )


# ============== 节点函数 ==============
def start_analysis(state: FuturesAnalysisState):
    """
    开始分析 - 初始化状态
    
    这个节点是工作流的入口，负责准备初始状态
    """
    logger.info("="*80)
    logger.info("【步骤1】开始分析节点 (start_analysis)")
    logger.info("="*80)
    logger.info(f"期货品种代码: {state['symbol']}")
    logger.info(f"搜索关键词: {state['keyword']}")
    logger.info(f"当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("="*80)
    
    # 返回空更新，只是触发并行分支
    return {}


def analyze_news(state: FuturesAnalysisState):
    """
    新闻搜集Agent节点
    
    搜集并分析期货相关新闻
    """
    logger.info("="*80)
    logger.info("【步骤2.1】新闻搜集Agent节点 (analyze_news)")
    logger.info("="*80)
    logger.info(f"开始时间: {datetime.now().strftime('%H:%M:%S')}")
    
    try:
        logger.debug("正在初始化模型...")
        model = get_model()
        logger.info(f"模型初始化成功: {model.model_name}")
        
        logger.debug("正在创建新闻分析Agent...")
        agent = create_news_agent(model)
        logger.info("Agent创建成功")
        
        # 构建查询
        query = f"分析{state['keyword']}期货市场的新闻资讯"
        logger.info("【Agent输入】")
        logger.info(f"查询内容: {query}")
        logger.info("-"*80)
        
        logger.debug("正在调用Agent进行分析...")
        result = agent.invoke({
            "messages": [("user", query)]
        })
        logger.info("Agent调用完成")
        
        # 提取Agent的输出内容
        content = ""
        for msg in result["messages"]:
            if hasattr(msg, 'content') and msg.content:
                content += msg.content + "\n"
        
        logger.info("【Agent输出】")
        logger.info(f"输出长度: {len(content)} 字符")
        logger.info("输出内容预览:")
        logger.info("-"*80)
        logger.info(content[:500])
        if len(content) > 500:
            logger.info(f"... (内容已截断，完整内容共 {len(content)} 字符)")
        logger.info("-"*80)
        
        logger.info(f"完成时间: {datetime.now().strftime('%H:%M:%S')}")
        logger.info("="*80)
        
        return {
            "news_result": [{"status": "success", "content": content}]
        }
        
    except Exception as e:
        logger.error("【错误】新闻Agent执行失败")
        logger.error(f"错误信息: {e}")
        logger.info("="*80)
        return {
            "news_result": [{"status": "error", "error": str(e)}],
            "errors": [f"新闻分析出错: {e}"]
        }


def analyze_sentiment(state: FuturesAnalysisState):
    """
    情绪分析Agent节点
    
    分析市场情绪
    """
    logger.info("="*80)
    logger.info("【步骤2.2】情绪分析Agent节点 (analyze_sentiment)")
    logger.info("="*80)
    logger.info(f"开始时间: {datetime.now().strftime('%H:%M:%S')}")
    
    try:
        logger.debug("正在初始化模型...")
        model = get_model()
        logger.info(f"模型初始化成功: {model.model_name}")
        
        logger.debug("正在创建情绪分析Agent...")
        agent = create_sentiment_agent(model)
        logger.info("Agent创建成功")
        
        # 构建查询，包含品种信息
        query = f"请分析{state['keyword']}期货市场的整体情绪。考虑当前市场环境、投资者心态、资金流向等因素。"
        logger.info("【Agent输入】")
        logger.info(f"查询内容: {query}")
        logger.info("-"*80)
        
        logger.debug("正在调用Agent进行分析...")
        result = agent.invoke({
            "messages": [("user", query)]
        })
        logger.info("Agent调用完成")
        
        # 提取Agent的输出内容
        content = ""
        for msg in result["messages"]:
            if hasattr(msg, 'content') and msg.content:
                content += msg.content + "\n"
        
        logger.info("【Agent输出】")
        logger.info(f"输出长度: {len(content)} 字符")
        logger.info("输出内容预览:")
        logger.info("-"*80)
        logger.info(content[:500])
        if len(content) > 500:
            logger.info(f"... (内容已截断，完整内容共 {len(content)} 字符)")
        logger.info("-"*80)
        
        logger.info(f"完成时间: {datetime.now().strftime('%H:%M:%S')}")
        logger.info("="*80)
        
        return {
            "sentiment_result": [{"status": "success", "content": content}]
        }
        
    except Exception as e:
        logger.error("【错误】情绪Agent执行失败")
        logger.error(f"错误信息: {e}")
        logger.info("="*80)
        return {
            "sentiment_result": [{"status": "error", "error": str(e)}],
            "errors": [f"情绪分析出错: {e}"]
        }


def analyze_fundamental(state: FuturesAnalysisState):
    """
    基本面分析Agent节点
    
    分析期货品种的技术面和基本面数据
    """
    logger.info("="*80)
    logger.info("【步骤2.3】基本面分析Agent节点 (analyze_fundamental)")
    logger.info("="*80)
    logger.info(f"开始时间: {datetime.now().strftime('%H:%M:%S')}")
    
    try:
        logger.debug("正在初始化模型...")
        model = get_model()
        logger.info(f"模型初始化成功: {model.model_name}")
        
        logger.debug("正在创建基本面分析Agent...")
        agent = create_fundamental_agent(model)
        logger.info("Agent创建成功")
        
        # 构建查询
        query = f"请分析{state['keyword']}({state['symbol']})期货的技术面数据，包括价格走势、成交量、持仓量、技术指标等。"
        logger.info("【Agent输入】")
        logger.info(f"查询内容: {query}")
        logger.info("-"*80)
        
        logger.debug("正在调用Agent进行分析...")
        result = agent.invoke({
            "messages": [("user", query)]
        })
        logger.info("Agent调用完成")
        
        # 提取Agent的输出内容
        content = ""
        for msg in result["messages"]:
            if hasattr(msg, 'content') and msg.content:
                content += msg.content + "\n"
        
        logger.info("【Agent输出】")
        logger.info(f"输出长度: {len(content)} 字符")
        logger.info("输出内容预览:")
        logger.info("-"*80)
        logger.info(content[:500])
        if len(content) > 500:
            logger.info(f"... (内容已截断，完整内容共 {len(content)} 字符)")
        logger.info("-"*80)
        
        logger.info(f"完成时间: {datetime.now().strftime('%H:%M:%S')}")
        logger.info("="*80)
        
        return {
            "fundamental_result": [{"status": "success", "content": content}]
        }
        
    except Exception as e:
        logger.error("【错误】基本面Agent执行失败")
        logger.error(f"错误信息: {e}")
        logger.info("="*80)
        return {
            "fundamental_result": [{"status": "error", "error": str(e)}],
            "errors": [f"基本面分析出错: {e}"]
        }


def analyze_bullish(state: FuturesAnalysisState):
    """
    看涨分析师Agent节点
    
    基于第一阶段分析结果，挖掘看涨逻辑和做多机会
    """
    logger.info("="*80)
    logger.info("【步骤2.4】看涨分析师Agent节点 (analyze_bullish)")
    logger.info("="*80)
    logger.info(f"开始时间: {datetime.now().strftime('%H:%M:%S')}")
    
    try:
        logger.debug("正在初始化模型...")
        model = get_model()
        logger.info(f"模型初始化成功: {model.model_name}")
        
        logger.debug("正在创建看涨分析Agent...")
        agent = create_bullish_agent(model)
        logger.info("Agent创建成功")
        
        # 提取第一阶段的结果
        news_content = ""
        if state.get("news_result") and len(state["news_result"]) > 0:
            news_data = state["news_result"][0]
            if news_data.get("status") == "success":
                news_content = news_data.get("content", "")
        
        sentiment_content = ""
        if state.get("sentiment_result") and len(state["sentiment_result"]) > 0:
            sentiment_data = state["sentiment_result"][0]
            if sentiment_data.get("status") == "success":
                sentiment_content = sentiment_data.get("content", "")
        
        fundamental_content = ""
        if state.get("fundamental_result") and len(state["fundamental_result"]) > 0:
            fundamental_data = state["fundamental_result"][0]
            if fundamental_data.get("status") == "success":
                fundamental_content = fundamental_data.get("content", "")
        
        # 构建查询
        query = f"""请基于以下{state['keyword']}({state['symbol']})期货的分析报告，给出专业的看涨分析：

===================
【新闻分析报告】
===================
{news_content if news_content else "新闻分析未能完成"}

===================
【情绪分析报告】
===================
{sentiment_content if sentiment_content else "情绪分析未能完成"}

===================
【基本面技术分析报告】
===================
{fundamental_content if fundamental_content else "基本面分析未能完成"}

请从多头视角深度挖掘投资机会，给出具体的做多策略建议，并保存分析报告。
"""
        logger.info("【Agent输入】")
        logger.info(f"查询内容长度: {len(query)} 字符")
        logger.info("-"*80)
        
        logger.debug("正在调用Agent进行分析...")
        result = agent.invoke({
            "messages": [("user", query)]
        })
        logger.info("Agent调用完成")
        
        # 提取Agent的输出内容
        content = ""
        for msg in result["messages"]:
            if hasattr(msg, 'content') and msg.content:
                content += msg.content + "\n"
        
        logger.info("【Agent输出】")
        logger.info(f"输出长度: {len(content)} 字符")
        logger.info("输出内容预览:")
        logger.info("-"*80)
        logger.info(content[:500])
        if len(content) > 500:
            logger.info(f"... (内容已截断，完整内容共 {len(content)} 字符)")
        logger.info("-"*80)
        
        logger.info(f"完成时间: {datetime.now().strftime('%H:%M:%S')}")
        logger.info("="*80)
        
        return {
            "bullish_result": [{"status": "success", "content": content}]
        }
        
    except Exception as e:
        logger.error("【错误】看涨分析师Agent执行失败")
        logger.error(f"错误信息: {e}")
        logger.info("="*80)
        return {
            "bullish_result": [{"status": "error", "error": str(e)}],
            "errors": [f"看涨分析出错: {e}"]
        }


def analyze_bearish(state: FuturesAnalysisState):
    """
    看跌分析师Agent节点
    
    基于第一阶段分析结果，挖掘看跌逻辑和风险警示
    """
    logger.info("="*80)
    logger.info("【步骤2.5】看跌分析师Agent节点 (analyze_bearish)")
    logger.info("="*80)
    logger.info(f"开始时间: {datetime.now().strftime('%H:%M:%S')}")
    
    try:
        logger.debug("正在初始化模型...")
        model = get_model()
        logger.info(f"模型初始化成功: {model.model_name}")
        
        logger.debug("正在创建看跌分析Agent...")
        agent = create_bearish_agent(model)
        logger.info("Agent创建成功")
        
        # 提取第一阶段的结果
        news_content = ""
        if state.get("news_result") and len(state["news_result"]) > 0:
            news_data = state["news_result"][0]
            if news_data.get("status") == "success":
                news_content = news_data.get("content", "")
        
        sentiment_content = ""
        if state.get("sentiment_result") and len(state["sentiment_result"]) > 0:
            sentiment_data = state["sentiment_result"][0]
            if sentiment_data.get("status") == "success":
                sentiment_content = sentiment_data.get("content", "")
        
        fundamental_content = ""
        if state.get("fundamental_result") and len(state["fundamental_result"]) > 0:
            fundamental_data = state["fundamental_result"][0]
            if fundamental_data.get("status") == "success":
                fundamental_content = fundamental_data.get("content", "")
        
        # 构建查询
        query = f"""请基于以下{state['keyword']}({state['symbol']})期货的分析报告，给出专业的看跌分析：

===================
【新闻分析报告】
===================
{news_content if news_content else "新闻分析未能完成"}

===================
【情绪分析报告】
===================
{sentiment_content if sentiment_content else "情绪分析未能完成"}

===================
【基本面技术分析报告】
===================
{fundamental_content if fundamental_content else "基本面分析未能完成"}

请从空头视角深度挖掘风险因素，给出具体的做空/避险策略建议，并保存分析报告。
"""
        logger.info("【Agent输入】")
        logger.info(f"查询内容长度: {len(query)} 字符")
        logger.info("-"*80)
        
        logger.debug("正在调用Agent进行分析...")
        result = agent.invoke({
            "messages": [("user", query)]
        })
        logger.info("Agent调用完成")
        
        # 提取Agent的输出内容
        content = ""
        for msg in result["messages"]:
            if hasattr(msg, 'content') and msg.content:
                content += msg.content + "\n"
        
        logger.info("【Agent输出】")
        logger.info(f"输出长度: {len(content)} 字符")
        logger.info("输出内容预览:")
        logger.info("-"*80)
        logger.info(content[:500])
        if len(content) > 500:
            logger.info(f"... (内容已截断，完整内容共 {len(content)} 字符)")
        logger.info("-"*80)
        
        logger.info(f"完成时间: {datetime.now().strftime('%H:%M:%S')}")
        logger.info("="*80)
        
        return {
            "bearish_result": [{"status": "success", "content": content}]
        }
        
    except Exception as e:
        logger.error("【错误】看跌分析师Agent执行失败")
        logger.error(f"错误信息: {e}")
        logger.info("="*80)
        return {
            "bearish_result": [{"status": "error", "error": str(e)}],
            "errors": [f"看跌分析出错: {e}"]
        }


def generate_summary(state: FuturesAnalysisState):
    """
    汇总Agent节点
    
    整合所有Agent的分析结果（基础分析 + 观点分析），生成最终报告
    """
    logger.info("="*80)
    logger.info("【步骤3】汇总Agent节点 (generate_summary)")
    logger.info("="*80)
    logger.info(f"开始时间: {datetime.now().strftime('%H:%M:%S')}")
    
    try:
        logger.debug("正在初始化模型...")
        model = get_model()
        logger.info(f"模型初始化成功: {model.model_name}")
        
        logger.debug("正在创建汇总Agent...")
        agent = create_summary_agent(model)
        logger.info("Agent创建成功")
        
        # 提取所有Agent的结果
        logger.info("正在收集所有Agent的分析结果...")
        logger.info("【第一阶段 - 基础分析】")
        
        news_content = ""
        if state.get("news_result") and len(state["news_result"]) > 0:
            news_data = state["news_result"][0]
            if news_data.get("status") == "success":
                news_content = news_data.get("content", "")
                logger.info(f"  ✓ 新闻分析结果: {len(news_content)} 字符")
            else:
                news_content = f"新闻分析出错: {news_data.get('error', '未知错误')}"
                logger.warning(f"  ✗ 新闻分析失败: {news_data.get('error', '未知错误')}")
        else:
            logger.warning("  ✗ 新闻分析结果为空")
        
        sentiment_content = ""
        if state.get("sentiment_result") and len(state["sentiment_result"]) > 0:
            sentiment_data = state["sentiment_result"][0]
            if sentiment_data.get("status") == "success":
                sentiment_content = sentiment_data.get("content", "")
                logger.info(f"  ✓ 情绪分析结果: {len(sentiment_content)} 字符")
            else:
                sentiment_content = f"情绪分析出错: {sentiment_data.get('error', '未知错误')}"
                logger.warning(f"  ✗ 情绪分析失败: {sentiment_data.get('error', '未知错误')}")
        else:
            logger.warning("  ✗ 情绪分析结果为空")
        
        fundamental_content = ""
        if state.get("fundamental_result") and len(state["fundamental_result"]) > 0:
            fundamental_data = state["fundamental_result"][0]
            if fundamental_data.get("status") == "success":
                fundamental_content = fundamental_data.get("content", "")
                logger.info(f"  ✓ 基本面分析结果: {len(fundamental_content)} 字符")
            else:
                fundamental_content = f"基本面分析出错: {fundamental_data.get('error', '未知错误')}"
                logger.warning(f"  ✗ 基本面分析失败: {fundamental_data.get('error', '未知错误')}")
        else:
            logger.warning("  ✗ 基本面分析结果为空")
        
        # 提取第二阶段观点分析师的结果
        logger.info("【第二阶段 - 观点分析】")
        
        bullish_content = ""
        if state.get("bullish_result") and len(state["bullish_result"]) > 0:
            bullish_data = state["bullish_result"][0]
            if bullish_data.get("status") == "success":
                bullish_content = bullish_data.get("content", "")
                logger.info(f"  ✓ 看涨分析结果: {len(bullish_content)} 字符")
            else:
                bullish_content = f"看涨分析出错: {bullish_data.get('error', '未知错误')}"
                logger.warning(f"  ✗ 看涨分析失败: {bullish_data.get('error', '未知错误')}")
        else:
            logger.warning("  ✗ 看涨分析结果为空")
        
        bearish_content = ""
        if state.get("bearish_result") and len(state["bearish_result"]) > 0:
            bearish_data = state["bearish_result"][0]
            if bearish_data.get("status") == "success":
                bearish_content = bearish_data.get("content", "")
                logger.info(f"  ✓ 看跌分析结果: {len(bearish_content)} 字符")
            else:
                bearish_content = f"看跌分析出错: {bearish_data.get('error', '未知错误')}"
                logger.warning(f"  ✗ 看跌分析失败: {bearish_data.get('error', '未知错误')}")
        else:
            logger.warning("  ✗ 看跌分析结果为空")
        
        # 构建汇总查询
        summary_query = f"""请基于以下五个分析报告生成综合投资报告：

分析品种: {state['keyword']} ({state['symbol']})

===================
【新闻分析报告】
===================
{news_content if news_content else "新闻分析未能完成"}

===================
【情绪分析报告】
===================
{sentiment_content if sentiment_content else "情绪分析未能完成"}

===================
【基本面技术分析报告】
===================
{fundamental_content if fundamental_content else "基本面分析未能完成"}

===================
【看涨分析报告（多头视角）】
===================
{bullish_content if bullish_content else "看涨分析未能完成"}

===================
【看跌分析报告（空头视角）】
===================
{bearish_content if bearish_content else "看跌分析未能完成"}

请整合以上所有信息，特别关注看涨和看跌分析师的对立观点，形成平衡的投资判断，生成一份完整的综合投资报告，并保存到文件。
"""
        
        logger.info("【Agent输入】")
        logger.info(f"输入内容总长度: {len(summary_query)} 字符")
        logger.info(f"  - 新闻部分: {len(news_content)} 字符")
        logger.info(f"  - 情绪部分: {len(sentiment_content)} 字符")
        logger.info(f"  - 基本面部分: {len(fundamental_content)} 字符")
        logger.info(f"  - 看涨分析部分: {len(bullish_content)} 字符")
        logger.info(f"  - 看跌分析部分: {len(bearish_content)} 字符")
        logger.info("-"*80)
        
        logger.debug("正在调用Agent进行汇总...")
        result = agent.invoke({
            "messages": [("user", summary_query)]
        })
        logger.info("Agent调用完成")
        
        # 提取最终报告内容
        final_content = ""
        for msg in result["messages"]:
            if hasattr(msg, 'content') and msg.content:
                final_content += msg.content + "\n"
        
        logger.info("【Agent输出】")
        logger.info(f"最终报告长度: {len(final_content)} 字符")
        logger.info("最终报告内容:")
        logger.info("-"*80)
        logger.info(final_content)
        logger.info("-"*80)
        
        logger.info(f"完成时间: {datetime.now().strftime('%H:%M:%S')}")
        logger.info("="*80)
        
        return {
            "final_report": final_content
        }
        
    except Exception as e:
        logger.error("【错误】汇总Agent执行失败")
        logger.error(f"错误信息: {e}")
        logger.info("="*80)
        return {
            "final_report": f"汇总报告生成失败: {e}",
            "errors": [f"汇总分析出错: {e}"]
        }


def end_workflow(state: FuturesAnalysisState):
    """
    工作流结束节点
    
    打印完成信息
    """
    logger.info("="*80)
    logger.info("【步骤4】工作流结束节点 (end_workflow)")
    logger.info("="*80)
    logger.info(f"结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"分析品种: {state['keyword']} ({state['symbol']})")
    
    logger.info("【执行结果统计】")
    
    # 统计各Agent的执行情况
    news_count = len(state.get("news_result", []))
    sentiment_count = len(state.get("sentiment_result", []))
    fundamental_count = len(state.get("fundamental_result", []))
    bullish_count = len(state.get("bullish_result", []))
    bearish_count = len(state.get("bearish_result", []))
    
    logger.info(f"  第一阶段 - 基础分析:")
    logger.info(f"    新闻分析结果数: {news_count}")
    logger.info(f"    情绪分析结果数: {sentiment_count}")
    logger.info(f"    基本面分析结果数: {fundamental_count}")
    
    logger.info(f"  第二阶段 - 观点分析:")
    logger.info(f"    看涨分析结果数: {bullish_count}")
    logger.info(f"    看跌分析结果数: {bearish_count}")
    
    # 统计成功和失败的情况
    news_success = 0
    if news_count > 0 and state["news_result"][0].get("status") == "success":
        news_success = 1
    
    sentiment_success = 0
    if sentiment_count > 0 and state["sentiment_result"][0].get("status") == "success":
        sentiment_success = 1
    
    fundamental_success = 0
    if fundamental_count > 0 and state["fundamental_result"][0].get("status") == "success":
        fundamental_success = 1
    
    bullish_success = 0
    if bullish_count > 0 and state["bullish_result"][0].get("status") == "success":
        bullish_success = 1
    
    bearish_success = 0
    if bearish_count > 0 and state["bearish_result"][0].get("status") == "success":
        bearish_success = 1
    
    logger.info(f"  成功执行的Agent: {news_success + sentiment_success + fundamental_success + bullish_success + bearish_success}/5")
    logger.info(f"    第一阶段:")
    logger.info(f"      - 新闻Agent: {'成功' if news_success else '失败'}")
    logger.info(f"      - 情绪Agent: {'成功' if sentiment_success else '失败'}")
    logger.info(f"      - 基本面Agent: {'成功' if fundamental_success else '失败'}")
    logger.info(f"    第二阶段:")
    logger.info(f"      - 看涨分析师: {'成功' if bullish_success else '失败'}")
    logger.info(f"      - 看跌分析师: {'成功' if bearish_success else '失败'}")
    
    # 最终报告信息
    final_report = state.get("final_report", "")
    if final_report:
        logger.info("  最终报告: 已生成")
        logger.info(f"    报告长度: {len(final_report)} 字符")
    else:
        logger.warning("  最终报告: 未生成")
    
    # 错误信息
    if state.get("errors"):
        logger.warning(f"【警告】执行过程中出现 {len(state['errors'])} 个错误:")
        for idx, error in enumerate(state["errors"], 1):
            logger.warning(f"  {idx}. {error}")
    else:
        logger.info("【状态】执行过程无错误")
    
    logger.info("="*80)
    
    return {}


# ============== 工作流构建 ==============
def create_workflow():
    """
    创建并编译工作流
    
    工作流结构（两阶段并行）:
    
    第一阶段:
    start -> [news_agent, sentiment_agent, fundamental_agent] (并行) -> first_phase_join
    
    第二阶段（在第一阶段全部完成后触发）:
    first_phase_join -> [bullish_agent, bearish_agent] (并行) -> second_phase_join
    
    汇总（在第二阶段全部完成后触发）:
    second_phase_join -> summary_agent -> end
    """
    from langgraph.graph import END
    
    # 创建状态图
    workflow = StateGraph(FuturesAnalysisState)
    
    # 添加节点
    workflow.add_node("start", start_analysis)
    workflow.add_node("news_agent", analyze_news)
    workflow.add_node("sentiment_agent", analyze_sentiment)
    workflow.add_node("fundamental_agent", analyze_fundamental)
    workflow.add_node("bullish_agent", analyze_bullish)
    workflow.add_node("bearish_agent", analyze_bearish)
    workflow.add_node("summary_agent", generate_summary)
    workflow.add_node("end", end_workflow)
    
    # 添加汇聚节点（在边配置部分定义）
    # first_phase_join 和 second_phase_join 在下面的边配置中通过 add_node 添加
    
    # 添加边
    # 从start节点分发到三个并行Agent（第一阶段）
    workflow.set_entry_point("start")
    
    # 使用Send实现第一阶段并行执行
    def dispatch_first_phase(state: FuturesAnalysisState):
        """分发到三个基础分析Agent"""
        logger.info("="*80)
        logger.info("【工作流分发】第一阶段：并行分发任务到三个基础Agent")
        logger.info("="*80)
        logger.info("目标节点: news_agent, sentiment_agent, fundamental_agent")
        logger.info(f"分发时间: {datetime.now().strftime('%H:%M:%S')}")
        logger.info("="*80)
        
        return [
            Send("news_agent", state),
            Send("sentiment_agent", state),
            Send("fundamental_agent", state)
        ]
    
    workflow.add_conditional_edges(
        "start",
        dispatch_first_phase,
        ["news_agent", "sentiment_agent", "fundamental_agent"]
    )
    
    # 汇聚节点 - 只记录日志和更新状态，不进行路由
    def first_phase_join(state: FuturesAnalysisState):
        """
        第一阶段汇聚节点
        
        记录三个基础Agent的完成状态
        """
        has_news = len(state.get("news_result", [])) > 0
        has_sentiment = len(state.get("sentiment_result", [])) > 0
        has_fundamental = len(state.get("fundamental_result", [])) > 0
        
        completed = sum([has_news, has_sentiment, has_fundamental])
        
        logger.info("="*80)
        logger.info(f"【第一阶段汇聚】检查完成状态: {completed}/3")
        logger.info(f"  新闻: {'✓' if has_news else '○'}, 情绪: {'✓' if has_sentiment else '○'}, 基本面: {'✓' if has_fundamental else '○'}")
        logger.info("="*80)
        
        # 返回状态更新，不在这里做路由决策
        return {"first_phase_ready": has_news and has_sentiment and has_fundamental}
    
    # 第一阶段路由函数
    def route_first_phase(state: FuturesAnalysisState):
        """路由函数：检查第一阶段是否全部完成"""
        has_news = len(state.get("news_result", [])) > 0
        has_sentiment = len(state.get("sentiment_result", [])) > 0
        has_fundamental = len(state.get("fundamental_result", [])) > 0
        
        if has_news and has_sentiment and has_fundamental:
            logger.info("【路由决策】第一阶段全部完成，分发到第二阶段！")
            return "dispatch_second"
        else:
            logger.info("【路由决策】第一阶段未完成，等待...")
            return "wait"
    
    # 添加汇聚节点到工作流
    workflow.add_node("first_phase_join", first_phase_join)
    
    # 三个Agent完成后都连接到汇聚节点
    workflow.add_edge("news_agent", "first_phase_join")
    workflow.add_edge("sentiment_agent", "first_phase_join")
    workflow.add_edge("fundamental_agent", "first_phase_join")
    
    # 汇聚节点通过条件边路由，使用Send直接分发到第二阶段Agent
    def route_and_dispatch_second(state: FuturesAnalysisState):
        """路由函数：检查第一阶段是否全部完成，如果完成则分发到第二阶段"""
        has_news = len(state.get("news_result", [])) > 0
        has_sentiment = len(state.get("sentiment_result", [])) > 0
        has_fundamental = len(state.get("fundamental_result", [])) > 0
        
        if has_news and has_sentiment and has_fundamental:
            logger.info("="*80)
            logger.info("【工作流分发】第一阶段全部完成，分发到第二阶段！")
            logger.info("="*80)
            logger.info("目标节点: bullish_agent, bearish_agent")
            logger.info(f"分发时间: {datetime.now().strftime('%H:%M:%S')}")
            logger.info("="*80)
            # 使用Send直接分发到第二阶段Agent
            return [
                Send("bullish_agent", state),
                Send("bearish_agent", state)
            ]
        else:
            logger.info("【路由决策】第一阶段未完成，等待...")
            return END
    
    workflow.add_conditional_edges(
        "first_phase_join",
        route_and_dispatch_second,
        ["bullish_agent", "bearish_agent", END]
    )
    
    # 第二阶段汇聚逻辑
    def second_phase_join(state: FuturesAnalysisState):
        """第二阶段汇聚节点"""
        has_bullish = len(state.get("bullish_result", [])) > 0
        has_bearish = len(state.get("bearish_result", [])) > 0
        
        completed = sum([has_bullish, has_bearish])
        
        logger.info("="*80)
        logger.info(f"【第二阶段汇聚】检查完成状态: {completed}/2")
        logger.info(f"  看涨: {'✓' if has_bullish else '○'}, 看跌: {'✓' if has_bearish else '○'}")
        logger.info("="*80)
        
        return {"second_phase_ready": has_bullish and has_bearish}
    
    # 第二阶段路由函数
    def route_second_phase(state: FuturesAnalysisState):
        """路由函数：检查第二阶段是否全部完成"""
        has_bullish = len(state.get("bullish_result", [])) > 0
        has_bearish = len(state.get("bearish_result", [])) > 0
        
        if has_bullish and has_bearish:
            logger.info("【路由决策】第二阶段全部完成，触发汇总！")
            return "summary"
        else:
            logger.info("【路由决策】第二阶段未完成，等待...")
            return "wait"
    
    workflow.add_node("second_phase_join", second_phase_join)
    
    # 两个观点分析师完成后汇聚
    workflow.add_edge("bullish_agent", "second_phase_join")
    workflow.add_edge("bearish_agent", "second_phase_join")
    
    # 第二阶段汇聚后路由到汇总或结束
    workflow.add_conditional_edges(
        "second_phase_join",
        route_second_phase,
        {
            "summary": "summary_agent",
            "wait": END
        }
    )
    
    # summary完成后到end
    workflow.add_edge("summary_agent", "end")
    
    # 编译工作流
    return workflow.compile()


# ============== 便捷函数 ==============
def analyze_futures(symbol: str, keyword: str = None) -> Dict[str, Any]:
    """
    分析期货品种的便捷函数
    
    参数:
        symbol (str): 期货品种代码，如 "ss" (不锈钢)
        keyword (str): 搜索关键词，如 "不锈钢"，默认为symbol
    
    返回:
        Dict: 包含分析结果的字典
    """
    logger.info("="*80)
    logger.info("【期货分析工作流启动】")
    logger.info("="*80)
    logger.info(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"期货品种代码: {symbol}")
    
    if keyword is None:
        # 尝试从symbol映射中文名
        from tools.futures_analyzer import FuturesAnalyzer
        analyzer = FuturesAnalyzer(symbol)
        keyword = analyzer.chinese_name
        logger.info(f"自动映射中文名: {keyword}")
    else:
        logger.info(f"搜索关键词: {keyword}")
    
    logger.info("="*80)
    
    # 创建工作流
    logger.debug("正在创建工作流...")
    app = create_workflow()
    logger.info("工作流创建完成")
    
    # 执行工作流
    logger.info("正在执行工作流...")
    logger.info("="*80)
    
    result = app.invoke({
        "symbol": symbol,
        "keyword": keyword,
        "news_result": [],
        "sentiment_result": [],
        "fundamental_result": [],
        "bullish_result": [],
        "bearish_result": [],
        "errors": [],
        "first_phase_ready": False,
        "second_phase_ready": False,
        "final_report": "",
        "report_path": ""
    })
    
    logger.info("="*80)
    logger.info("【工作流执行完成】")
    logger.info("="*80)
    logger.info(f"结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("="*80)
    
    return result


# ============== 主程序 ==============
if __name__ == "__main__":
    # 测试
    logger.info("#"*80)
    logger.info("# 期货多智能体分析工作流 - 测试程序")
    logger.info("#"*80)
    
    logger.info("开始测试期货分析工作流...")
    
    # 分析不锈钢期货
    result = analyze_futures("ss", "不锈钢")
    
    logger.info("#"*80)
    logger.info("# 最终结果预览")
    logger.info("#"*80)
    
    if result.get("final_report"):
        logger.info(f"最终报告已生成，长度: {len(result['final_report'])} 字符")
        logger.info("报告内容:")
        logger.info("-"*80)
        logger.info(result["final_report"])
        logger.info("-"*80)
    else:
        logger.warning("未生成最终报告")
    
    logger.info("#"*80)
    logger.info("# 测试程序结束")
    logger.info("#"*80)
