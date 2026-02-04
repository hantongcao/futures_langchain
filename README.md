# 期货多智能体分析系统

基于 LangGraph 和 DeepSeek 的期货智能分析系统，采用多智能体协作架构，实现新闻分析、情绪分析、技术分析三位一体。

## 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                     期货多智能体分析系统                      │
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

## 功能特点

- **新闻搜集Agent**: 自动搜索期货相关新闻，分类整理利好/利空信息
- **情绪分析Agent**: 分析市场情绪，判断多空力量对比
- **基本面分析Agent**: 获取实时行情数据，计算技术指标
- **汇总报告Agent**: 整合三方分析，生成专业投资报告

## 安装

### 1. 克隆项目

```bash
cd futures-langchain
```

### 2. 安装依赖

```bash
pip install -e .
```

或使用 uv:

```bash
uv pip install -e .
```

### 3. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 文件，填入你的 API 密钥
```

需要配置的 API 密钥:
- `ZHIPU_API_KEY`: 智谱 AI API 密钥（用于网络搜索）
- `DEEPSEEK_API_KEY`: DeepSeek API 密钥（用于 LLM 推理）

## 使用方法

### 命令行使用

```bash
# 分析不锈钢期货
python main.py --symbol ss

# 分析铜期货
python main.py --symbol cu --keyword 铜

# 分析螺纹钢期货
python main.py --symbol rb --keyword 螺纹钢

# 列出所有支持的品种
python main.py --list-symbols
```

### Python API 使用

```python
from workflow import analyze_futures

# 分析不锈钢期货
result = analyze_futures(symbol="ss", keyword="不锈钢")

# 获取最终报告
final_report = result["final_report"]
print(final_report)
```

## 支持的期货品种

| 代码 | 品种 | 交易所 |
|------|------|--------|
| ss | 不锈钢 | SHFE |
| cu | 铜 | SHFE |
| rb | 螺纹钢 | SHFE |
| pb | 铅 | SHFE |
| al | 铝 | SHFE |
| zn | 锌 | SHFE |
| ni | 镍 | SHFE |
| au | 黄金 | SHFE |
| ag | 白银 | SHFE |
| sc | 原油 | INE |
| m | 豆粕 | DCE |
| y | 豆油 | DCE |
| c | 玉米 | DCE |
| i | 铁矿石 | DCE |
| sr | 白糖 | CZCE |
| cf | 棉花 | CZCE |
| ta | PTA | CZCE |
| ma | 甲醇 | CZCE |
| ... | ... | ... |

完整列表请运行 `python main.py --list-symbols`

## 项目结构

```
futures-langchain/
├── agents/                 # 智能体模块
│   ├── __init__.py
│   ├── news_agent.py       # 新闻搜集Agent
│   ├── sentiment_agent.py  # 情绪分析Agent
│   ├── fundamental_agent.py # 基本面分析Agent
│   └── summary_agent.py    # 汇总报告Agent
├── tools/                  # 工具模块
│   ├── __init__.py
│   ├── futures_analyzer.py # 期货数据分析类
│   ├── web_search.py       # 网络搜索工具
│   └── file_saver.py       # 文件保存工具
├── reports/                # 报告输出目录
├── workflow.py             # 主工作流定义
├── main.py                 # 命令行入口
├── pyproject.toml          # 项目配置
├── .env.example            # 环境变量模板
└── README.md               # 项目说明
```

## 工作流程

1. **并行分析**: 三个子 Agent 同时执行
   - 新闻搜集 Agent 搜索并分析相关新闻
   - 情绪分析 Agent 分析市场情绪
   - 基本面分析 Agent 获取并分析行情数据

2. **结果汇总**: 汇总 Agent 整合三方分析结果

3. **生成报告**: 输出专业的综合投资报告

## 报告内容

生成的报告包含:

- **执行摘要**: 核心观点、投资评级、操作建议
- **新闻面分析**: 重要新闻回顾、利好/利空因素
- **情绪分析**: 整体情绪、多空力量对比
- **技术分析**: 价格走势、关键指标、支撑阻力
- **综合分析**: 多维度一致性分析、情景分析
- **投资建议**: 操作策略、入场/止损/止盈价位
- **风险提示**: 市场风险、操作风险

## 技术栈

- **LangGraph**: 多智能体工作流编排
- **LangChain**: LLM 应用框架
- **DeepSeek**: 大语言模型
- **Zhipu AI**: 网络搜索
- **akshare**: 期货数据获取
- **pandas/numpy**: 数据分析

## 注意事项

1. 本系统仅供参考，不构成投资建议
2. 期货交易风险较大，请谨慎决策
3. API 调用可能产生费用，请注意使用量
4. 数据延迟可能存在，请以交易所数据为准

## License

MIT License

## 联系方式

如有问题或建议，欢迎提交 Issue 或 PR。
