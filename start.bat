@echo off
REM 智能股票分析系统 - Windows快速启动脚本

echo 🚀 智能股票分析系统 - 快速启动
echo ==================================

REM 检查Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python未安装，请先安装Python 3.9+
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo ✅ Python版本: %PYTHON_VERSION%

REM 检查虚拟环境
if not exist "venv\" (
    echo 📦 创建虚拟环境...
    python -m venv venv
)

REM 激活虚拟环境
echo 🔧 激活虚拟环境...
call venv\Scripts\activate.bat

REM 升级pip
echo ⬆️ 升级pip...
python -m pip install --upgrade pip -q

REM 安装依赖
echo 📥 安装依赖...
pip install -r requirements.txt -q

if %errorlevel% neq 0 (
    echo ❌ 依赖安装失败
    exit /b 1
)

echo ✅ 依赖安装成功

REM 检查配置文件
if not exist "config\intent_recognition_llm_cfg.json" (
    echo ⚠️ 警告: 配置文件不存在，请确保config目录下有正确的配置文件
)

REM 设置环境变量
set FLASK_APP=api/server.py
set FLASK_ENV=development

REM 启动服务
echo.
echo 🎉 启动服务...
echo 📱 访问地址: http://localhost:5000
echo 🛑 按 Ctrl+C 停止服务
echo.

python api/server.py
