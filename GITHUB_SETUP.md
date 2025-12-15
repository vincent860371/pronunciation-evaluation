# 推送项目到 GitHub 的步骤

## 1. 在 GitHub 上创建新仓库

1. 登录 https://github.com
2. 点击右上角的 "+" 按钮，选择 "New repository"
3. 填写仓库信息：
   - Repository name: `speech-evaluation-tencent` 或 `语音评测-腾讯智聆`
   - Description: 基于腾讯云智聆的英文口语评测系统
   - 选择 Public 或 Private
   - **不要勾选** "Initialize this repository with a README"
4. 点击 "Create repository"

## 2. 连接本地仓库到 GitHub

在您的项目目录中运行以下命令（替换 YOUR_USERNAME 为您的 GitHub 用户名）：

```bash
# 添加远程仓库
git remote add origin https://github.com/YOUR_USERNAME/语音评测-腾讯智聆.git

# 或者使用 SSH（如果已配置）
git remote add origin git@github.com:YOUR_USERNAME/语音评测-腾讯智聆.git

# 推送代码
git push -u origin master
```

## 3. 如果使用 HTTPS，需要身份验证

GitHub 已不再支持密码认证，需要使用以下方式之一：

### 方式 1: Personal Access Token (推荐)

1. 访问 https://github.com/settings/tokens
2. 点击 "Generate new token (classic)"
3. 勾选 `repo` 权限
4. 生成并复制 token
5. 推送时使用 token 作为密码

### 方式 2: GitHub CLI

```bash
# 安装 GitHub CLI
winget install GitHub.cli

# 认证
gh auth login

# 推送
git push -u origin master
```

## 4. 验证推送成功

访问您的 GitHub 仓库页面，应该能看到所有文件。

## 已完成的本地操作

✅ Git 仓库已初始化
✅ 所有项目文件已添加
✅ 首次提交已完成
✅ 用户信息已配置

## 注意事项

- ⚠️ 敏感信息（.env 文件）已被 .gitignore 排除
- ⚠️ 虚拟环境目录（venv/）已被排除
- ✅ 项目文档已完善（README_PROJECT.md）

