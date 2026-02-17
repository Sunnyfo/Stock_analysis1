FROM python:3.12-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件
COPY . .

# 暴露端口
EXPOSE 5000

# 设置环境变量
ENV FLASK_APP=api/server.py
ENV FLASK_ENV=production
ENV PYTHONPATH=/app

# 启动命令
CMD ["gunicorn", "api.server:app", "--bind", "0.0.0.0:5000", "--workers", "3", "--timeout", "120"]
