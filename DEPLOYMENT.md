# BlackCat AI 部署指南

## 架构说明

本项目采用前后端分离架构：
- **前端**: Vue 3 + Vite + Vuetify (部署到 Vercel)
- **后端**: FastAPI + SQLite + Alembic (部署到支持 Python 的平台)

---

## 一、前端部署到 Vercel

### 1. 准备工作

确保 `frontend` 目录包含以下文件：
- `vercel.json` - Vercel 配置文件 ✅
- `.env.production` - 生产环境变量 ✅
- `package.json` - 依赖配置 ✅

### 2. 部署步骤

#### 方式 A：通过 Vercel CLI（推荐）

```bash
# 安装 Vercel CLI
npm i -g vercel

# 进入前端目录
cd frontend

# 登录 Vercel
vercel login

# 部署（首次）
vercel

# 部署到生产环境
vercel --prod
```

#### 方式 B：通过 GitHub 集成

1. 将代码推送到 GitHub
2. 访问 [vercel.com](https://vercel.com) 并登录
3. 点击 "New Project"
4. 选择你的 GitHub 仓库
5. 配置项目：
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`

### 3. 配置环境变量

在 Vercel 项目设置中添加环境变量：

| 变量名 | 值 | 说明 |
|--------|-----|------|
| `VITE_API_BASE_URL` | `https://your-backend-api.com` | 后端 API 地址 |

⚠️ **重要**：部署后需要将此值改为实际的后端 API 地址！

---

## 二、后端部署

后端需要部署到支持 Python 和持久化存储的平台。以下是推荐方案：

### 方案 1: Railway（推荐 - 最简单）

**优点**: 自动部署、免费额度、支持 SQLite、内置域名

#### 部署步骤：

1. 访问 [railway.app](https://railway.app) 并登录

2. 创建 `railway.json` 配置文件：

```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT",
    "healthcheckPath": "/health",
    "restartPolicyType": "ON_FAILURE"
  }
}
```

3. 创建 `Procfile` 文件（可选）：

```
web: cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

4. 设置环境变量：
   - `JWT_SECRET`: 随机生成的密钥
   - `SMTP_PASSWORD`: 邮箱密码
   - `SILICONFLOW_API_KEY`: AI API 密钥
   - `DATABASE_URL`: SQLite 路径（默认：`sqlite:///./blackcat.db`）

5. 部署：
   - 连接 GitHub 仓库
   - 选择 `backend` 目录
   - 自动构建和部署

6. 获取部署 URL 并更新 Vercel 环境变量

---

### 方案 2: Render

**优点**: 免费计划、支持 PostgreSQL、易用

#### 部署步骤：

1. 访问 [render.com](https://render.com)

2. 创建 `render.yaml` 配置：

```yaml
services:
  - type: web
    name: blackcat-backend
    env: python
    buildCommand: "cd backend && pip install -r requirements.txt"
    startCommand: "cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT"
    envVars:
      - key: PYTHON_VERSION
        value: 3.9
      - key: JWT_SECRET
        generateValue: true
      - key: DATABASE_URL
        value: sqlite:///./data/blackcat.db
```

3. 添加环境变量并部署

---

### 方案 3: Fly.io

**优点**: 全球分布、支持持久化卷、Docker 部署

#### 部署步骤：

1. 创建 `Dockerfile`（在项目根目录）：

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ ./backend/

EXPOSE 8000

CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

2. 安装 Fly CLI：
```bash
curl -L https://fly.io/install.sh | sh
```

3. 登录并初始化：
```bash
fly auth login
fly launch
```

4. 创建持久化卷：
```bash
fly volumes create blackcat_data --size 1
```

5. 部署：
```bash
fly deploy
```

---

## 三、后端 CORS 配置

确保后端允许前端域名的跨域请求。修改 `backend/app/main.py`：

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # 开发环境
        "https://your-vercel-app.vercel.app",  # 生产环境
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 四、数据库迁移

生产环境首次部署时运行迁移：

```bash
cd backend
alembic upgrade head
```

如果使用 PostgreSQL，需要修改 `backend/app/config.py` 中的数据库连接字符串。

---

## 五、验证部署

### 前端验证：
1. 访问 Vercel 部署的 URL
2. 检查是否能正常加载页面
3. 打开浏览器控制台，检查 API 请求是否指向正确的后端地址

### 后端验证：
1. 访问 `https://your-backend-api.com/docs`
2. 测试 API 端点
3. 检查日志确认服务运行正常

---

## 六、环境变量清单

### 前端 (Vercel)
```
VITE_API_BASE_URL=https://your-backend-api.com
```

### 后端 (Railway/Render/Fly.io)
```
JWT_SECRET=your-random-secret-key
SMTP_HOST=smtp.qq.com
SMTP_PORT=587
SMTP_USER=your-email@qq.com
SMTP_PASSWORD=your-smtp-password
SILICONFLOW_API_KEY=sk-xxxxx
SILICONFLOW_BASE_URL=https://api.siliconflow.cn/v1
MODEL_NAME=Qwen/Qwen2-VL-7B-Instruct
DATABASE_URL=sqlite:///./blackcat.db
```

---

## 七、常见问题

### Q1: 前端部署后 404 错误
**解决**: 确保 `vercel.json` 包含路由重写配置

### Q2: API 跨域错误
**解决**: 检查后端 CORS 配置是否包含前端域名

### Q3: 数据库连接失败
**解决**: 确保数据库文件路径正确，Railway/Render 需要使用持久化卷

### Q4: 图片上传失败
**解决**: 确保后端有写入权限，检查上传目录是否存在

---

## 八、监控和日志

- **Vercel**: 内置日志和分析面板
- **Railway**: 实时日志流
- **Render**: Web 日志查看器
- **Fly.io**: `fly logs` 命令

---

## 九、成本估算

### 免费方案组合：
- **Vercel**: 100GB 带宽/月（前端）
- **Railway**: $5 免费额度/月（后端）
- **总成本**: $0-5/月

### 生产环境推荐：
- **Vercel Pro**: $20/月
- **Railway**: $10-20/月
- **总成本**: $30-40/月

---

## 十、下一步

1. 部署后端到 Railway/Render
2. 获取后端 API 地址
3. 更新 Vercel 环境变量 `VITE_API_BASE_URL`
4. 重新部署前端
5. 测试完整功能

🎉 部署完成！
