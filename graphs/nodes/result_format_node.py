"""
结果汇总节点 - 将分析结果格式化
"""
import os
import json
from jinja2 import Template
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from coze_coding_dev_sdk import LLMClient
from graphs.state import ResultFormatInput, ResultFormatOutput


def result_format_node(state: ResultFormatInput, config: RunnableConfig, runtime: Runtime[Context]) -> ResultFormatOutput:
    """
    title: 结果汇总
    desc: 将选股或诊股的结果整理成易读的格式
    integrations: 大语言模型
    """
    ctx = runtime.context
    
    # 读取大模型配置
    cfg_file = os.path.join(os.getenv("COZE_WORKSPACE_PATH"), config['metadata']['llm_cfg'])
    with open(cfg_file, 'r') as fd:
        _cfg = json.load(fd)
    
    llm_config = _cfg.get("config", {})
    sp = _cfg.get("sp", "")
    up = _cfg.get("up", "")
    
    # 准备上下文信息
    if state.intent == "选股":
        context_info = f"""
        选股理由：{state.selection_reason}
        推荐股票代码：{', '.join(state.stock_codes) if state.stock_codes else '无'}
        """
        result_type = "selection"
    else:  # 诊股
        context_info = f"""
        股票分析结果：{json.dumps(state.stock_analysis, ensure_ascii=False, indent=2)}
        """
        result_type = "diagnosis"
    
    # 渲染用户提示词
    up_tpl = Template(up)
    user_prompt_content = up_tpl.render({
        "intent": state.intent,
        "context_info": context_info
    })
    
    # 初始化LLM客户端
    client = LLMClient(ctx=ctx)
    
    # 构建消息
    messages = [
        SystemMessage(content=sp),
        HumanMessage(content=user_prompt_content)
    ]
    
    # 调用大模型
    response = client.invoke(
        messages=messages,
        model=llm_config.get("model", "doubao-seed-1-8-251228"),
        temperature=llm_config.get("temperature", 0.3),
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
    
    # 准备邮件主题
    if state.intent == "选股":
        email_subject = "智能选股推荐报告"
    else:
        email_subject = "股票诊断分析报告"
    
    # 邮件内容和飞书内容都使用格式化结果
    email_content = result_text
    feishu_content = result_text
    
    return ResultFormatOutput(
        formatted_result=result_text,
        result_type=result_type,
        email_subject=email_subject,
        email_content=email_content,
        feishu_content=feishu_content
    )
