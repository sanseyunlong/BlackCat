# Vercel 404 问题排查清单

## 🔍 立即检查这些配置

### ✅ 步骤 1: Vercel 项目设置

登录 Vercel Dashboard，检查：

- [ ] **Root Directory** 设置为 `frontend` （不是留空！）
- [ ] **Framework Preset** 选择 `Vite`
- [ ] **Build Command** 是 `npm run build`
- [ ] **Output Directory** 是 `dist`

📍 **如何修改**:
1. 进入项目 → Settings → General
2. 找到 "Root Directory" 
3. 点击 "Edit"
4. 输入 `frontend`
5. Save

### ✅ 步骤 2: 测试静态文件

访问: `https://your-app.vercel.app/test.html`

- **如果显示测试页面** ✅ → 静态文件正常，继续步骤 3
- **如果显示 404** ❌ → Root Directory 配置错误，回到步骤 1

### ✅ 步骤 3: 测试首页

访问: `https://your-app.vercel.app/`

- **如果显示 BlackCat 登录页** ✅ → 部署成功！
- **如果显示 404** ❌ → 路由配置问题，继续步骤 4

### ✅ 步骤 4: 检查 vercel.json

确保 `frontend/vercel.json` 存在且内容正确：

```bash
# 在本地检查
cat frontend/vercel.json
```

应该包含：
```json
{
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ]
}
```

### ✅ 步骤 5: 重新部署

```bash
# 提交更新
git add .
git commit -m "fix: 修复 Vercel 配置"
git push

# 或使用 CLI 重新部署
cd frontend
vercel --prod
```

---

## 🚨 常见错误和快速修复

### 错误 A: 整个站点 404
**原因**: Root Directory 未设置或设置错误
**快速修复**:
1. Vercel Settings → General → Root Directory
2. 设置为 `frontend`
3. Redeploy

### 错误 B: 首页正常，其他页面 404
**原因**: 路由重写配置缺失
**快速修复**:
1. 确认 `frontend/vercel.json` 存在
2. 确认包含 rewrites 配置
3. Git 提交并推送

### 错误 C: 构建失败
**原因**: 依赖或构建命令错误
**快速修复**:
```bash
# 本地测试构建
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run build
```

---

## 💡 使用 CLI 部署（最可靠）

如果网页配置复杂，直接用 CLI：

```bash
# 1. 安装 CLI
npm i -g vercel

# 2. 进入前端目录（重要！）
cd frontend

# 3. 登录
vercel login

# 4. 部署
vercel --prod

# CLI 会自动检测 Vite 并配置正确
```

---

## 📋 完整检查清单

- [ ] GitHub 仓库已更新最新代码
- [ ] `frontend/vercel.json` 文件存在
- [ ] `frontend/package.json` 包含正确的 scripts
- [ ] Vercel Root Directory = `frontend`
- [ ] Vercel Framework Preset = Vite
- [ ] 环境变量 VITE_API_BASE_URL 已设置
- [ ] 测试页面 `/test.html` 可访问
- [ ] 首页 `/` 可访问
- [ ] 子路由 `/login` 可访问

---

## 🎯 终极解决方案

如果以上都不行，删除 Vercel 项目重新创建：

```bash
# 1. 在 Vercel Dashboard 删除项目

# 2. 使用 CLI 重新部署
cd frontend
vercel --prod

# 3. 按提示选择：
# - Setup and deploy? Y
# - Which scope? [选择你的账户]
# - Link to existing project? N
# - What's your project's name? blackcat-frontend
# - In which directory is your code located? ./
# - Want to override the settings? N

# 4. 等待部署完成
```

---

## 📞 需要更多帮助？

请提供以下信息：

1. **Vercel 部署 URL**
2. **Root Directory 当前设置** (截图)
3. **部署日志**（最后 50 行）
4. **访问 /test.html 的结果**

这样我可以更精准地帮你解决问题！
