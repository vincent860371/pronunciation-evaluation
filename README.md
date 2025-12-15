# 英文口语评测系统 - 腾讯智聆

基于腾讯云智聆口语评测（SOE）API 开发的英文口语评测 Web 应用，支持 **HTTP** 和 **WebSocket** 两种协议，提供发音准确度、流畅度和完整度等多维度评分。

## ✨ 功能特性

- 🎤 **实时录音评测** - 支持浏览器麦克风录音
- ⚡ **双协议支持** - HTTP REST API + WebSocket 实时流式
- 📊 **多维度评分** - 综合得分、准确度、流畅度、完整度
- 🎯 **多种评测模式** - 词模式、句子模式、段落模式、自由说模式
- 🎨 **现代化界面** - 深色主题，流畅动画效果
- 📱 **响应式设计** - 支持各种设备访问

## 🚀 快速开始

### 环境要求

- Python 3.7+
- 现代浏览器（Chrome/Firefox/Edge 等）
- 腾讯云账号（需要 SecretId 和 SecretKey）

### 安装步骤

1. **克隆项目**
```bash
git clone https://github.com/vincent860371/pronunciation-evaluation.git
cd pronunciation-evaluation
```

2. **创建虚拟环境**
```bash
python -m venv venv
```

3. **激活虚拟环境**

Windows:
```bash
venv\Scripts\activate
```

Linux/Mac:
```bash
source venv/bin/activate
```

4. **安装依赖**

选择一个版本安装依赖：

**HTTP 版本（简单快速）**
```bash
pip install -r requirements.txt
python app.py
```

**WebSocket 版本（实时流式）**
```bash
pip install -r requirements_websocket.txt
python app_websocket.py
```

5. **访问应用**

打开浏览器访问：http://localhost:5000

## 📋 版本对比

| 特性 | HTTP 版本 | WebSocket 版本 |
|------|-----------|----------------|
| **实时反馈** | ❌ 录音结束后返回 | ✅ 边说边评 |
| **延迟** | 较高 | 低 |
| **连接方式** | 短连接 | 长连接 |
| **流式传输** | ❌ | ✅ |
| **实现复杂度** | 简单 | 中等 |
| **适用场景** | 短音频评测 | 实时对话评测 |
| **文件** | `app.py` + `index.html` | `app_websocket.py` + `index_websocket.html` |

## 📁 项目结构

```
pronunciation-evaluation/
├── venv/                          # 虚拟环境
├── app.py                         # HTTP 后端服务
├── app_websocket.py               # WebSocket 后端服务
├── index.html                     # HTTP 版本前端
├── index_websocket.html           # WebSocket 版本前端
├── requirements.txt               # HTTP 版本依赖
├── requirements_websocket.txt     # WebSocket 版本依赖
├── README.md                      # 项目说明文档
├── WEBSOCKET_VERSION.md           # WebSocket 详细说明
├── GITHUB_SETUP.md                # GitHub 部署指南
└── .gitignore                     # Git 忽略文件
```

## 📝 使用说明

### 1. 获取腾讯云密钥

访问 [腾讯云控制台](https://console.cloud.tencent.com/capi) 获取：
- **SecretId** - API 调用者身份标识
- **SecretKey** - 签名密钥

### 2. 配置密钥

在网页中填写您的 SecretId 和 SecretKey

### 3. 开始评测

1. 选择评测模式和评分系数
2. 输入要朗读的英文文本
3. 点击"开始录音"并朗读
4. 点击"停止评测"获取结果

## ⚙️ 配置参数

### 评测模式

- **0** - 词模式：评测单个单词
- **1** - 句子模式：评测完整句子（推荐）
- **2** - 段落模式：评测多句段落
- **3** - 自由说模式：开放式评测

### 评分系数

- **1.0** - 严格评分
- **1.5** - 推荐（默认）
- **2.0** - 适中
- **3.0** - 宽松
- **4.0** - 非常宽松

### 音频要求

- **采样率**: 16000Hz
- **采样精度**: 16bits
- **声道**: 单声道 (mono)
- **格式**: PCM, WAV, MP3, Speex

## 🔧 技术栈

### 后端
- **Flask** - Python Web 框架
- **Flask-CORS** / **Flask-Sock** - 跨域 / WebSocket 支持
- **tencentcloud-sdk-python** - 腾讯云 SDK
- **websocket-client** - WebSocket 客户端

### 前端
- **原生 JavaScript** - 无框架依赖
- **WebRTC / WebSocket** - 浏览器录音和实时通信
- **CSS3** - 现代化样式和动画

## 📄 API 接口

### HTTP 版本

**POST /evaluate**

```json
{
  "secret_id": "your_secret_id",
  "secret_key": "your_secret_key",
  "ref_text": "Hello, how are you today?",
  "eval_mode": 1,
  "score_coeff": 1.5,
  "audio_data": "base64_encoded_audio"
}
```

### WebSocket 版本

**WS /ws/evaluate**

```javascript
// 连接
ws = new WebSocket('ws://localhost:5000/ws/evaluate')

// 开始评测
ws.send(JSON.stringify({
    action: 'start',
    secret_id: '...',
    ref_text: 'Hello world',
    eval_mode: 1
}))

// 发送音频
ws.send(JSON.stringify({
    action: 'audio',
    audio_data: 'base64...'
}))

// 结束评测
ws.send(JSON.stringify({
    action: 'end'
}))
```

详细说明请查看 [WEBSOCKET_VERSION.md](WEBSOCKET_VERSION.md)

## 🔒 安全说明

- ⚠️ **不要将密钥提交到 Git 仓库**
- ⚠️ **生产环境建议使用临时密钥或后端代理**
- ⚠️ **定期轮换密钥以保证安全**
- ⚠️ **使用 HTTPS/WSS 加密传输**

## 📊 评分说明

- **综合得分** - 整体发音质量评分（0-100）
- **准确度** - 发音准确性（0-100）
- **流畅度** - 语音流畅程度（0-100）
- **完整度** - 内容完整性（0-100）

## 🐛 常见问题

### 1. 麦克风权限被拒绝

确保浏览器已允许麦克风权限，HTTPS 或 localhost 环境下可用。

### 2. 评测返回错误

- 检查 SecretId 和 SecretKey 是否正确
- 确认腾讯云账户已开通智聆口语评测服务
- 查看控制台错误信息

### 3. WebSocket 连接失败

- 确认使用了正确的启动脚本 `app_websocket.py`
- 检查端口 5000 是否被占用
- 查看后端日志

## 📚 参考文档

- [腾讯云智聆口语评测 API 文档](https://cloud.tencent.com/document/product/1774)
- [WebSocket 版本详细说明](WEBSOCKET_VERSION.md)
- [Flask 文档](https://flask.palletsprojects.com/)
- [WebSocket API](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket)

## 🎯 使用建议

### HTTP 版本适用于：
- ✅ 短句评测（<10秒）
- ✅ 简单场景
- ✅ 快速原型开发

### WebSocket 版本适用于：
- ✅ 实时对话评测
- ✅ 长段落评测
- ✅ 需要即时反馈的场景

## 📄 开源协议

MIT License

## 👥 贡献

欢迎提交 Issue 和 Pull Request！

## 📮 联系方式

- GitHub: [@vincent860371](https://github.com/vincent860371)
- 项目地址: https://github.com/vincent860371/pronunciation-evaluation

---

⭐ 如果这个项目对您有帮助，请给个 Star！
