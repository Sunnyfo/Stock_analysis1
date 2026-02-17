## 项目概述
- **名称**: 智能股票分析工作流
- **功能**: 提供智能选股、诊股功能，并支持将分析结果发送到邮件和飞书群聊
- **Web界面**: 提供图形化操作界面，支持股票搜索（代码/名称/首字母）、选股条件设置、邮箱登记等功能

### 节点清单
| 节点名 | 文件位置 | 类型 | 功能描述 | 分支逻辑 | 配置文件 |
|-------|---------|------|---------|---------|---------|
| intent_recognition | `nodes/intent_recognition_node.py` | agent | 意图识别 | "选股"→stock_selection, "诊股"→stock_diagnosis | `config/intent_recognition_llm_cfg.json` |
| stock_selection | `nodes/stock_selection_node.py` | agent | 智能选股 | - | `config/stock_analysis_llm_cfg.json` |
| stock_diagnosis | `nodes/stock_diagnosis_node.py` | agent | 智能诊股 | - | `config/stock_analysis_llm_cfg.json` |
| result_format | `nodes/result_format_node.py` | agent | 结果汇总 | - | `config/result_format_llm_cfg.json` |
| email_send | `nodes/email_send_node.py` | task | 发送邮件 | - | - |
| feishu_send | `nodes/feishu_send_node.py` | task | 发送飞书消息 | - | - |
| final_summary | `nodes/final_summary_node.py` | task | 最终汇总 | - | - |

**类型说明**: task(task节点) / agent(大模型) / condition(条件分支) / looparray(列表循环) / loopcond(条件循环)

## 子图清单
本工作流暂无子图

## API服务器
- **位置**: `api/server.py`
- **框架**: Flask
- **功能**: 提供REST API接口供Web界面调用
- **端口**: 5000（可通过PORT环境变量配置）
- **接口**:
  - `GET /` - 主页面
  - `GET /<path>` - 静态文件服务
  - `POST /api/analyze` - 股票分析API
  - `GET /api/stocks/search?q=xxx` - 股票搜索API
  - `GET /api/health` - 健康检查

## 技能使用
- 节点 `intent_recognition` 使用大语言模型技能
- 节点 `stock_selection` 使用大语言模型和网页搜索技能
- 节点 `stock_diagnosis` 使用大语言模型和网页搜索技能
- 节点 `result_format` 使用大语言模型技能
- 节点 `email_send` 使用邮件集成（IMAP/SMTP）
- 节点 `feishu_send` 使用飞书消息集成

## Web界面
- **位置**: `assets/index.html`
- **功能**:
  - 股票搜索：支持代码、名称、首字母缩写搜索
  - 智能诊股：快速诊断指定股票
  - 智能选股：设置多种筛选条件（行业、市值、PE、K线周期、技术指标等）
  - 邮箱管理：登记默认收件人
  - 系统设置：配置Webhook和消息格式
- **使用说明**: 详细文档见 `assets/README_UI.md`

## 工作流说明

### 核心功能
1. **智能意图识别**：自动识别用户是要选股还是诊股
2. **智能选股**：根据用户提供的条件（行业、市值、市盈率等）推荐符合要求的股票
3. **智能诊股**：深度分析指定股票的基本面、技术面和投资价值
4. **多渠道通知**：支持将分析结果发送到邮件和飞书群聊

### 工作流流程
```
用户输入
  ↓
意图识别（判断选股/诊股）
  ↓ (条件分支)
选股分支 → 选股分析
诊股分支 → 诊股分析
  ↓ (汇聚)
结果汇总（格式化报告）
  ↓ (并行发送)
邮件发送 → 邮件集成
飞书发送 → 飞书集成
  ↓ (汇聚)
最终汇总
  ↓
结束
```

### 使用方法
1. 输入用户消息（如："分析一下贵州茅台的投资价值" 或 "推荐一些科技股"）
2. 选择发送渠道（email/feishu/both）
3. 如选择邮件发送，提供收件人列表（可选）
4. 系统自动执行分析并发送结果

### 配置文件
- `config/intent_recognition_llm_cfg.json`: 意图识别模型配置
- `config/stock_analysis_llm_cfg.json`: 股票分析模型配置
- `config/result_format_llm_cfg.json`: 结果格式化模型配置

### 集成配置
- **邮件集成**：需要配置 `integration-email-imap-smtp`
- **飞书集成**：需要配置 `integration-feishu-message`

### 注意事项
1. 邮件和飞书发送为并行执行，提升效率
2. 如果未配置收件人，邮件发送将失败但不会影响飞书发送
3. 系统会自动将分析结果格式化为易读的格式
4. 支持通过飞书对话进行选股和诊股操作
