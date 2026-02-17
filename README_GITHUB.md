# 📈 智能股票分析系统

一个基于AI的智能股票分析平台，提供诊股、选股功能，并支持邮件和飞书消息通知。

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ 核心功能

- 🔍 **智能诊股** - 深度分析股票基本面和技术面
- 🎯 **智能选股** - 多维度筛选推荐优质股票
- 📧 **邮件通知** - 自动发送分析报告到邮箱
- 💬 **飞书集成** - 通过飞书机器人实时推送结果
- 🌐 **Web界面** - 美观易用的图形化操作界面
- 🔎 **股票搜索** - 支持代码、名称、首字母缩写搜索

## 🚀 快速开始

### 在线体验

访问已部署的网站：[点击这里](https://your-app.herokuapp.com)

### 本地运行

```bash
# 克隆项目
git clone https://github.com/your-username/stock-analysis.git
cd stock-analysis

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 启动服务
python api/server.py
```

访问 http://localhost:5000

## 📖 使用说明

### 诊股分析
1. 在"诊股"面板输入股票名称、代码或首字母缩写
2. 选择发送渠道（飞书/邮件）
3. 点击"开始诊断"
4. 查看分析结果

### 智能选股
1. 在"选股"面板设置筛选条件：
   - 行业、市值、市盈率
   - K线周期（日线/周线/月线）
   - 技术指标（MACD、RSI等）
2. 点击"开始选股"
3. 获取推荐股票列表

### 系统设置
- 登记默认邮箱地址
- 配置飞书Webhook
- 选择消息格式

详细使用说明请参考 [assets/README_UI.md](assets/README_UI.md)

## 🛠️ 技术栈

### 后端
- **Flask** - Web框架
- **LangGraph** - 工作流编排
- **LangChain** - LLM集成
- **Coze SDK** - AI能力

### 前端
- **HTML5** - 页面结构
- **CSS3** - 样式设计
- **JavaScript** - 交互逻辑

### 集成
- **邮件** - IMAP/SMTP协议
- **飞书** - Webhook消息推送
- **网页搜索** - 实时信息获取

## 📦 部署

### Heroku部署（推荐）

```bash
# 安装Heroku CLI
# 创建应用并部署
heroku create your-app-name
git push heroku main
heroku open
```

详细部署指南请参考 [DEPLOYMENT.md](DEPLOYMENT.md)

### Docker部署

```bash
# 使用Docker Compose
docker-compose up -d

# 或使用Docker命令
docker build -t stock-analysis .
docker run -p 5000:5000 stock-analysis
```

## 🗂️ 项目结构

```
stock-analysis/
├── api/                  # API服务器
│   └── server.py        # Flask应用主文件
├── assets/              # 前端资源
│   ├── css/            # 样式文件
│   ├── js/             # JavaScript文件
│   └── index.html      # 主页面
├── config/             # 配置文件
│   ├── intent_recognition_llm_cfg.json
│   ├── stock_analysis_llm_cfg.json
│   └── result_format_llm_cfg.json
├── src/                # 源代码
│   ├── graphs/        # 工作流定义
│   └── tools/         # 工具函数
├── requirements.txt   # Python依赖
├── Dockerfile        # Docker配置
├── docker-compose.yml
├── Procfile          # Heroku配置
└── DEPLOYMENT.md     # 部署指南
```

## 🔧 配置

### 环境变量

| 变量名 | 说明 |
|--------|------|
| `COZE_WORKSPACE_PATH` | 工作空间路径 |
| `FLASK_ENV` | Flask环境（development/production） |
| `PORT` | 服务端口 |

### 集成配置

应用需要在Coze平台配置以下集成：
- 邮件集成 (`integration-email-imap-smtp`)
- 飞书消息集成 (`integration-feishu-message`)

## 📊 工作流架构

```
用户输入 → 意图识别 → [选股/诊股] → 结果汇总 → [邮件/飞书] → 最终结果
```

详细架构说明请参考 [AGENTS.md](AGENTS.md)

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 📞 联系方式

- 提交问题：[GitHub Issues](https://github.com/your-username/stock-analysis/issues)
- 邮箱：your-email@example.com

## 🙏 致谢

感谢以下开源项目：
- [Flask](https://flask.palletsprojects.com/)
- [LangGraph](https://github.com/langchain-ai/langgraph)
- [LangChain](https://github.com/langchain-ai/langchain)

---

**⚠️ 免责声明**：本系统仅供学习和参考使用，不构成投资建议。投资有风险，入市需谨慎。
