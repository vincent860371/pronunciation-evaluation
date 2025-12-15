# 更新日志

## [2.0.0] - 2025-12-15

### 🎉 重大更新

**仅保留 WebSocket 版本，移除 HTTP 版本**

根据腾讯云智聆口语评测接口要求，项目已完全迁移到 WebSocket 协议，提供更好的实时评测体验。

### ✨ 新增功能

- ✅ WebSocket 实时流式评测
- ✅ 边说边评，即时反馈
- ✅ 持续连接，降低延迟
- ✅ 实时返回评测结果
- ✅ 支持音频流式传输
- ✅ 一键安装脚本 (`setup.bat`)
- ✅ 一键启动脚本 (`start.bat`)

### 🗑️ 移除功能

- ❌ 移除 HTTP REST API 版本
- ❌ 移除 `app.py` (旧 HTTP 版本)
- ❌ 移除 `index.html` (旧 HTTP 版本)
- ❌ 移除 `start_http.bat`

### 📝 文件更改

**重命名**:
- `app_websocket.py` → `app.py`
- `index_websocket.html` → `index.html`
- `requirements_websocket.txt` → `requirements.txt`
- `start_websocket.bat` → `start.bat`

**新增**:
- `CHANGELOG.md` - 更新日志
- `WEBSOCKET_VERSION.md` - WebSocket 详细说明

**删除**:
- `README_PROJECT.md`
- HTTP 版本相关文件

### 🔧 技术改进

#### WebSocket 连接流程

```
前端 WebSocket → Flask-Sock → 腾讯云 WebSocket API
     ↓                ↓               ↓
   录音           转发数据        实时评测
     ↓                ↓               ↓
  显示结果    ←  推送结果  ←    返回评分
```

#### 音频处理

- 采样率: 16000Hz
- 采样精度: 16bits
- 声道: 单声道
- 格式: PCM, WAV, MP3, Speex
- 传输: 每 100ms 发送一次音频数据

### 📋 接口变更

#### WebSocket 消息格式

**开始评测**
```json
{
  "action": "start",
  "secret_id": "...",
  "secret_key": "...",
  "ref_text": "Hello world",
  "eval_mode": 1,
  "score_coeff": 1.5
}
```

**发送音频**
```json
{
  "action": "audio",
  "audio_data": "base64..."
}
```

**结束评测**
```json
{
  "action": "end"
}
```

### 🚀 升级指南

#### 从旧版本升级

1. **拉取最新代码**
```bash
git pull origin main
```

2. **重新安装依赖**
```bash
# Windows
setup.bat

# 或手动
pip install -r requirements.txt
```

3. **启动新版本**
```bash
# Windows
start.bat

# 或手动
python app.py
```

#### 兼容性说明

- ✅ 保持相同的评测参数
- ✅ 保持相同的 SecretId/SecretKey 配置
- ✅ 保持相同的端口 5000
- ⚠️ 前端连接方式改为 WebSocket
- ⚠️ 不再支持 HTTP POST 请求

### 📊 性能提升

| 指标 | 旧版本 (HTTP) | 新版本 (WebSocket) |
|------|---------------|-------------------|
| 延迟 | ~2-3秒 | ~500ms |
| 实时反馈 | ❌ | ✅ |
| 连接复用 | ❌ | ✅ |
| 流式传输 | ❌ | ✅ |

### 🐛 已修复问题

- ✅ 修复了录音结束后等待时间过长的问题
- ✅ 修复了无法实时查看评测进度的问题
- ✅ 优化了音频数据传输效率

### 📚 文档更新

- ✅ 更新了 README.md
- ✅ 添加了 WEBSOCKET_VERSION.md 详细说明
- ✅ 更新了 GITHUB_SETUP.md
- ✅ 简化了启动脚本

### 🔒 安全改进

- ✅ WebSocket 连接支持 WSS (HTTPS 环境)
- ✅ 改进了密钥传输安全性
- ✅ 添加了连接状态监控

---

## [1.0.0] - 2025-12-14

### 初始版本

- ✅ HTTP REST API 实现
- ✅ 基础评测功能
- ✅ 前端录音界面
- ✅ 腾讯云 SDK 集成

---

### 贡献者

- [@vincent860371](https://github.com/vincent860371)

### 反馈

如有问题或建议，请在 [GitHub Issues](https://github.com/vincent860371/pronunciation-evaluation/issues) 提交。

---

⭐ **感谢使用！如果项目对您有帮助，请给个 Star！**

