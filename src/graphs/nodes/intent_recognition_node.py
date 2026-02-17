"""
意图识别节点 - 判断用户是要选股还是诊股
"""
import os
import json
from jinja2 import Template
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from coze_coding_dev_sdk import LLMClient
from graphs.state import IntentRecognitionInput, IntentRecognitionOutput


def intent_recognition_node(state: IntentRecognitionInput, config: RunnableConfig, runtime: Runtime[Context]) -> IntentRecognitionOutput:
    """
    title: 意图识别
    desc: 识别用户输入的意图是选股还是诊股
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
    
    # 渲染用户提示词
    up_tpl = Template(up)
    user_prompt_content = up_tpl.render({"user_input": state.user_input})
    
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
        max_completion_tokens=llm_config.get("max_completion_tokens", 500)
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
    
    # 提取意图和置信度
    intent = "诊股"  # 默认值
    confidence = 0.5  # 默认置信度
    
    # 尝试从结果中提取JSON
    try:
        if "选股" in result_text or "selection" in result_text.lower():
            intent = "选股"
            confidence = 0.9
        elif "诊股" in result_text or "diagnosis" in result_text.lower():
            intent = "诊股"
            confidence = 0.9
        else:
            # 默认根据关键词判断
            if any(keyword in state.user_input for keyword in ["选", "推荐", "筛选", "条件", "行业", "市值", "市盈率"]):
                intent = "选股"
                confidence = 0.7
            else:
                intent = "诊股"
                confidence = 0.7
    except Exception:
        # 解析失败，使用关键词判断
        if any(keyword in state.user_input for keyword in ["选", "推荐", "筛选", "条件"]):
            intent = "选股"
            confidence = 0.6
        else:
            intent = "诊股"
            confidence = 0.6
    
    return IntentRecognitionOutput(intent=intent, confidence=confidence)
