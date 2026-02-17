"""
飞书消息发送节点 - 将分析结果发送到飞书群聊
"""
import os
import json
import requests
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from coze_workload_identity import Client
from graphs.state import FeishuSendInput, FeishuSendOutput


def get_webhook_url():
    """获取飞书webhook URL"""
    client = Client()
    feishu_credential = client.get_integration_credential("integration-feishu-message")
    webhook_key = json.loads(feishu_credential)["webhook_url"]
    return webhook_key


def feishu_send_node(state: FeishuSendInput, config: RunnableConfig, runtime: Runtime[Context]) -> FeishuSendOutput:
    """
    title: 发送飞书消息
    desc: 将股票分析结果通过飞书机器人发送到群聊
    integrations: 飞书消息集成
    """
    ctx = runtime.context
    
    try:
        webhook_url = get_webhook_url()
        
        # 根据消息类型构建payload
        if state.message_type == "text":
            # 纯文本消息
            payload = {
                "msg_type": "text",
                "content": {"text": state.feishu_content}
            }
        elif state.message_type == "post":
            # 富文本消息
            # 将内容转换为适合的格式
            lines = state.feishu_content.split('\n')
            content_blocks = []
            
            for line in lines:
                if line.strip():
                    content_blocks.append([{"tag": "text", "text": line}])
            
            payload = {
                "msg_type": "post",
                "content": {
                    "post": {
                        "zh_cn": {
                            "title": "股票分析报告",
                            "content": content_blocks
                        }
                    }
                }
            }
        else:  # interactive
            # 交互式卡片
            elements = [{
                "tag": "div",
                "text": {
                    "tag": "plain_text",
                    "content": state.feishu_content
                }
            }]
            
            payload = {
                "msg_type": "interactive",
                "card": {
                    "header": {
                        "title": {
                            "tag": "plain_text",
                            "content": "股票分析报告"
                        }
                    },
                    "elements": elements
                }
            }
        
        # 发送消息
        response = requests.post(webhook_url, json=payload, timeout=10)
        result = response.json()
        
        if response.status_code == 200 and result.get("code") == 0:
            return FeishuSendOutput(
                status="success",
                message="飞书消息发送成功",
                feishu_send_result="飞书消息发送成功"
            )
        else:
            return FeishuSendOutput(
                status="failed",
                message=f"飞书消息发送失败: {result.get('msg', '未知错误')}",
                feishu_send_result=f"飞书消息发送失败：{result.get('msg', '未知错误')}"
            )
            
    except Exception as e:
        return FeishuSendOutput(
            status="failed",
            message=f"飞书消息发送异常: {str(e)}",
            feishu_send_result=f"飞书消息发送失败：{str(e)}"
        )
