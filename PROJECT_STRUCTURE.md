# 项目结构说明

```
stock-analysis-system/
│
├── 📁 api/                           # API服务器目录
│   └── server.py                     # Flask应用主入口
│
├── 📁 assets/                        # 前端资源目录
│   ├── 📁 css/                       # CSS样式文件
│   │   └── style.css                 # 主样式文件
│   │
│   ├── 📁 js/                        # JavaScript文件
│   │   └── app.js                    # 前端交互逻辑
│   │
│   ├── index.html                    # 主页面HTML
│   └── README_UI.md                  # UI使用说明
│
├── 📁 config/                        # 配置文件目录
│   ├── intent_recognition_llm_cfg.json    # 意图识别模型配置
│   ├── stock_analysis_llm_cfg.json        # 股票分析模型配置
│   └── result_format_llm_cfg.json        # 结果格式化模型配置
│
├── 📁 src/                           # 源代码目录
│   │
│   ├── 📁 graphs/                    # 工作流定义
│   │   ├── graph.py                  # 主图编排
│   │   ├── state.py                  # 状态定义
│   │   ├── nodes/                    # 节点实现
│   │   │   ├── __init__.py
│   │   │   ├── intent_recognition_node.py    # 意图识别节点
│   │   │   ├── stock_selection_node.py        # 选股节点
│   │   │   ├── stock_diagnosis_node.py        # 诊股节点
│   │   │   ├── result_format_node.py          # 结果格式化节点
│   │   │   ├── email_send_node.py             # 邮件发送节点
│   │   │   ├── feishu_send_node.py            # 飞书发送节点
│   │   │   └── final_summary_node.py          # 最终汇总节点
│   │   └── loop_graph.py             # 子图（如有）
│   │
│   ├── 📁 agents/                    # Agent代码（预留）
│   │   └── __init__.py
│   │
│   ├── 📁 tools/                     # 工具函数
│   │   └── __init__.py
│   │
│   ├── 📁 storage/                   # 存储相关
│   │   ├── database/                 # 数据库
│   │   │   ├── __init__.py
│   │   │   ├── db.py
│   │   │   └── shared/
│   │   │       ├── __init__.py
│   │   │       └── model.py
│   │   ├── memory/                   # 内存存储
│   │   │   ├── __init__.py
│   │   │   └── memory_saver.py
│   │   └── s3/                       # S3存储
│   │       ├── __init__.py
│   │       └── s3_storage.py
│   │
│   ├── 📁 utils/                     # 工具类
│   │   ├── __init__.py
│   │   └── file/
│   │       ├── __init__.py
│   │       └── file.py               # 文件操作工具
│   │
│   ├── __init__.py
│   └── main.py                       # 主入口（CLI运行）
│
├── 📁 .github/                       # GitHub配置
│   └── 📁 workflows/
│       └── deploy-heroku.yml         # GitHub Actions工作流
│
├── 📁 scripts/                       # 脚本文件
│   └── load_env.py                   # 环境加载脚本
│
├── 📄 .coze                          # Coze配置
├── 📄 .dockerignore                  # Docker忽略文件
├── 📄 .gitignore                     # Git忽略文件
├── 📄 Dockerfile                     # Docker配置
├── 📄 LICENSE                        # MIT许可证
├── 📄 Procfile                       # Heroku配置
├── 📄 README.md                      # 项目说明
├── 📄 README_GITHUB.md               # GitHub README
├── 📄 DEPLOYMENT.md                  # 部署指南
├── 📄 requirements.txt               # Python依赖
├── 📄 runtime.txt                    # Python版本配置
├── 📄 start.sh                       # Linux/Mac启动脚本
├── 📄 start.bat                      # Windows启动脚本
└── 📄 docker-compose.yml             # Docker Compose配置

```

## 核心模块说明

### API服务器 (`api/server.py`)
- 提供RESTful API接口
- 处理前端请求
- 调用工作流引擎
- 返回分析结果

### 工作流引擎 (`src/graphs/`)
- **graph.py**: 定义主工作流结构
- **state.py**: 定义全局状态和节点输入输出
- **nodes/**: 各个业务节点的实现

### 前端界面 (`assets/`)
- **index.html**: 主页面结构
- **style.css**: 页面样式
- **app.js**: 交互逻辑和API调用

### 配置文件 (`config/`)
- LLM模型配置
- 提示词模板
- 参数设置

## 数据流

```
用户操作（Web界面）
    ↓
API请求（/api/analyze）
    ↓
意图识别节点
    ↓
[选股/诊股分支]
    ↓
结果格式化节点
    ↓
[邮件发送节点 + 飞书发送节点（并行）]
    ↓
最终汇总节点
    ↓
返回结果给前端
```

## 扩展说明

### 添加新节点
1. 在 `src/graphs/nodes/` 创建新节点文件
2. 在 `src/graphs/state.py` 定义输入输出状态
3. 在 `src/graphs/graph.py` 添加到工作流
4. 更新 `AGENTS.md`

### 添加新API接口
1. 在 `api/server.py` 添加路由
2. 实现业务逻辑
3. 返回JSON响应
4. 更新文档

### 集成新服务
1. 加载相关技能
2. 创建配置文件
3. 在节点中调用
4. 更新依赖
