# 智能股票分析系统 - 部署指南

本指南将帮助你将智能股票分析系统部署到不同的平台。

## 📦 部署方式总览

支持以下部署方式：

1. **本地开发** - 适合开发和测试
2. **Heroku部署** - 推荐用于生产环境
3. **Docker部署** - 适合容器化部署
4. **传统服务器部署** - 适合VPS或自有服务器

## 🚀 方式一：本地开发部署

### 前置要求
- Python 3.9+
- pip

### 部署步骤

1. **克隆项目**
```bash
git clone <your-repo-url>
cd stock-analysis-system
```

2. **创建虚拟环境**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows
```

3. **安装依赖**
```bash
pip install -r requirements.txt
pip install gunicorn
```

4. **配置环境变量**
```bash
export FLASK_APP=api/server.py
export FLASK_ENV=development
```

5. **启动服务**
```bash
python api/server.py
# 或使用gunicorn
gunicorn api.server:app --bind 0.0.0.0:5000
```

6. **访问应用**
打开浏览器访问：http://localhost:5000

---

## ☁️ 方式二：Heroku部署（推荐）

Heroku提供免费的云服务，非常适合部署Flask应用。

### 前置要求
- [Heroku账号](https://signup.heroku.com/)
- [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
- Git

### 部署步骤

1. **创建Heroku应用**
```bash
heroku login
heroku create your-app-name
```

2. **推送代码到GitHub**
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/your-username/your-repo.git
git push -u origin main
```

3. **连接Heroku和GitHub**
在Heroku Dashboard中：
- 进入你的应用
- 点击 "Deploy" 标签
- 在 "Deployment method" 中选择 "GitHub"
- 连接你的GitHub仓库

4. **配置环境变量**
在Heroku Dashboard中，添加以下环境变量：
```
COZE_WORKSPACE_PATH=/app
FLASK_ENV=production
```

5. **自动部署**
- 启用 "Automatic deploys"
- 选择 `main` 分支
- 每次推送代码将自动部署

或手动部署：
```bash
git push heroku main
```

6. **访问应用**
```bash
heroku open
# 或访问 https://your-app-name.herokuapp.com
```

### 使用GitHub Actions自动部署

项目已配置GitHub Actions，实现代码推送后自动部署到Heroku。

**配置步骤**：
1. 在GitHub仓库中设置Secrets：
   - `HEROKU_API_KEY`: 你的Heroku API Key
   - `HEROKU_APP_NAME`: 你的应用名称
   - `HEROKU_EMAIL`: 你的Heroku邮箱

2. 推送代码到main分支，自动部署将触发。

---

## 🐳 方式三：Docker部署

### 前置要求
- Docker
- Docker Compose（可选）

### 部署步骤

#### 方式A：使用Docker Compose（推荐）

1. **启动服务**
```bash
docker-compose up -d
```

2. **查看日志**
```bash
docker-compose logs -f
```

3. **停止服务**
```bash
docker-compose down
```

#### 方式B：使用Docker命令

1. **构建镜像**
```bash
docker build -t stock-analysis .
```

2. **运行容器**
```bash
docker run -d -p 5000:5000 --name stock-app stock-analysis
```

3. **查看日志**
```bash
docker logs -f stock-app
```

4. **停止容器**
```bash
docker stop stock-app
```

---

## 🖥️ 方式四：传统服务器部署

适用于VPS（如阿里云、腾讯云、AWS等）或自有服务器。

### 前置要求
- Linux服务器（Ubuntu/CentOS）
- Nginx
- Python 3.9+
- Supervisor（进程管理）

### 部署步骤

#### 1. 安装系统依赖
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv nginx supervisor git
```

#### 2. 克隆项目
```bash
cd /var/www
sudo git clone <your-repo-url> stock-analysis
cd stock-analysis
```

#### 3. 创建虚拟环境
```bash
sudo python3 -m venv venv
sudo venv/bin/pip install -r requirements.txt
sudo venv/bin/pip install gunicorn
```

#### 4. 配置Gunicorn
创建Systemd服务文件：
```bash
sudo nano /etc/systemd/system/stock-analysis.service
```

内容：
```ini
[Unit]
Description=Stock Analysis Flask App
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/stock-analysis
Environment="PATH=/var/www/stock-analysis/venv/bin"
ExecStart=/var/www/stock-analysis/venv/bin/gunicorn \
    api.server:app \
    --bind 0.0.0.0:5000 \
    --workers 3 \
    --timeout 120
Restart=always

[Install]
WantedBy=multi-user.target
```

启动服务：
```bash
sudo systemctl start stock-analysis
sudo systemctl enable stock-analysis
sudo systemctl status stock-analysis
```

#### 5. 配置Nginx
创建Nginx配置文件：
```bash
sudo nano /etc/nginx/sites-available/stock-analysis
```

内容：
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /var/www/stock-analysis/assets/css;
    }

    location /js {
        alias /var/www/stock-analysis/assets/js;
    }
}
```

启用配置：
```bash
sudo ln -s /etc/nginx/sites-available/stock-analysis /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 6. 配置HTTPS（可选）
使用Let's Encrypt：
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

---

## 🔧 环境变量配置

应用需要以下环境变量：

| 变量名 | 说明 | 默认值 | 必需 |
|--------|------|--------|------|
| `COZE_WORKSPACE_PATH` | 工作空间路径 | - | ✅ |
| `FLASK_ENV` | Flask环境 | production | - |
| `FLASK_DEBUG` | 调试模式 | False | - |
| `PORT` | 服务端口 | 5000 | - |

### 集成配置

应用依赖以下集成，需要在Coze平台配置：

1. **邮件集成** (`integration-email-imap-smtp`)
2. **飞书消息集成** (`integration-feishu-message`)

---

## 📊 监控和日志

### 查看应用日志

**Heroku**:
```bash
heroku logs --tail
```

**Docker**:
```bash
docker logs -f stock-app
```

**Systemd**:
```bash
sudo journalctl -u stock-analysis -f
```

### 性能监控

建议使用以下工具监控应用性能：
- Sentry - 错误追踪
- New Relic - 性能监控
- Prometheus + Grafana - 完整监控栈

---

## 🔐 安全建议

1. **使用HTTPS**：生产环境必须使用SSL证书
2. **环境变量**：敏感信息通过环境变量配置，不要提交到代码库
3. **限制访问**：配置防火墙，只开放必要端口
4. **定期更新**：及时更新系统和依赖包
5. **日志审计**：定期检查日志，发现异常

---

## 📈 扩展和优化

### 水平扩展

使用负载均衡器（如Nginx、HAProxy）分发流量到多个实例。

### 数据库集成

如需持久化数据，可以添加数据库：
```bash
pip install sqlalchemy psycopg2-binary  # PostgreSQL
# 或
pip install pymysql  # MySQL
```

### 缓存优化

添加Redis缓存提升性能：
```bash
pip install redis flask-caching
```

---

## 🆘 常见问题

### Q1: Heroku部署失败，显示"Could not find a version that satisfies the requirement"
**A**: 某些依赖可能需要指定版本，检查`requirements.txt`

### Q2: 访问网站显示502 Bad Gateway
**A**: 检查应用是否正常运行，查看日志排查错误

### Q3: 邮件发送失败
**A**: 确保在Coze平台正确配置了邮件集成凭证

### Q4: 飞书消息发送失败
**A**: 检查Webhook URL是否正确，机器人是否添加到群聊

### Q5: 应用启动慢
**A**: 考虑增加Gunicorn workers数量，或使用更强大的服务器

---

## 📞 技术支持

遇到问题？请：
1. 查看日志文件
2. 检查配置是否正确
3. 参考本文档的常见问题
4. 联系开发团队

---

**祝部署顺利！** 🚀
