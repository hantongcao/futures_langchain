# 期货多智能体分析系统 - 项目总结

## 项目概述

本项目是一个基于 **LangGraph** 和 **DeepSeek** 的期货智能分析系统，采用多智能体协作架构，实现了新闻分析、情绪分析、技术分析三位一体的综合分析能力。

## 核心特性

### 1. 多智能体并行架构

```
┌─────────────────────────────────────────────────────────────┐
│                    期货多智能体分析系统                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  新闻搜集Agent │  │  情绪分析Agent │  │ 基本面分析Agent│      │
│  │   (并行)      │  │   (并行)      │  │   (并行)      │      │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘      │
│         │                 │                 │              │
│         └─────────────────┼─────────────────┘              │
│                           ▼                                │
│                  ┌─────────────────┐                       │
│                  │   汇总报告Agent  │                       │
│                  └────────┬────────┘                       │
│                           ▼                                │
│                  ┌─────────────────┐                       │
│                  │   综合投资报告   │                       │
│                  └─────────────────┘                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 2. 四个专业Agent

| Agent | 功能 | 工具 |
|-------|------|------|
| **新闻搜集Agent** | 搜索期货新闻，分类整理利好/利空 | web_search, save_news_to_markdown |
| **情绪分析Agent** | 分析市场情绪，判断多空力量 | save_sentiment_to_markdown |
| **基本面分析Agent** | 获取行情数据，计算技术指标 | analyze_futures_data, save_fundamental_to_markdown |
| **汇总报告Agent** | 整合三方分析，生成投资报告 | save_summary_to_markdown |

### 3. 数据支持

- **行情数据**: 通过 akshare 获取实时期货数据
- **新闻搜索**: 通过智谱AI进行网络搜索
- **技术指标**: RSI、MACD、MA、波动率等
- **支持品种**: 50+ 种期货品种（上期所、大商所、郑商所、上期能源、广期所）

## 项目结构

```
futures-langchain/
├── agents/                    # 智能体模块
│   ├── __init__.py
│   ├── news_agent.py          # 新闻搜集Agent
│   ├── sentiment_agent.py     # 情绪分析Agent
│   ├── fundamental_agent.py   # 基本面分析Agent
│   └── summary_agent.py       # 汇总报告Agent
├── tools/                     # 工具模块
│   ├── __init__.py
│   ├── futures_analyzer.py    # 期货数据分析类
│   ├── web_search.py          # 网络搜索工具
│   └── file_saver.py          # 文件保存工具
├── tests/                     # 测试模块
│   ├── __init__.py
│   ├── test_futures_analyzer.py
│   ├── test_agents.py
│   └── test_workflow.py
├── reports/                   # 报告输出目录
├── workflow.py                # 主工作流定义
├── main.py                    # 命令行入口
├── demo.py                    # 演示脚本
├── pyproject.toml             # 项目配置
├── .env.example               # 环境变量模板
├── README.md                  # 项目说明
└── PROJECT_SUMMARY.md         # 项目总结
```

## 技术栈

- **LangGraph**: 多智能体工作流编排
- **LangChain**: LLM 应用框架
- **DeepSeek**: 大语言模型（推理）
- **Zhipu AI**: 网络搜索
- **akshare**: 期货数据获取
- **pandas/numpy**: 数据分析

## 使用方法

### 1. 安装依赖

```bash
pip install -e .
```

### 2. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 文件，填入 API 密钥
```

### 3. 命令行使用

```bash
# 分析不锈钢期货
python main.py --symbol ss

# 分析铜期货
python main.py --symbol cu --keyword 铜

# 列出所有支持的品种
python main.py --list-symbols
```

### 4. Python API 使用

```python
from workflow import analyze_futures

# 分析不锈钢期货
result = analyze_futures(symbol="ss", keyword="不锈钢")

# 获取最终报告
final_report = result["final_report"]
print(final_report)
```

## 报告内容

生成的综合投资报告包含:

1. **执行摘要**: 核心观点、投资评级、操作建议
2. **新闻面分析**: 重要新闻回顾、利好/利空因素
3. **情绪分析**: 整体情绪、多空力量对比
4. **技术分析**: 价格走势、关键指标、支撑阻力
5. **综合分析**: 多维度一致性分析、情景分析
6. **投资建议**: 操作策略、入场/止损/止盈价位
7. **风险提示**: 市场风险、操作风险

## 工作流程

1. **并行分析**: 三个子Agent同时执行
   - 新闻搜集Agent搜索并分析相关新闻
   - 情绪分析Agent分析市场情绪
   - 基本面分析Agent获取并分析行情数据

2. **结果汇总**: 汇总Agent整合三方分析结果

3. **生成报告**: 输出专业的综合投资报告

## 关键代码说明

### 工作流定义 (workflow.py)

```python
# 创建状态图
workflow = StateGraph(FuturesAnalysisState)

# 添加节点
workflow.add_node("start", start_analysis)
workflow.add_node("news_agent", analyze_news)
workflow.add_node("sentiment_agent", analyze_sentiment)
workflow.add_node("fundamental_agent", analyze_fundamental)
workflow.add_node("summary_agent", generate_summary)
workflow.add_node("end", end_workflow)

# 使用Send实现并行执行
def dispatch_parallel(state: FuturesAnalysisState):
    return [
        Send("news_agent", state),
        Send("sentiment_agent", state),
        Send("fundamental_agent", state)
    ]

workflow.add_conditional_edges("start", dispatch_parallel)
```

### 期货数据分析 (tools/futures_analyzer.py)

```python
class FuturesAnalyzer:
    """期货数据分析类"""
    
    def get_recent_30_days(self) -> pd.DataFrame:
        """获取最近30天数据"""
        
    def get_key_indicators(self) -> Dict:
        """获取关键技术指标"""
        # RSI、MACD、MA、波动率等
```

## 测试

项目包含完整的测试套件:

```bash
# 测试期货数据分析
python tests/test_futures_analyzer.py

# 测试各个Agent
python tests/test_agents.py

# 测试工作流
python tests/test_workflow.py

# 运行演示
python demo.py
```

## 注意事项

1. 本系统仅供参考，不构成投资建议
2. 期货交易风险较大，请谨慎决策
3. API 调用可能产生费用，请注意使用量
4. 数据延迟可能存在，请以交易所数据为准

## 后续优化方向

1. **增加更多数据源**: 接入更多行情数据源
2. **优化并行效率**: 使用异步IO提高并发性能
3. **增加回测功能**: 验证分析策略的有效性
4. **Web界面**: 开发可视化操作界面
5. **定时任务**: 支持定时自动分析
6. **邮件通知**: 分析完成后发送邮件通知

## 总结

本项目成功实现了一个完整的期货多智能体分析系统，通过LangGraph的并行工作流机制，实现了三个专业Agent的协同工作，能够自动生成专业的投资分析报告。系统设计清晰、模块化程度高、易于扩展和维护。
