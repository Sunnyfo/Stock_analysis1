# 🌐 GitHub在线运行完整指南

由于这个项目需要Python后端，有几种在GitHub上运行的方式：

---

## 🎯 方式一：GitHub Codespaces（推荐）⭐⭐⭐

GitHub Codespaces是GitHub提供的云端开发环境，可以直接在浏览器中运行代码，无需本地配置。

### 优点
- ✅ 完全在线运行，无需安装任何软件
- ✅ 自动配置Python环境
- ✅ 免费使用（每月60小时）
- ✅ 可以随时随地访问

### 详细步骤

#### 1. 打开GitHub仓库
```
访问你的GitHub仓库地址
```

#### 2. 创建Codespace
```
点击绿色 "Code" 按钮
↓
选择 "Codespaces" 标签
↓
点击 "Create codespace on main"
↓
等待环境创建（约1-2分钟）
```

#### 3. 安装依赖
创建完成后，在终端中运行：

```bash
# 确认Python版本
python --version

# 安装依赖
pip install -r requirements.txt

# 安装gunicorn
pip install gunicorn
```

#### 4. 启动服务

```bash
# 启动Flask服务
python api/server.py
```

#### 5. 访问应用

GitHub Codespaces会自动转发端口：
- 在终端找到类似这样的信息：`Running on http://0.0.0.0:5000`
- 查看Codespaces窗口顶部的 "PORTS" 标签
- 找到端口5000，点击右侧的 "打开浏览器" 图标 🌐
- 或点击显示的URL（通常是 `https://xxxx-5000.app.github.dev`）

#### 6. 停止服务

- 在终端按 `Ctrl+C` 停止服务
- 或直接关闭Codespace（下次会自动保存）

---

## 🎯 方式二：GitHub Actions自动部署到Heroku ⭐⭐

这种方式会将你的GitHub代码自动部署到Heroku，部署后可以通过公网URL访问。

### 前置准备

#### 1. 注册Heroku账号
```
访问：https://signup.heroku.com/
注册免费账号（需要信用卡验证）
```

#### 2. 获取Heroku API Key
```
1. 登录 https://dashboard.heroku.com/
2. 点击右上角头像 → "Account settings"
3. 滚动到 "API Key" 部分
4. 点击 "Reveal" 显示API Key
5. 复制保存这个Key
```

### 配置GitHub仓库

#### 1. 添加Secrets
```
1. 进入你的GitHub仓库
2. 点击 "Settings" → "Secrets and variables" → "Actions"
3. 点击 "New repository secret"
4. 添加以下Secrets：

   Name: HEROKU_API_KEY
   Value: 你复制的API Key

   Name: HEROKU_APP_NAME
   Value: 你的Heroku应用名称（如：my-stock-app）

   Name: HEROKU_EMAIL
   Value: 你的Heroku注册邮箱
```

#### 2. 创建Heroku应用
在Heroku Dashboard中：
```
1. 点击 "Create new app"
2. 输入应用名称（如：my-stock-app）
3. 选择地区（推荐选择离你近的）
4. 点击 "Create app"
```

#### 3. 连接GitHub仓库
```
1. 在Heroku应用页面
2. 点击 "Deploy" 标签
3. 在 "Deployment method" 中选择 "GitHub"
4. 搜索并连接你的GitHub仓库
5. 选择分支（通常是 main）
6. 启用 "Automatic deploys"
```

### 自动部署

现在每次你推送代码到GitHub的main分支，都会自动部署到Heroku！

```bash
git add .
git commit -m "更新代码"
git push origin main

# 等待2-3分钟，自动部署完成
```

### 访问应用

```
方式1：在Heroku应用页面点击 "Open app"
方式2：直接访问 https://你的应用名.herokuapp.com
```

---

## 🎯 方式三：直接在本地克隆GitHub仓库运行

如果你想在本地运行但代码在GitHub上：

### Windows用户

```batch
1. 安装Git：https://git-scm.com/download/win
2. 打开Git Bash或PowerShell
3. 克隆代码：
   git clone https://github.com/你的用户名/你的仓库名.git
   cd 你的仓库名
4. 运行：
   start.bat
```

### Mac/Linux用户

```bash
# 克隆代码
git clone https://github.com/你的用户名/你的仓库名.git
cd 你的仓庛名

# 运行
chmod +x start.sh
./start.sh
```

---

## 📊 三种方式对比

| 方式 | 优点 | 缺点 | 推荐指数 |
|------|------|------|----------|
| **GitHub Codespaces** | 完全在线，无需配置 | 每月60小时限制 | ⭐⭐⭐ |
| **Actions+Heroku** | 自动部署，永久访问 | 需要信用卡验证 | ⭐⭐⭐ |
| **本地克隆** | 完全免费，无限制 | 需要本地配置Python | ⭐⭐ |

---

## 🚀 推荐方案

### 场景1：只想快速测试（5分钟）
👉 **GitHub Codespaces**
- 无需任何配置
- 直接在浏览器中运行
- 点击按钮即可访问

### 场景2：长期使用和分享
👉 **GitHub Actions + Heroku**
- 自动部署
- 永久在线
- 随时随地访问

### 场景3：完全免费且无限制
👉 **本地克隆运行**
- 完全免费
- 无时长限制
- 需要本地配置

---

## 💡 GitHub Codespaces详细教程

### 第1步：打开仓库并创建Codespace

```
1. 访问你的GitHub仓库
2. 点击绿色的 "Code" 按钮
3. 在弹出的窗口中，找到 "Codespaces" 标签
4. 点击 "+" 号创建新的Codespace
5. 选择配置（默认即可）
6. 点击 "Create codespace"
```

### 第2步：等待环境创建

```
⏳ 等待1-2分钟，看到以下界面说明成功：
- 终端已打开
- 显示 Welcome to GitHub Codespaces
- 可以看到项目文件
```

### 第3步：在终端中运行

```bash
# 在终端中依次输入以下命令：

# 1. 确认Python版本
python --version
# 应该显示：Python 3.9+

# 2. 安装依赖
pip install -r requirements.txt
# 等待安装完成（约1-2分钟）

# 3. 启动服务
python api/server.py
# 看到 "Running on http://0.0.0.0:5000" 表示成功
```

### 第4步：访问应用

```
1. 在Codespaces窗口顶部，找到 "PORTS" 标签
2. 看到端口5000的转发信息
3. 点击右侧的 "打开浏览器" 图标 🌐
4. 或点击显示的URL（如 https://xxxx-5000.app.github.dev）
5. 浏览器会自动打开应用界面
```

### 第5步：使用应用

```
✅ 测试诊股：
- 输入：贵州茅台
- 点击"开始诊断"

✅ 测试选股：
- 选择行业：科技
- 点击"开始选股"
```

### 第6步：停止和重启

```
停止：
- 在终端按 Ctrl+C

重启：
- 重新运行 python api/server.py

关闭Codespace：
- 关闭浏览器标签页
- 下次打开会自动保存状态
```

---

## 🔧 GitHub Actions详细教程

### 第1步：配置GitHub Secrets

```
1. 进入GitHub仓库
2. 点击 "Settings" 标签
3. 左侧菜单找到 "Secrets and variables"
4. 点击 "Actions"
5. 点击 "New repository secret"

添加3个Secret：
- HEROKU_API_KEY: 你的Heroku API Key
- HEROKU_APP_NAME: 你的应用名称
- HEROKU_EMAIL: 你的邮箱
```

### 第2步：创建Heroku应用

```
1. 登录 https://dashboard.heroku.com/
2. 点击 "Create new app"
3. 输入应用名称（如：my-stock-analysis）
4. 选择地区（推荐 US）
5. 点击 "Create app"
```

### 第3步：连接GitHub仓库

```
1. 在Heroku应用页面，点击 "Deploy" 标签
2. 在 "Deployment method" 部分，点击 "GitHub"
3. 搜索并连接你的GitHub仓库
4. 选择 "main" 分支
5. 点击 "Enable Automatic Deploys"
```

### 第4步：推送代码触发自动部署

```bash
# 在你的本地电脑，推送代码到GitHub
git add .
git commit -m "部署到Heroku"
git push origin main

# 或者直接在GitHub网页上编辑文件后提交
```

### 第5步：查看部署状态

```
1. 在GitHub仓库，点击 "Actions" 标签
2. 看到部署工作流正在运行
3. 等待2-3分钟，显示绿色 ✅ 表示成功
4. 点击可以查看详细日志
```

### 第6步：访问应用

```
方式1：Heroku Dashboard
- 进入你的Heroku应用
- 点击右上角 "Open app"

方式2：直接访问
- https://my-stock-analysis.herokuapp.com
- （替换成你的应用名称）
```

---

## 🆘 常见问题

### Q1: GitHub Codespaces显示端口无法访问
**A**: 
1. 确保服务正在运行
2. 检查 "PORTS" 标签
3. 点击 "刷新" 图标
4. 或手动访问显示的URL

### Q2: GitHub Actions部署失败
**A**:
```bash
# 查看部署日志
在GitHub仓库 → Actions → 点击失败的workflow

# 常见错误：
- HEROKU_API_KEY错误 → 检查Secret配置
- requirements.txt错误 → 检查依赖文件
- 权限错误 → 检查GitHub仓库设置
```

### Q3: Heroku应用无法访问
**A**:
```bash
# 检查应用状态
heroku ps --app 你的应用名

# 查看日志
heroku logs --tail --app 你的应用名

# 重启应用
heroku restart --app 你的应用名
```

---

## 📝 推荐操作流程

### 第一次使用（推荐Codespaces）

```
1. 打开GitHub仓库
2. 创建Codespace
3. 在终端运行：pip install -r requirements.txt
4. 运行：python api/server.py
5. 点击顶部的端口5000打开浏览器
6. 开始使用！
```

### 长期使用（推荐Heroku自动部署）

```
1. 配置GitHub Secrets（一次性）
2. 创建Heroku应用（一次性）
3. 连接GitHub仓库（一次性）
4. 每次推送代码自动部署
5. 通过https://xxx.herokuapp.com访问
```

---

## 🎉 总结

### 最快的方式（3分钟）
👉 **GitHub Codespaces**
- 无需任何配置
- 完全在线运行
- 点击即可访问

### 最稳定的方式（推荐）
👉 **GitHub Actions + Heroku**
- 自动部署
- 永久在线
- 随时随地访问

### 最省钱的方式
👉 **本地运行**
- 完全免费
- 无任何限制
- 需要本地配置

---

## 📞 需要帮助？

- GitHub Codespaces文档：https://docs.github.com/codespaces
- GitHub Actions文档：https://docs.github.com/actions
- Heroku文档：https://devcenter.heroku.com/

---

**现在就试试吧！** 🚀
