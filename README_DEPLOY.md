# BlackCat AI - 部署文件说明

## 📁 已创建的部署相关文件

### 前端部署文件（Vercel）

1. **`frontend/vercel.json`**
   - Vercel 配置文件
   - 配置路由重写、缓存策略

2. **`frontend/.env.production`**
   - 生产环境变量
   - 需要设置 `VITE_API_BASE_URL` 为后端地址

3. **`frontend/.env.development`**
   - 开发环境变量
   - 默认指向本地后端

4. **`frontend/src/services/api.ts`**
   - 已修改为支持环境变量
   - 自动根据环境选择 API 地址

### 后端部署文件

1. **`Procfile`**
   - Railway/Heroku 启动命令配置

2. **`railway.json`**
   - Railway 平台专用配置
   - 包含自动数据库迁移

3. **`render.yaml`**
   - Render 平台专用配置
   - 包含环境变量模板

### 文档文件

1. **`DEPLOYMENT.md`**
   - 完整部署文档
   - 包含多种平台的详细步骤

2. **`QUICK_DEPLOY.md`**
   - 5 分钟快速部署指南
   - 适合快速上手

3. **`README_DEPLOY.md`**（本文件）
   - 部署文件总览

---

## 🚀 快速开始

### 方式 1：完全自动化（推荐）

1. **部署后端到 Railway**
   ```bash
   # 推送代码到 GitHub
   git add .
   git commit -m "准备部署"
   git push
   
   # 访问 https://railway.app
   # 导入 GitHub 仓库，Railway 会自动识别 railway.json
   ```

2. **部署前端到 Vercel**
   ```bash
   # 访问 https://vercel.com
   # 导入 GitHub 仓库，Vercel 会自动识别 vercel.json
   # 设置 Root Directory 为 "frontend"
   # 添加环境变量 VITE_API_BASE_URL
   ```

### 方式 2：通过 CLI

```bash
# 后端（Railway）
npm i -g @railway/cli
railway login
railway init
railway up

# 前端（Vercel）
npm i -g vercel
cd frontend
vercel --prod
```

---

## ⚙️ 必需的环境变量

### Vercel（前端）
```env
VITE_API_BASE_URL=https://your-backend.railway.app
```

### Railway/Render（后端）
```env
JWT_SECRET=随机生成的密钥
SILICONFLOW_API_KEY=sk-xxxxx
SMTP_HOST=smtp.qq.com
SMTP_PORT=587
SMTP_USER=your-email@qq.com
SMTP_PASSWORD=your-password
MODEL_NAME=Qwen/Qwen2-VL-7B-Instruct
DATABASE_URL=sqlite:///./blackcat.db
```

---

## 📝 部署检查清单

- [ ] 代码已推送到 GitHub
- [ ] 后端已部署（Railway/Render）
- [ ] 获得后端 URL
- [ ] 前端已部署到 Vercel
- [ ] Vercel 环境变量已设置
- [ ] 后端 CORS 已配置前端域名
- [ ] 数据库迁移已运行
- [ ] 功能测试通过

---

## 🔍 验证部署

### 检查后端
访问: `https://your-backend.railway.app/docs`
应该能看到 FastAPI 文档页面

### 检查前端
访问: `https://your-app.vercel.app`
应该能看到登录页面和 LOGO

### 检查 API 连接
1. 在前端注册账号
2. 上传图片测试识别
3. 检查历史记录

---

## ❓ 常见问题

### Q: Vercel 部署成功但页面空白
A: 检查浏览器控制台错误，可能是 API 地址配置问题

### Q: Railway 部署失败
A: 检查 `backend/requirements.txt` 是否完整，查看构建日志

### Q: CORS 错误
A: 在 `backend/app/main.py` 中添加 Vercel 域名到 `allow_origins`

### Q: 图片无法上传
A: 检查后端是否有文件写入权限，可能需要配置持久化存储

---

## 📞 获取帮助

- 完整文档: 查看 `DEPLOYMENT.md`
- 快速指南: 查看 `QUICK_DEPLOY.md`
- Railway 文档: https://docs.railway.app
- Vercel 文档: https://vercel.com/docs
- Render 文档: https://render.com/docs

---

## 🎉 部署成功后

记得：
1. 备份数据库文件
2. 设置域名（可选）
3. 配置监控和日志
4. 定期更新依赖

祝部署顺利！🚀
