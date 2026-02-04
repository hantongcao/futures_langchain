"""
文件保存工具 - 用于保存各类分析报告
"""
import os
from datetime import datetime
from langchain_core.tools import tool


def _ensure_reports_dir():
    """确保reports目录存在"""
    reports_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "reports")
    os.makedirs(reports_dir, exist_ok=True)
    return reports_dir


@tool
def save_news_to_markdown(content: str, keyword: str = "期货") -> str:
    """
    将新闻内容保存为Markdown格式文件
    
    参数:
        content (str): 要保存的新闻内容字符串
        keyword (str): 搜索关键词，用于文件名
    
    返回:
        str: 保存的文件路径
    """
    try:
        reports_dir = _ensure_reports_dir()
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = os.path.join(reports_dir, f"news_{keyword}_{timestamp}.md")
        
        # 构建报告头部
        header = f"""# 期货新闻分析报告

**搜集时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**关键词**: {keyword}

---

"""
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(header + content)
        
        return f"新闻文件已成功保存至: {filename}"
    except Exception as e:
        return f"保存新闻文件失败：{str(e)}"


@tool
def save_sentiment_to_markdown(content: str, keyword: str = "期货") -> str:
    """
    将情绪分析内容保存为Markdown格式文件
    
    参数:
        content (str): 要保存的情绪分析内容字符串
        keyword (str): 分析的品种关键词
    
    返回:
        str: 保存的文件路径
    """
    try:
        reports_dir = _ensure_reports_dir()
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = os.path.join(reports_dir, f"sentiment_{keyword}_{timestamp}.md")
        
        header = f"""# 期货市场情绪分析报告

**分析时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**分析品种**: {keyword}

---

"""
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(header + content)
        
        return f"情绪分析文件已成功保存至: {filename}"
    except Exception as e:
        return f"保存情绪分析文件失败：{str(e)}"


@tool
def save_fundamental_to_markdown(content: str, symbol: str = "期货") -> str:
    """
    将基本面分析内容保存为Markdown格式文件
    
    参数:
        content (str): 要保存的基本面分析内容字符串
        symbol (str): 期货品种代码
    
    返回:
        str: 保存的文件路径
    """
    try:
        reports_dir = _ensure_reports_dir()
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = os.path.join(reports_dir, f"fundamental_{symbol}_{timestamp}.md")
        
        header = f"""# 期货基本面技术分析报告

**分析时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**分析品种**: {symbol.upper()}

---

"""
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(header + content)
        
        return f"基本面分析文件已成功保存至: {filename}"
    except Exception as e:
        return f"保存基本面分析文件失败：{str(e)}"


@tool
def save_summary_to_markdown(content: str, symbol: str = "期货") -> str:
    """
    将汇总分析报告保存为Markdown格式文件
    
    参数:
        content (str): 要保存的汇总分析内容字符串
        symbol (str): 期货品种代码
    
    返回:
        str: 保存的文件路径
    """
    try:
        reports_dir = _ensure_reports_dir()
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = os.path.join(reports_dir, f"summary_{symbol}_{timestamp}.md")
        
        header = f"""# 期货综合分析报告

**报告生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**分析品种**: {symbol.upper()}

---

"""
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(header + content)
        
        return f"汇总分析报告已成功保存至: {filename}"
    except Exception as e:
        return f"保存汇总分析报告失败：{str(e)}"


@tool
def save_bullish_to_markdown(content: str, symbol: str = "期货") -> str:
    """
    将看涨分析报告保存为Markdown格式文件
    
    参数:
        content (str): 要保存的看涨分析内容字符串
        symbol (str): 期货品种代码
    
    返回:
        str: 保存的文件路径
    """
    try:
        reports_dir = _ensure_reports_dir()
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = os.path.join(reports_dir, f"bullish_{symbol}_{timestamp}.md")
        
        header = f"""# 期货看涨分析报告（多头视角）

**分析时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**分析品种**: {symbol.upper()}

---

"""
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(header + content)
        
        return f"看涨分析报告已成功保存至: {filename}"
    except Exception as e:
        return f"保存看涨分析报告失败：{str(e)}"


@tool
def save_bearish_to_markdown(content: str, symbol: str = "期货") -> str:
    """
    将看跌分析报告保存为Markdown格式文件
    
    参数:
        content (str): 要保存的看跌分析内容字符串
        symbol (str): 期货品种代码
    
    返回:
        str: 保存的文件路径
    """
    try:
        reports_dir = _ensure_reports_dir()
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = os.path.join(reports_dir, f"bearish_{symbol}_{timestamp}.md")
        
        header = f"""# 期货看跌分析报告（空头视角）

**分析时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**分析品种**: {symbol.upper()}

---

"""
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(header + content)
        
        return f"看跌分析报告已成功保存至: {filename}"
    except Exception as e:
        return f"保存看跌分析报告失败：{str(e)}"


if __name__ == "__main__":
    # 测试
    result = save_news_to_markdown.invoke({"content": "# 测试内容\n这是一条测试新闻", "keyword": "测试"})
    print(result)
