"""
选股节点 - 根据用户条件筛选股票
"""
import os
import json
from jinja2 import Template
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from coze_coding_dev_sdk import LLMClient, SearchClient
from graphs.state import StockSelectionInput, StockSelectionOutput


def stock_selection_node(state: StockSelectionInput, config: RunnableConfig, runtime: Runtime[Context]) -> StockSelectionOutput:
    """
    title: 智能选股
    desc: 根据用户输入的条件，搜索并推荐符合条件的股票
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
    
    # 先进行网页搜索获取相关信息
    search_client = SearchClient(ctx=ctx)
    
    # 构建搜索查询
    search_query = f"A股 {state.user_input} 推荐 筛选"
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
        max_completion_tokens=llm_config.get("max_completion_tokens", 2000)
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
    
    # 提取股票代码和名称（简化处理，实际可以更精确）
    stock_codes = []
    stock_names = []
    
    # 尝试提取股票代码（6位数字）
    import re
    code_pattern = r'\d{6}'
    codes = re.findall(code_pattern, result_text)
    stock_codes = codes[:5]  # 最多返回5个
    
    # 返回结果
    return StockSelectionOutput(
        stock_codes=stock_codes,
        stock_names=stock_names,
        selection_reason=result_text
    )
