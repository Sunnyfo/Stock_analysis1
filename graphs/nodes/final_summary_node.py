"""
最终汇总节点 - 整合所有发送节点的结果
"""
from typing import Optional
from pydantic import BaseModel, Field
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context


class FinalSummaryInput(BaseModel):
    """最终汇总节点输入"""
    email_send_result: str = Field(default="", description="邮件发送结果")
    feishu_send_result: str = Field(default="", description="飞书发送结果")


class FinalSummaryOutput(BaseModel):
    """最终汇总节点输出"""
    result: str = Field(..., description="最终结果摘要")


def final_summary_node(state: FinalSummaryInput, config: RunnableConfig, runtime: Runtime[Context]) -> FinalSummaryOutput:
    """
    title: 最终汇总
    desc: 整合所有发送节点的结果，生成最终输出
    integrations:
    """
    ctx = runtime.context
    
    # 整合所有发送结果
    results = []
    if state.email_send_result:
        results.append(f"邮件：{state.email_send_result}")
    if state.feishu_send_result:
        results.append(f"飞书：{state.feishu_send_result}")
    
    final_result = " | ".join(results) if results else "股票分析完成"
    
    return FinalSummaryOutput(result=final_result)
