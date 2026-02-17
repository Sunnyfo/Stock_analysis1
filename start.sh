#!/bin/bash

# 智能股票分析系统 - 快速启动脚本

echo "🚀 智能股票分析系统 - 快速启动"
echo "=================================="

# 检查Python版本
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未安装，请先安装Python 3.9+"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | awk '{print $2}')
echo "✅ Python版本: $PYTHON_VERSION"

# 检查是否已存在虚拟环境
if [ ! -d "venv" ]; then
    echo "📦 创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
echo "🔧 激活虚拟环境..."
source venv/bin/activate

# 升级pip
echo "⬆️ 升级pip..."
pip install --upgrade pip -q

# 安装依赖
echo "📥 安装依赖..."
pip install -r requirements.txt -q

# 检查是否安装成功
if [ $? -eq 0 ]; then
    echo "✅ 依赖安装成功"
else
    echo "❌ 依赖安装失败"
    exit 1
fi

# 检查配置文件
if [ ! -f "config/intent_recognition_llm_cfg.json" ]; then
    echo "⚠️ 警告: 配置文件不存在，请确保config目录下有正确的配置文件"
fi

# 设置环境变量
export FLASK_APP=api/server.py
export FLASK_ENV=development

# 启动服务
echo ""
echo "🎉 启动服务..."
echo "📱 访问地址: http://localhost:5000"
echo "🛑 按 Ctrl+C 停止服务"
echo ""

python api/server.py
