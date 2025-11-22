# Vercel 部署配置指南

## ⚠️ 如果遇到 404 错误，按以下步骤检查

### 第一步：检查 Vercel 项目设置

登录 Vercel，进入你的项目设置页面，确保配置如下：

#### 1. 根目录设置
```
Root Directory: frontend
```
⚠️ **重要**：必须设置为 `frontend`，不是项目根目录！

#### 2. 构建设置
```
Framework Preset: Vite
Build Command: npm run build
Output Directory: dist
Install Command: npm install
```

#### 3. 环境变量
```
VITE_API_BASE_URL = https://your-backend-url.com
```

### 第二步：如果已经部署，重新配置

1. 进入 Vercel Dashboard
2. 选择你的项目
3. 点击 "Settings" (设置)
4. 找到 "General" → "Root Directory"
5. 点击 "Edit" 修改为 `frontend`
6. 保存并重新部署

### 第三步：通过 Git 重新部署

```bash
cd /Users/zhengyunlong/PycharmProjects/BlackCat

# 提交最新的 vercel.json 修改
git add .
git commit -m "fix: 修复 Vercel 配置"
git push

# Vercel 会自动检测并重新部署
```

---

## 🔍 详细排查步骤

### 问题 1: 根目录配置错误

**症状**: 访问任何路径都是 404

**原因**: Vercel 在项目根目录查找 `package.json`，但前端代码在 `frontend` 目录

**解决方案**:
1. Vercel Dashboard → Settings → General
2. Root Directory: 设置为 `frontend`
3. 点击 Save

### 问题 2: 路由重写未生效

**症状**: 首页正常，但刷新其他页面 404

**原因**: Vue Router 使用 History 模式，需要服务器端重写

**解决方案**: 
- `vercel.json` 中的 rewrites 配置已经添加
- 确保 `vercel.json` 在 `frontend` 目录下

### 问题 3: 构建失败

**症状**: 部署日志显示构建错误

**原因**: 依赖安装失败或构建命令错误

**解决方案**:
```bash
# 本地测试构建
cd frontend
npm install
npm run build

# 如果成功，检查 dist 目录是否生成
ls -la dist/
```

---

## ✅ 正确的 Vercel 配置

### 通过 Web 界面配置

![Vercel Settings](https://i.imgur.com/example.png)

#### General 设置
| 配置项 | 值 |
|--------|-----|
| Root Directory | `frontend` |
| Node.js Version | 18.x (或更高) |

#### Build & Development Settings
| 配置项 | 值 |
|--------|-----|
| Framework Preset | Vite |
| Build Command | `npm run build` |
| Output Directory | `dist` |
| Install Command | `npm install` |

#### Environment Variables
| 变量名 | 值 | 环境 |
|--------|-----|------|
| VITE_API_BASE_URL | https://your-backend.railway.app | Production |

### 通过 vercel.json 配置

已创建在 `frontend/vercel.json`，内容：

```json
{
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ],
  "headers": [
    {
      "source": "/assets/(.*)",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "public, max-age=31536000, immutable"
        }
      ]
    }
  ]
}
```

---

## 🚀 推荐的部署流程

### 方法 1: 通过 Vercel CLI（最可靠）

```bash
# 1. 安装 Vercel CLI
npm i -g vercel

# 2. 进入前端目录
cd frontend

# 3. 登录
vercel login

# 4. 首次部署（预览）
vercel

# 5. 部署到生产环境
vercel --prod

# 按提示操作，CLI 会自动检测 Vite 项目
```

### 方法 2: 通过 GitHub（需要正确配置）

```bash
# 1. 确保 vercel.json 在 frontend 目录
ls frontend/vercel.json

# 2. 提交到 GitHub
git add .
git commit -m "配置 Vercel 部署"
git push

# 3. 在 Vercel 中导入项目
# - 访问 https://vercel.com/new
# - 选择 GitHub 仓库
# - Root Directory 设置为 "frontend"
# - 其他保持默认
# - 添加环境变量 VITE_API_BASE_URL
# - 点击 Deploy
```

---

## 🧪 部署后测试

### 1. 检查构建日志
在 Vercel Dashboard 查看部署日志：
- 是否成功找到 `frontend` 目录
- `npm install` 是否成功
- `npm run build` 是否成功
- 是否生成了 `dist` 目录

### 2. 检查页面
```
✅ https://your-app.vercel.app/         # 首页应该显示
✅ https://your-app.vercel.app/login    # 登录页应该显示
✅ https://your-app.vercel.app/register # 注册页应该显示
```

### 3. 检查静态资源
```
✅ https://your-app.vercel.app/logo.jpg # LOGO 应该显示
✅ 浏览器控制台无 404 错误
```

### 4. 检查 API 连接
```bash
# 在浏览器控制台执行
console.log(import.meta.env.VITE_API_BASE_URL)
// 应该输出你的后端 URL
```

---

## 📞 如果还是 404

### 最后的杀手锏：重新创建项目

```bash
# 1. 在 Vercel 删除当前项目

# 2. 使用 CLI 重新部署
cd frontend
vercel --prod

# 3. CLI 会引导你完成所有配置
```

### 或者联系支持

如果以上都不行，可能是以下原因：
1. GitHub 仓库权限问题
2. Vercel 账户限制
3. 构建环境问题

可以在 Vercel Dashboard → Help 提交工单。

---

## 💡 常见错误和解决方案

### 错误 1: "No such file or directory: package.json"
**解决**: Root Directory 设置为 `frontend`

### 错误 2: "Module not found: Can't resolve './App.vue'"
**解决**: 确保所有文件都已提交到 Git

### 错误 3: "Failed to load module script"
**解决**: 检查 `vite.config.ts` 中的 `base` 配置，应该为 `/`

### 错误 4: 白屏或空页面
**解决**: 
1. 检查浏览器控制台错误
2. 确认 `index.html` 存在
3. 检查 `dist` 目录结构

---

## ✅ 成功部署的标志

- Vercel 构建日志显示 "Build Completed"
- 访问首页能看到 BlackCat LOGO
- 能够访问 `/login`、`/register` 等路由
- 浏览器控制台无错误
- 静态资源（CSS、JS、图片）加载正常

---

希望这能帮助你解决 404 问题！如果还有问题，请提供：
1. Vercel 部署日志
2. 浏览器控制台错误
3. 当前的 Root Directory 设置

我会进一步帮你排查！🔧
