# 英文口语评测系统 - 腾讯智聆 (WebSocket 实时版)

基于腾讯云智聆口语评测（SOE）**WebSocket API** 开发的英文口语评测 Web 应用，支持**实时流式评测**，提供发音准确度、流畅度和完整度等多维度评分。

## ✨ 功能特性

- 🎤 **实时录音评测** - 支持浏览器麦克风录音
- ⚡ **WebSocket 实时流式** - 边说边评，即时反馈
- 📊 **多维度评分** - 综合得分、准确度、流畅度、完整度
- 🎯 **多种评测模式** - 词模式、句子模式、段落模式、自由说模式
- 🎨 **现代化界面** - 深色主题，流畅动画效果
- 📱 **响应式设计** - 支持各种设备访问

## 🚀 快速开始

### 环境要求

- Python 3.7+
- 现代浏览器（Chrome/Firefox/Edge 等）
- 腾讯云账号（需要 SecretId 和 SecretKey）

### 一键安装（Windows）

双击运行 `setup.bat`，按提示完成环境配置。

### 手动安装

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
```bash
pip install -r requirements.txt
```

5. **启动服务**

Windows:
```bash
start.bat
```

或手动启动:
```bash
python app.py
```

6. **访问应用**

打开浏览器访问：http://localhost:5000

## 📋 WebSocket 技术优势

| 特性 | WebSocket 版本 |
|------|----------------|
| **实时反馈** | ✅ 边说边评 |
| **延迟** | 低 |
| **连接方式** | 长连接 |
| **流式传输** | ✅ |
| **用户体验** | 优秀 |
| **适用场景** | 实时对话评测 |

## 📁 项目结构

```
pronunciation-evaluation/
├── venv/                   # 虚拟环境
├── app.py                  # WebSocket 后端服务
├── index.html              # 前端页面
├── requirements.txt        # 项目依赖
├── setup.bat               # 一键安装脚本 (Windows)
├── start.bat               # 启动脚本 (Windows)
├── README.md               # 项目说明文档
├── WEBSOCKET_VERSION.md    # WebSocket 详细说明
├── GITHUB_SETUP.md         # GitHub 部署指南
├── image.png               # 接口文档截图
└── .gitignore              # Git 忽略文件
```

## 📝 使用说明

### 1. 获取腾讯云密钥

访问 [腾讯云控制台](https://console.cloud.tencent.com/capi) 获取：
- **SecretId** - API 调用者身份标识
- **SecretKey** - 签名密钥

⚠️ **注意**：请确保已开通 [智聆口语评测服务](https://console.cloud.tencent.com/soe)

### 2. 配置密钥

在网页中填写您的 SecretId 和 SecretKey

### 3. 开始评测

1. 选择评测模式和评分系数
2. 输入要朗读的英文文本
3. 点击"开始录音评测"并朗读
4. 实时查看评测结果
5. 点击"停止评测"获取最终结果

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

根据腾讯云 WebSocket 接口规范：

- **采样率**: 16000Hz
- **采样精度**: 16bits
- **声道**: 单声道 (mono)
- **格式**: PCM, WAV, MP3, Speex
- **数据发送**: 建议每 40ms 发送 40ms 时长的音频数据

## 🔧 技术栈

### 后端
- **Flask** - Python Web 框架
- **Flask-Sock** - WebSocket 支持
- **tencentcloud-sdk-python** - 腾讯云 SDK
- **websocket-client** - WebSocket 客户端

### 前端
- **原生 JavaScript** - 无框架依赖
- **WebSocket API** - 浏览器实时通信
- **WebRTC API** - 浏览器录音
- **CSS3** - 现代化样式和动画

## 📄 WebSocket API 接口

### 连接地址

```
ws://localhost:5000/ws/evaluate
```

### 消息格式

**1. 开始评测**
```json
{
  "action": "start",
  "secret_id": "your_secret_id",
  "secret_key": "your_secret_key",
  "ref_text": "Hello, how are you today?",
  "eval_mode": 1,
  "score_coeff": 1.5
}
```

**2. 发送音频数据**
```json
{
  "action": "audio",
  "audio_data": "base64_encoded_audio_chunk"
}
```

**3. 结束评测**
```json
{
  "action": "end"
}
```

### 返回消息

**连接成功**
```json
{
  "code": 0,
  "message": "连接成功",
  "voice_id": "uuid-string"
}
```

**实时评测结果**
```json
{
  "code": 0,
  "result": {
    "overall": 85.5,
    "phone_score": 88.0,
    "fluency_score": 82.0,
    "integrity_score": 86.0
  }
}
```

**最终结果**
```json
{
  "code": 0,
  "result": {
    "overall": 85.5,
    "phone_score": 88.0,
    "fluency_score": 82.0,
    "integrity_score": 86.0,
    "words": [...]
  },
  "final": 1
}
```

详细说明请查看 [WEBSOCKET_VERSION.md](WEBSOCKET_VERSION.md)

## 🔒 安全说明

- ⚠️ **不要将密钥提交到 Git 仓库**
- ⚠️ **生产环境建议使用临时密钥或后端代理**
- ⚠️ **定期轮换密钥以保证安全**
- ⚠️ **生产环境使用 HTTPS/WSS 加密传输**

## 📊 评分说明

- **综合得分 (overall)** - 整体发音质量评分（0-100）
- **准确度 (phone_score)** - 发音准确性（0-100）
- **流畅度 (fluency_score)** - 语音流畅程度（0-100）
- **完整度 (integrity_score)** - 内容完整性（0-100）

## 🔄 工作流程

```
用户浏览器 ←→ Flask WebSocket ←→ 腾讯云 WebSocket API
     ↓              ↓                    ↓
   录音         转发数据            实时评测
     ↓              ↓                    ↓
  显示结果    ← 推送结果 ←          返回评分
```

## 🐛 常见问题

### 1. 麦克风权限被拒绝

确保浏览器已允许麦克风权限，HTTPS 或 localhost 环境下可用。

### 2. WebSocket 连接失败

- 确认服务已正常启动
- 检查端口 5000 是否被占用
- 查看浏览器控制台和后端日志

### 3. 评测返回错误

- 检查 SecretId 和 SecretKey 是否正确
- 确认腾讯云账户已开通智聆口语评测服务
- 检查账户余额是否充足

### 4. 音频质量差

- 调整麦克风位置
- 在安静环境下录音
- 检查采样率设置（16000Hz）

## 📚 参考文档

- [腾讯云智聆口语评测 WebSocket API](https://cloud.tencent.com/document/product/1774/107497)
- [WebSocket 版本详细说明](WEBSOCKET_VERSION.md)
- [Flask-Sock 文档](https://flask-sock.readthedocs.io/)
- [WebSocket API (MDN)](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket)

## 🎯 适用场景

✅ **推荐使用场景**：
- 实时对话评测
- 长段落评测
- 需要即时反馈的教学场景
- 在线英语口语练习
- 发音纠正训练

## 📄 开源协议

MIT License

## 👥 贡献

欢迎提交 Issue 和 Pull Request！

## 📮 联系方式

- GitHub: [@vincent860371](https://github.com/vincent860371)
- 项目地址: https://github.com/vincent860371/pronunciation-evaluation

---

⭐ 如果这个项目对您有帮助，请给个 Star！

🎤 实时流式评测，边说边评，体验更佳！
