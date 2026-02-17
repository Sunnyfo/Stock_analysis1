# 🎯 GitHub Codespaces 超详细教程

> 完全在线运行，无需安装任何软件！跟着这个教程，3分钟就能运行起来！

---

## 📋 准备工作（开始前必读）

### 你需要什么？
- ✅ 一个GitHub账号（如果没有，去 https://github.com 注册）
- ✅ 你的股票分析项目GitHub仓库
- ✅ 网络连接

### 不需要什么？
- ❌ 不需要安装Python
- ❌ 不需要安装任何开发工具
- ❌ 不需要配置环境

---

## 🚀 详细步骤（跟着操作就行）

---

## 第1步：打开GitHub仓库

### 操作说明

1. **登录GitHub**
   ```
   访问：https://github.com
   输入账号密码登录
   ```

2. **找到你的项目仓库**
   ```
   在页面顶部点击你的头像
   点击 "Your repositories"
   找到 "智能股票分析系统" 仓库
   点击仓库名称进入
   ```

3. **确认仓库内容**
   ```
   你应该能看到：
   - api/ 文件夹
   - assets/ 文件夹
   - config/ 文件夹
   - requirements.txt 文件
   - README.md 文件
   ```

✅ **确认成功后，进入下一步**

---

## 第2步：创建Codespace

### 详细操作

#### 步骤2.1：找到Code按钮

1. **在仓库页面**，找到绿色的 **"Code"** 按钮
   - 位置：页面右上方，文件列表上方
   - 颜色：绿色
   - 标识：带有代码图标 📝

#### 步骤2.2：点击Code按钮

1. **点击绿色 "Code" 按钮**
   - 会弹出一个下拉菜单
   - 菜单包含多个选项：
     - Clone
     - Open with Codespaces
     - Download ZIP
     - 等

#### 步骤2.3：选择Codespaces标签

1. **在下拉菜单中**，找到 **"Codespaces"** 标签
   - 可能在中间或底部位置
   - 标签下方显示："+ New codespace on main"

2. **点击这个标签**
   - 展开Codespaces选项
   - 显示："Create codespace on main"

#### 步骤2.4：创建Codespace

1. **点击 "Create codespace on main"**

2. **选择配置（可选）**
   ```
   通常会自动选择默认配置，直接点击 "Create codespace" 即可
   ```

3. **等待创建**
   - 页面会显示创建进度
   - 时间：约1-3分钟（取决于网络速度）
   - 你会看到：
     - 正在配置虚拟机...
     - 正在安装扩展...
     - 正在设置环境...

✅ **创建成功后，会进入Codespace编辑器界面**

---

## 第3步：认识Codespace界面

### 界面布局说明

```
┌─────────────────────────────────────────────────────┐
│  仓库文件列表    │   代码编辑区域    │   右侧面板   │
│  (左侧)         │   (中间)         │   (可选)     │
│                 │                  │              │
│  📁 api/        │   这里显示代码    │   搜索/扩展  │
│  📁 assets/     │                  │              │
│  📁 config/     │   ↓↓↓           │              │
│  📁 src/        │   # 文件内容    │              │
│                 │                  │              │
├─────────────────────────────────────────────────────┤
│                终端窗口 (底部)                        │
│  Welcome to GitHub Codespaces!                       │
│  user@codespace:~$                                    │
└─────────────────────────────────────────────────────┘
```

### 界面各部分功能

- **左侧文件列表**：显示项目所有文件和文件夹
- **中间代码编辑区**：编辑和查看代码
- **底部终端**：输入命令的地方（我们主要在这里操作）
- **顶部菜单栏**：包含Ports、Source Control等标签

---

## 第4步：在终端中运行命令

### 步骤4.1：确认终端已打开

1. **查看底部**，应该有一个终端窗口
   - 提示符类似：`user@codespace:~$`
   - 如果没有，按 `Ctrl + ~`（波浪号）打开终端

### 步骤4.2：进入项目目录

```bash
# 输入以下命令（按回车确认）
cd /workspaces/你的仓库名

# 示例：
cd /workspaces/智能股票分析系统

# 查看当前目录内容（确认）
ls
```

**期望看到的内容：**
```
api/    assets/    config/    docs/    src/
requirements.txt    README.md
```

### 步骤4.3：确认Python版本

```bash
# 查看Python版本
python --version
```

**期望输出：**
```
Python 3.9.x 或 Python 3.10.x 或 Python 3.11.x
```

✅ **确认Python版本3.9+后，继续下一步**

### 步骤4.4：安装项目依赖

这是最重要的一步！安装项目所需的所有Python包。

```bash
# 安装依赖（需要1-2分钟）
pip install -r requirements.txt
```

**你会看到：**
```
Collecting flask
  Downloading flask-3.0.0-py3-none-any.whl
Collecting langchain
  Downloading langchain-0.1.0-py3-none-any.whl
Collecting ...
Installing collected packages: flask, langchain, ...
Successfully installed flask-3.0.0 langchain-0.1.0 ...
```

**等待提示 "Successfully installed" 出现后，继续**

### 步骤4.5：安装额外的服务器依赖

```bash
# 安装gunicorn（生产环境服务器）
pip install gunicorn

# 安装requests（如果不在requirements.txt中）
pip install requests
```

**期望输出：**
```
Successfully installed gunicorn-21.2.0
Successfully installed requests-2.31.0
```

✅ **所有依赖安装完成！**

---

## 第5步：启动Flask服务器

### 步骤5.1：进入api目录

```bash
# 进入api目录
cd api

# 确认目录内容
ls
```

**期望看到：**
```
server.py
```

### 步骤5.2：启动服务器

```bash
# 启动Flask应用
python server.py
```

**你会看到启动日志：**
```
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment.
 * Running on http://0.0.0.0:5000
Press CTRL+C to quit
```

✅ **看到 "Running on http://0.0.0.0:5000" 表示启动成功！**

**重要提示：**
- ⚠️ 不要关闭这个终端窗口
- ⚠️ 不要按 Ctrl+C（这会停止服务）
- ⚠️ 保持这个窗口打开

---

## 第6步：访问Web应用

### 方法1：通过Ports标签（推荐）

#### 步骤6.1：找到Ports标签

1. **查看Codespace窗口顶部**
   - 找到 "PORTS" 标签（在 "TERMINAL" 旁边）
   - 点击 "PORTS" 标签

#### 步骤6.2：查看端口信息

1. **你会看到端口列表：**
   ```
   Forwarded Ports
   Local Address  Forwarded Address   Visible  Browser
   5000          https://xxxx-5000.app.github.dev   ✔     Open Browser
   ```

2. **说明：**
   - Local Address: 5000（本地端口）
   - Forwarded Address: https://xxxx-5000.app.github.dev（访问地址）
   - Visible: ✔（已转发）
   - Browser: Open Browser（点击可以打开）

#### 步骤6.3：打开浏览器

1. **点击 "Open Browser" 列的按钮**
   - 按钮位置：最右侧
   - 按钮图标：🌐 浏览器图标
   - 按钮文字："Open Browser"

2. **浏览器会自动打开**
   - 地址栏显示：https://xxxx-5000.app.github.dev
   - 看到股票分析系统的界面

✅ **成功访问应用！**

---

### 方法2：复制URL直接访问

1. **在Ports标签中，找到 Forwarded Address**
   ```
   https://xxxx-5000.app.github.dev
   ```

2. **复制这个URL**

3. **在浏览器新标签页中粘贴并访问**

---

### 方法3：点击弹出通知

1. **当你启动服务器后**
   - 顶部可能会弹出一个通知
   - 提示："Your application is running on http://0.0.0.0:5000"
   - 通知中有一个链接 "Open in Browser"

2. **点击这个链接**

3. **浏览器自动打开应用**

---

## 第7步：使用应用

### 测试诊股功能

1. **在页面找到诊股区域**
2. **输入股票代码或名称**
   ```
   示例：
   - 贵州茅台
   - 600519
   - 平安银行
   ```
3. **点击"开始诊断"按钮**
4. **等待结果显示**
   - 分析结果会在页面上显示
   - 包含股票基本信息、技术分析等

### 测试选股功能

1. **在页面找到选股区域**
2. **设置选股条件**
   ```
   示例：
   - 行业：科技
   - 市值：大于100亿
   - 市盈率：小于30
   ```
3. **点击"开始选股"按钮**
4. **查看推荐的股票列表**

### 测试其他功能

- 邮箱登记
- 搜索股票
- 查看历史记录

---

## 第8步：停止和重启服务

### 停止服务（当你不使用时）

#### 方法1：在终端停止
```bash
# 在运行服务器的终端窗口中
# 按以下组合键：

Ctrl + C
```

**你会看到：**
```
^C
user@codespace:~/your-repo/api$
```

**服务已停止**

#### 方法2：关闭Codespace
```
1. 关闭浏览器标签页
2. Codespace会自动保存状态
3. 下次打开会恢复
```

### 重启服务（当你想继续使用时）

#### 如果终端还在：
```bash
# 直接再次运行
python server.py
```

#### 如果终端已关闭：
```bash
# 1. 重新打开终端
按 Ctrl + ~

# 2. 进入目录
cd api

# 3. 启动服务
python server.py

# 4. 访问Ports标签打开浏览器
```

---

## 🆘 常见问题和解决方案

### 问题1：找不到Codespace按钮

**现象：**
- 仓库页面没有绿色的"Code"按钮
- 或没有"Codespaces"选项

**解决方案：**
```
1. 确认你已登录GitHub账号
2. 确认仓库是公共的或你有权限访问
3. 刷新页面重新尝试
```

### 问题2：Codespace创建失败

**现象：**
- 创建进度卡住不动
- 显示错误信息

**解决方案：**
```
1. 检查网络连接
2. 刷新页面重新创建
3. 检查GitHub账号的Codespaces额度
   - 免费账号每月60小时
```

### 问题3：pip安装失败

**现象：**
```
ERROR: Could not find a version that satisfies the requirement xxx
```

**解决方案：**
```
# 方法1：升级pip
python -m pip install --upgrade pip

# 方法2：重新安装
pip install -r requirements.txt

# 方法3：单独安装失败的包
pip install flask
pip install langchain
# ...
```

### 问题4：服务器启动失败

**现象：**
```
ModuleNotFoundError: No module named 'flask'
```

**解决方案：**
```bash
# 确认依赖已安装
pip list | grep flask

# 如果没有，重新安装
pip install flask

# 再次尝试启动
python server.py
```

### 问题5：无法访问端口5000

**现象：**
- 点击"Open Browser"后显示"无法访问此网站"

**解决方案：**
```
1. 确认服务器正在运行
   - 检查终端是否显示 "Running on http://0.0.0.0:5000"

2. 检查Ports标签
   - 确认端口5000状态为 ✔

3. 手动复制URL访问
   - 在Ports标签中复制 Forwarded Address
   - 在浏览器中粘贴访问

4. 刷新页面
```

### 问题6：终端命令不响应

**现象：**
- 输入命令后没有反应
- 光标闪烁但不显示结果

**解决方案：**
```
1. 检查是否有命令正在运行
   - 按 Ctrl+C 中断

2. 打开新终端
   - 点击终端窗口右上角的 "+"
   - 创建新的终端窗口

3. 在新终端中重试
```

### 问题7：页面显示错误

**现象：**
- 浏览器显示"Internal Server Error"
- 页面显示"404 Not Found"

**解决方案：**
```bash
# 1. 查看终端错误信息
# 在运行server.py的终端中查看日志

# 2. 检查文件是否完整
ls
# 确认api/server.py存在

# 3. 检查端口是否被占用
# 如果显示 "Address already in use"
# 更换端口，修改server.py中的端口配置
```

---

## 💡 实用技巧

### 技巧1：保持服务运行

```
如果你想长时间运行服务（比如展示给朋友看）：

1. 不要关闭Codespace标签页
2. 不要按Ctrl+C
3. Codespace会在后台运行（限制时间内）

注意：免费账号的Codespace会在无活动一段时间后自动休眠
```

### 技巧2：多终端操作

```
你可以打开多个终端窗口：

1. 终端1：运行服务器
   python server.py

2. 终端2：查看日志或执行其他命令
   ls
   cat server.py
```

### 技巧3：查看文件内容

```bash
# 查看server.py内容
cat server.py

# 或使用编辑器打开
# 在左侧文件列表中点击文件
```

### 技巧4：编辑代码

```
1. 在左侧文件列表中找到要编辑的文件
2. 双击文件打开
3. 在中间编辑区修改代码
4. 保存：Ctrl + S
5. 重启服务器查看效果
```

### 技巧5：检查Python包

```bash
# 查看已安装的所有包
pip list

# 搜索特定包
pip list | grep flask

# 查看包信息
pip show flask
```

---

## 📊 Codespaces使用限制

### 免费账号限制

| 项目 | 限制 |
|------|------|
| **每月使用时长** | 60小时 |
| **每次运行时长** | 最长12小时（无活动后自动休眠） |
| **存储空间** | 15GB |
| **CPU** | 2核 |
| **内存** | 8GB |

### 付费账号

- 如需更多时长，可以升级到付费计划
- 价格：$10/月起

---

## 🔄 下次使用

### 如何快速重新启动

```
1. 打开GitHub仓库
2. 点击 "Code" → "Codespaces"
3. 找到你之前的Codespace
4. 点击继续（Resume）
5. 在终端运行：
   cd api
   python server.py
6. 访问Ports标签打开浏览器
```

### 如何创建新的Codespace

```
如果之前的Codespace已过期或想创建新的：

1. 仓库页面 → "Code" → "Codespaces"
2. 点击 "+ New codespace"
3. 按照第4-7步操作即可
```

---

## 🎉 总结

### 操作流程图

```
打开GitHub仓库
    ↓
点击绿色Code按钮
    ↓
选择Codespaces标签
    ↓
点击Create codespace
    ↓
等待1-2分钟创建完成
    ↓
终端输入：pip install -r requirements.txt
    ↓
进入api目录：cd api
    ↓
启动服务：python server.py
    ↓
点击Ports标签的Open Browser
    ↓
开始使用！
```

### 核心命令速查

```bash
# 安装依赖
pip install -r requirements.txt

# 启动服务器
cd api
python server.py

# 停止服务器
Ctrl + C

# 查看端口
点击顶部PORTS标签
```

---

## 🆘 还是有问题？

### 获取帮助

1. **查看GitHub官方文档**
   - https://docs.github.com/codespaces

2. **查看Codespaces状态**
   - https://www.githubstatus.com/
   - 检查GitHub服务是否正常

3. **联系GitHub支持**
   - 仓库页面 → "Settings" → "Contact GitHub Support"

---

## 🎯 快速开始检查清单

开始前确认：

- [ ] 已登录GitHub
- [ ] 已找到正确的仓库
- [ ] 网络连接正常
- [ ] 有至少5分钟时间

操作步骤：

- [ ] 点击Code → Codespaces → Create
- [ ] 等待创建完成（1-2分钟）
- [ ] 在终端运行：`pip install -r requirements.txt`
- [ ] 运行：`cd api`
- [ ] 运行：`python server.py`
- [ ] 看到启动成功提示
- [ ] 点击Ports标签的Open Browser
- [ ] 浏览器打开应用界面

✅ **全部完成，开始使用吧！**

---

**祝你在GitHub Codespaces中使用愉快！** 🚀

有任何问题随时问我！
