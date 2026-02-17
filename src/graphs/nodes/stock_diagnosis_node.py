"""
诊股节点 - 分析指定股票的基本面和技术面
"""
import os
import json
from jinja2 import Template
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from coze_coding_dev_sdk import LLMClient, SearchClient
from graphs.state import StockDiagnosisInput, StockDiagnosisOutput


def stock_diagnosis_node(state: StockDiagnosisInput, config: RunnableConfig, runtime: Runtime[Context]) -> StockDiagnosisOutput:
    """
    title: 智能诊股
    desc: 深度分析指定股票的基本面、技术面和投资价值
    integrations: 大语言模型, 网页搜索
    """
    ctx = runtime.context
    
    # 读取大模型配置
    cfg_file = os.path.join(os.getenv("COZE_WORKSPACE_PATH"), config['metadata']['llm_cfg'])
    with open(cfg_file, 'r') as fd:
        _cfg = json.load(fd)
    
    llm_config = _cfg.get("config", {})
    sp = _cfg.get("sp", "")
    up = _cfg.get("up", "")
    
    # 渲染用户提示词
    up_tpl = Template(up)
    user_prompt_content = up_tpl.render({"user_input": state.user_input})
    
    # 先进行网页搜索获取股票信息
    search_client = SearchClient(ctx=ctx)
    
    # 构建搜索查询
    search_query = f"{state.user_input} 股票 基本面 财务 数据"
    search_response = search_client.web_search(
        query=search_query,
        count=5,
        need_summary=True
    )
    
    # 整理搜索结果
    search_context = ""
    if search_response.web_items:
        search_context = "\n".join([
            f"- {item.title}: {item.snippet}"
            for item in search_response.web_items[:3]
        ])
    
    # 初始化LLM客户端
    llm_client = LLMClient(ctx=ctx)
    
    # 构建消息
    messages = [
        SystemMessage(content=sp),
        HumanMessage(content=f"{user_prompt_content}\n\n参考信息：\n{search_context}")
    ]
    
    # 调用大模型
    response = llm_client.invoke(
        messages=messages,
        model=llm_config.get("model", "doubao-seed-1-8-251228"),
        temperature=llm_config.get("temperature", 0.7),
        max_completion_tokens=llm_config.get("max_completion_tokens", 3000)
    )
    
    # 解析响应
    result_text = ""
    if isinstance(response.content, str):
        result_text = response.content.strip()
    elif isinstance(response.content, list):
        if response.content and isinstance(response.content[0], str):
            result_text = " ".join(response.content).strip()
        else:
            text_parts = [item.get("text", "") for item in response.content if isinstance(item, dict) and item.get("type") == "text"]
            result_text = " ".join(text_parts).strip()
    
    # 提取股票代码和名称
    import re
    code_pattern = r'\d{6}'
    codes = re.findall(code_pattern, state.user_input)
    stock_code = codes[0] if codes else ""
    
    # 简化：股票名称从输入中提取（实际可以更精确）
    stock_name = state.user_input.replace(stock_code, "").strip() if stock_code else state.user_input
    
    # 构建分析结果
    analysis_result = {
        "stock_code": stock_code,
        "stock_name": stock_name,
        "analysis_report": result_text,
        "fundamental_analysis": "基本面分析已包含在报告中",
        "technical_analysis": "技术面分析已包含在报告中",
        "investment_advice": "投资建议已包含在报告中"
    }
    
    return StockDiagnosisOutput(
        stock_analysis=analysis_result,
        stock_code=stock_code,
        stock_name=stock_name
    )
