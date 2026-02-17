# 🚀 快速运行指南

恭喜你已将代码上传到GitHub！现在按照以下步骤运行项目。

---

## 📌 方式一：本地运行（推荐新手）

### Windows用户

1. **下载代码**
   - 访问你的GitHub仓库
   - 点击绿色的 "Code" 按钮
   - 选择 "Download ZIP"
   - 解压到任意文件夹

2. **运行启动脚本**
   - 进入解压后的文件夹
   - 双击 `start.bat` 文件
   - 等待自动安装依赖和启动服务

3. **访问应用**
   - 打开浏览器
   - 访问：http://localhost:5000

---

### Mac/Linux用户

1. **下载代码**
   ```bash
   # 克隆代码
   git clone https://github.com/你的用户名/你的仓库名.git
   cd 你的仓库名
   ```

2. **运行启动脚本**
   ```bash
   chmod +x start.sh
   ./start.sh
   ```

3. **访问应用**
   - 打开浏览器
   - 访问：http://localhost:5000

---

## 📌 方式二：在线部署（Heroku）

### 前置准备

1. **注册Heroku账号**
   - 访问：https://signup.heroku.com/
   - 免费注册（需要信用卡验证，但不会收费）

2. **安装Heroku CLI**
   - Windows: 下载 https://devcenter.heroku.com/articles/heroku-cli
   - Mac: `brew tap heroku/brew && brew install heroku`
   - Linux: 按照 https://devcenter.heroku.com/articles/heroku-cli 安装

### 部署步骤

1. **登录Heroku**
   ```bash
   heroku login
   # 浏览器会弹出登录页面
   ```

2. **创建应用**
   ```bash
   heroku create 你的应用名称
   # 例如：heroku create my-stock-app
   ```

3. **部署到Heroku**
   ```bash
   git push heroku main
   # 如果你的分支是master，改成 git push heroku master
   ```

4. **访问应用**
   ```bash
   heroku open
   # 或访问 https://你的应用名称.herokuapp.com
   ```

### 设置自动部署（可选）

1. **进入你的GitHub仓库**
2. **点击 "Settings" → "Secrets and variables" → "Actions"**
3. **添加以下Secrets**：
   - `HEROKU_API_KEY`: 你的API Key（在Heroku Account Settings中找到）
   - `HEROKU_APP_NAME`: 你的应用名称
   - `HEROKU_EMAIL`: 你的注册邮箱

4. **推送代码自动部署**
   - 每次推送代码到main分支都会自动部署

---

## 📌 方式三：Docker运行

### 1. 安装Docker
   - Windows/Mac: 下载 Docker Desktop
   - Linux: `sudo apt install docker.io docker-compose`

### 2. 运行应用
   ```bash
   docker-compose up -d
   ```

### 3. 访问应用
   - 打开浏览器
   - 访问：http://localhost:5000

### 4. 查看日志
   ```bash
   docker-compose logs -f
   ```

### 5. 停止应用
   ```bash
   docker-compose down
   ```

---

## ❓ 常见问题

### Q1: 运行start.bat显示"python不是内部或外部命令"
**解决方案**：
1. 下载并安装Python 3.9+：https://www.python.org/downloads/
2. 安装时勾选 "Add Python to PATH"
3. 重新运行start.bat

### Q2: pip安装依赖很慢或失败
**解决方案**：
```bash
# 使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### Q3: 访问localhost:5000显示"无法连接"
**解决方案**：
1. 检查服务是否启动
2. 查看命令行是否有错误信息
3. 尝试重启服务（Ctrl+C停止后重新运行）
4. 检查端口5000是否被占用

### Q4: Heroku部署失败
**解决方案**：
```bash
# 查看部署日志
heroku logs --tail

# 常见原因：
# 1. requirements.txt依赖不正确
# 2. Python版本不支持
# 3. 环境变量未设置
```

### Q5: 邮件或飞书发送失败
**解决方案**：
- 确保在Coze平台正确配置了集成
- 检查邮箱授权码是否正确
- 确认飞书Webhook URL有效

---

## 📋 运行前检查清单

### 本地运行
- [ ] 已安装Python 3.9+
- [ ] 已下载项目代码
- [ ] 已运行start.bat或start.sh
- [ ] 浏览器可以访问 http://localhost:5000

### Heroku部署
- [ ] 已注册Heroku账号
- [ ] 已安装Heroku CLI
- [ ] 已登录Heroku
- [ ] 已创建Heroku应用
- [ ] 已执行 git push heroku main
- [ ] 可以通过heroku open访问应用

### Docker运行
- [ ] 已安装Docker
- [ ] 已运行 docker-compose up -d
- [ ] 浏览器可以访问 http://localhost:5000

---

## 🎯 推荐运行方式

### 如果你是新手
👉 **使用方式一（本地运行）**：最简单，双击start.bat即可

### 如果想在线访问
👉 **使用方式二（Heroku部署）**：可以随时随地访问

### 如果熟悉Docker
👉 **使用方式三（Docker运行）**：环境隔离，便于管理

---

## 📞 需要帮助？

1. **查看详细文档**：
   - 部署指南：`DEPLOYMENT.md`
   - 使用说明：`assets/README_UI.md`
   - 项目结构：`PROJECT_STRUCTURE.md`

2. **检查日志**：
   - 本地运行：查看命令行输出
   - Heroku：运行 `heroku logs --tail`
   - Docker：运行 `docker-compose logs -f`

3. **检查配置**：
   - 确保 `config/` 目录下有配置文件
   - 检查环境变量是否正确设置

---

## 🎉 开始使用

选择一种方式运行后：

1. **访问应用**
   - 本地：http://localhost:5000
   - Heroku：https://你的应用名.herokuapp.com

2. **测试诊股功能**
   - 输入：贵州茅台 或 600519
   - 点击"开始诊断"

3. **测试选股功能**
   - 选择行业、市值等条件
   - 点击"开始选股"

4. **配置邮箱（可选）**
   - 进入"设置"面板
   - 添加默认邮箱

---

**祝你运行顺利！** 🚀📈
