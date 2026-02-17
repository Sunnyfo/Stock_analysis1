"""
股票分析工作流主图编排
实现选股、诊股、邮件和飞书发送的完整流程
"""
from langgraph.graph import StateGraph, END
from graphs.state import (
    GlobalState,
    GraphInput,
    GraphOutput
)
from graphs.nodes.intent_recognition_node import intent_recognition_node
from graphs.nodes.stock_selection_node import stock_selection_node
from graphs.nodes.stock_diagnosis_node import stock_diagnosis_node
from graphs.nodes.email_send_node import email_send_node
from graphs.nodes.feishu_send_node import feishu_send_node
from graphs.nodes.result_format_node import result_format_node
from graphs.nodes.final_summary_node import final_summary_node


# 条件判断函数：根据意图决定流程
def route_by_intent(state: GlobalState) -> str:
    """
    title: 意图路由
    desc: 根据识别出的意图（选股/诊股）路由到不同的处理节点
    """
    if state.intent == "选股":
        return "选股"
    else:
        return "诊股"


# 创建状态图
builder = StateGraph(GlobalState, input_schema=GraphInput, output_schema=GraphOutput)

# 添加节点
# 1. 意图识别节点
builder.add_node(
    "intent_recognition",
    intent_recognition_node,
    metadata={"type": "agent", "llm_cfg": "config/intent_recognition_llm_cfg.json"}
)

# 2. 选股节点
builder.add_node(
    "stock_selection",
    stock_selection_node,
    metadata={"type": "agent", "llm_cfg": "config/stock_analysis_llm_cfg.json"}
)

# 3. 诊股节点
builder.add_node(
    "stock_diagnosis",
    stock_diagnosis_node,
    metadata={"type": "agent", "llm_cfg": "config/stock_analysis_llm_cfg.json"}
)

# 4. 结果汇总节点
builder.add_node(
    "result_format",
    result_format_node,
    metadata={"type": "agent", "llm_cfg": "config/result_format_llm_cfg.json"}
)

# 5. 邮件发送节点
builder.add_node(
    "email_send",
    email_send_node,
    metadata={"type": "task"}
)

# 6. 飞书发送节点
builder.add_node(
    "feishu_send",
    feishu_send_node,
    metadata={"type": "task"}
)

# 7. 最终汇总节点
builder.add_node(
    "final_summary",
    final_summary_node,
    metadata={"type": "task"}
)

# 设置入口点
builder.set_entry_point("intent_recognition")

# 添加条件分支：根据意图路由
builder.add_conditional_edges(
    source="intent_recognition",
    path=route_by_intent,
    path_map={
        "选股": "stock_selection",
        "诊股": "stock_diagnosis"
    }
)

# 添加边：选股和诊股都汇聚到结果汇总
builder.add_edge("stock_selection", "result_format")
builder.add_edge("stock_diagnosis", "result_format")

# 添加边：结果汇总后并行发送到邮件和飞书
builder.add_edge("result_format", "email_send")
builder.add_edge("result_format", "feishu_send")

# 添加边：两个发送节点都结束后才执行最终汇总
builder.add_edge(["email_send", "feishu_send"], "final_summary")

# 添加结束边
builder.add_edge("final_summary", END)

# 编译图
main_graph = builder.compile()
