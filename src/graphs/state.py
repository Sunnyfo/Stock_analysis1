"""
股票分析工作流状态定义
包含全局状态、图输入输出、各节点输入输出
"""
from typing import Optional, List, Literal
from pydantic import BaseModel, Field


# ==================== 全局状态 ====================
class GlobalState(BaseModel):
    """全局状态定义，在整个工作流中共享"""
    user_input: str = Field(..., description="用户输入的文本消息")
    intent: str = Field(default="", description="识别出的用户意图：选股/诊股")
    stock_codes: List[str] = Field(default=[], description="选出的股票代码列表")
    stock_analysis: dict = Field(default={}, description="股票分析结果")
    formatted_result: str = Field(default="", description="格式化后的结果文本")
    send_channel: str = Field(default="feishu", description="发送渠道：email/feishu/both")
    email_recipients: List[str] = Field(default=[], description="邮件收件人列表")
    send_status: dict = Field(default={}, description="发送状态")
    email_subject: str = Field(default="股票分析报告", description="邮件主题")
    email_content: str = Field(default="", description="邮件内容")
    feishu_content: str = Field(default="", description="飞书消息内容")
    email_send_result: str = Field(default="", description="邮件发送结果")
    feishu_send_result: str = Field(default="", description="飞书发送结果")
    result: str = Field(default="", description="最终结果摘要")


# ==================== 图输入输出 ====================
class GraphInput(BaseModel):
    """工作流输入"""
    user_input: str = Field(..., description="用户输入的消息内容")
    send_channel: str = Field(default="feishu", description="发送渠道：email/feishu/both")
    email_recipients: List[str] = Field(default=[], description="邮件收件人列表（可选）")


class GraphOutput(BaseModel):
    """工作流输出"""
    result: str = Field(..., description="处理结果摘要")
    send_status: dict = Field(default={}, description="发送状态")


# ==================== 意图识别节点 ====================
class IntentRecognitionInput(BaseModel):
    """意图识别节点输入"""
    user_input: str = Field(..., description="用户输入的文本消息")


class IntentRecognitionOutput(BaseModel):
    """意图识别节点输出"""
    intent: str = Field(..., description="识别出的意图：选股/诊股")
    confidence: float = Field(default=0.0, description="识别置信度")


# ==================== 选股节点 ====================
class StockSelectionInput(BaseModel):
    """选股节点输入"""
    user_input: str = Field(..., description="用户输入的选股条件")


class StockSelectionOutput(BaseModel):
    """选股节点输出"""
    stock_codes: List[str] = Field(..., description="选出的股票代码列表")
    stock_names: List[str] = Field(default=[], description="股票名称列表")
    selection_reason: str = Field(default="", description="选股理由说明")


# ==================== 诊股节点 ====================
class StockDiagnosisInput(BaseModel):
    """诊股节点输入"""
    user_input: str = Field(..., description="用户输入的股票代码或名称")


class StockDiagnosisOutput(BaseModel):
    """诊股节点输出"""
    stock_analysis: dict = Field(..., description="股票分析结果，包含基本面、技术面等信息")
    stock_code: str = Field(default="", description="分析的股票代码")
    stock_name: str = Field(default="", description="分析的股票名称")


# ==================== 邮件发送节点 ====================
class EmailSendInput(BaseModel):
    """邮件发送节点输入"""
    email_subject: str = Field(default="股票分析报告", description="邮件主题")
    email_content: str = Field(default="", description="邮件内容")
    email_recipients: List[str] = Field(default=[], description="收件人列表")


class EmailSendOutput(BaseModel):
    """邮件发送节点输出"""
    status: str = Field(..., description="发送状态：success/failed")
    message: str = Field(default="", description="发送结果消息")
    recipient_count: int = Field(default=0, description="成功发送的收件人数")
    email_send_result: str = Field(default="", description="邮件发送结果")


# ==================== 飞书消息发送节点 ====================
class FeishuSendInput(BaseModel):
    """飞书消息发送节点输入"""
    feishu_content: str = Field(default="", description="消息内容")
    message_type: str = Field(default="post", description="消息类型：text/post/interactive")


class FeishuSendOutput(BaseModel):
    """飞书消息发送节点输出"""
    status: str = Field(..., description="发送状态：success/failed")
    message: str = Field(default="", description="发送结果消息")
    feishu_send_result: str = Field(default="", description="飞书发送结果")


# ==================== 结果汇总节点 ====================
class ResultFormatInput(BaseModel):
    """结果汇总节点输入"""
    intent: str = Field(..., description="用户意图：选股/诊股")
    stock_codes: List[str] = Field(default=[], description="股票代码列表")
    stock_analysis: dict = Field(default={}, description="股票分析结果")
    selection_reason: str = Field(default="", description="选股理由")


class ResultFormatOutput(BaseModel):
    """结果汇总节点输出"""
    formatted_result: str = Field(..., description="格式化后的结果文本")
    result_type: str = Field(default="", description="结果类型：selection/diagnosis")
    email_subject: str = Field(default="股票分析报告", description="邮件主题")
    email_content: str = Field(default="", description="邮件内容")
    feishu_content: str = Field(default="", description="飞书消息内容")
