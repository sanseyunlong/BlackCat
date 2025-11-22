# 快速部署指南

## 🚀 5 分钟部署到 Vercel

### 第一步：准备后端（选择一个平台）

#### 选项 A：Railway（推荐）
1. 访问 https://railway.app
2. 点击 "Start a New Project"
3. 连接 GitHub 仓库
4. 选择 `backend` 目录
5. 添加环境变量：
   ```
   JWT_SECRET=随机字符串（例如：openssl rand -hex 32）
   SILICONFLOW_API_KEY=你的API密钥
   SMTP_PASSWORD=你的SMTP密码
   ```
6. 部署完成后，复制 Railway 给你的 URL（例如：`https://xxx.railway.app`）

#### 选项 B：Render
1. 访问 https://render.com
2. 创建 Web Service
3. 连接仓库，选择 `backend` 目录
4. 设置：
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. 添加环境变量（同上）
6. 复制 Render 给你的 URL

---

### 第二步：部署前端到 Vercel

#### 通过 GitHub（推荐）

1. 将代码推送到 GitHub：
   ```bash
   git add .
   git commit -m "准备部署"
   git push
   ```

2. 访问 https://vercel.com 并登录

3. 点击 "Add New Project"

4. 导入你的 GitHub 仓库

5. 配置项目：
   - **Framework**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`

6. 添加环境变量：
   - 变量名: `VITE_API_BASE_URL`
   - 值: 你的后端 URL（第一步获得的 Railway 或 Render URL）
   - 例如: `https://xxx.railway.app`

7. 点击 "Deploy"

8. 等待 2-3 分钟，部署完成！

#### 通过 CLI

```bash
# 安装 Vercel CLI
npm i -g vercel

# 进入前端目录
cd frontend

# 登录
vercel login

# 部署
vercel --prod

# 按提示设置环境变量
```

---

### 第三步：配置后端 CORS

部署后，需要更新后端 CORS 配置以允许前端域名。

1. 修改 `backend/app/main.py`：

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://your-vercel-app.vercel.app",  # 改为你的 Vercel 域名
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

2. 重新部署后端（Railway/Render 会自动检测 git 更新并重新部署）

---

### 第四步：测试

1. 访问你的 Vercel URL
2. 注册账号
3. 上传图片测试识别功能
4. 检查历史记录

---

## ✅ 完成清单

- [ ] 后端部署完成（获得后端 URL）
- [ ] 前端部署到 Vercel
- [ ] 设置 `VITE_API_BASE_URL` 环境变量
- [ ] 更新后端 CORS 配置
- [ ] 测试注册/登录功能
- [ ] 测试图片识别功能
- [ ] 测试历史记录功能

---

## 🔧 如果遇到问题

### 前端显示但 API 调用失败
- 检查 Vercel 环境变量 `VITE_API_BASE_URL` 是否正确
- 检查后端 CORS 配置是否包含前端域名
- 在浏览器控制台查看具体错误

### 后端部署失败
- 检查 `requirements.txt` 是否完整
- 检查环境变量是否都已设置
- 查看平台日志获取详细错误信息

### 数据库错误
- Railway/Render 会自动处理 SQLite
- 确保运行了数据库迁移：`alembic upgrade head`

---

## 💰 成本

- **Vercel**: 免费（Hobby 计划）
- **Railway**: 前 $5 免费，之后按使用量计费
- **Render**: 免费计划（有休眠机制）

**推荐**: Railway（无休眠，免费额度足够个人使用）

---

## 📚 需要更详细的说明？

查看完整部署文档：`DEPLOYMENT.md`
