# WebSocket 版本使用说明

## 🆕 新版本特性

基于腾讯云智聆口语评测 WebSocket API 开发，相比 HTTP 版本有以下优势：

### ✨ 主要特性

1. **实时流式评测** - 边说边评，实时返回评测结果
2. **更低延迟** - WebSocket 双向通信，响应更快
3. **更好的用户体验** - 实时反馈，无需等待录音结束
4. **持续连接** - 减少连接建立开销

## 📋 技术规格

### WebSocket 接口要求

- **协议**: WSS (WebSocket Secure)
- **端点**: `wss://soe.cloud.tencent.com/soe/api/`
- **音频格式**: PCM, WAV, MP3, Speex
- **音频属性**:
  - 采样率: 16000Hz
  - 采样精度: 16bits
  - 声道: 单声道 (mono)
- **数据发送**: 建议每 40ms 发送 40ms 时长的音频数据

### 接口调用流程

```
1. 客户端主动发起 WebSocket 连接请求
2. 连接建立后，开始发送音频数据
3. 服务端实时返回评测结果 (JSON 格式)
4. 发送结束标记，获取最终完整结果
```

## 🚀 快速开始

### 1. 安装依赖

```bash
# 激活虚拟环境
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 安装 WebSocket 版本依赖
pip install -r requirements_websocket.txt
```

### 2. 启动服务

```bash
python app_websocket.py
```

### 3. 访问应用

打开浏览器访问：http://localhost:5000

WebSocket 地址：`ws://localhost:5000/ws/evaluate`

## 📁 文件说明

### WebSocket 版本文件

- `app_websocket.py` - WebSocket 后端服务
- `index_websocket.html` - WebSocket 前端页面
- `requirements_websocket.txt` - WebSocket 版本依赖

### 原 HTTP 版本文件（保留）

- `app.py` - HTTP REST API 服务
- `index.html` - HTTP 版本前端页面
- `requirements.txt` - HTTP 版本依赖

## 🔄 工作流程

### 前端流程

```javascript
1. 连接 WebSocket
   ws = new WebSocket('ws://localhost:5000/ws/evaluate')

2. 发送开始评测指令
   ws.send(JSON.stringify({
       action: 'start',
       secret_id: '...',
       secret_key: '...',
       ref_text: 'Hello world',
       eval_mode: 1,
       score_coeff: 1.5
   }))

3. 持续发送音频数据
   ws.send(JSON.stringify({
       action: 'audio',
       audio_data: 'base64_encoded_audio'
   }))

4. 发送结束标记
   ws.send(JSON.stringify({
       action: 'end'
   }))

5. 接收评测结果
   ws.onmessage = (event) => {
       const data = JSON.parse(event.data)
       // 处理实时结果和最终结果
   }
```

### 后端流程

```python
1. 接收前端 WebSocket 连接
2. 连接到腾讯云 WebSocket API
3. 转发音频数据到腾讯云
4. 接收腾讯云评测结果
5. 实时推送结果到前端
6. 评测完成后关闭连接
```

## 📊 消息格式

### 前端 → 后端

**开始评测**
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

**发送音频**
```json
{
  "action": "audio",
  "audio_data": "base64_encoded_audio_chunk"
}
```

**结束评测**
```json
{
  "action": "end"
}
```

### 后端 → 前端

**连接成功**
```json
{
  "code": 0,
  "message": "连接成功",
  "voice_id": "uuid-string"
}
```

**实时结果**
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

**错误信息**
```json
{
  "code": -1,
  "message": "错误描述"
}
```

## ⚙️ 配置说明

### 音频参数

```python
# 音频格式配置
audio_config = {
    'sampleRate': 16000,      # 16kHz 采样率
    'channelCount': 1,        # 单声道
    'echoCancellation': True, # 回声消除
    'noiseSuppression': True  # 噪声抑制
}
```

### 评测参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `engine_model_type` | String | `16k_en` (英文) / `16k_zh` (中文) |
| `eval_mode` | Integer | 0=词模式, 1=句子, 2=段落, 3=自由说 |
| `score_coeff` | Float | 1.0-4.0，评分宽松度 |
| `voice_format` | Integer | 1=PCM, 2=WAV, 3=MP3, 4=Speex |
| `needvad` | Integer | 0=不需要, 1=需要语音检测 |

## 🔍 调试技巧

### 1. 查看 WebSocket 连接状态

打开浏览器开发者工具 → Network → WS，可以查看 WebSocket 消息流

### 2. 后端日志

后端会打印详细的连接和消息日志：

```
[2025-12-15 00:00:00] 新的 WebSocket 连接
[2025-12-15 00:00:01] 收到动作: start
[2025-12-15 00:00:02] WebSocket 连接已建立
[2025-12-15 00:00:03] 收到消息: 0
[2025-12-15 00:00:10] 收到最终结果，准备关闭连接
```

### 3. 常见问题

**问题1: WebSocket 连接失败**
- 检查后端服务是否正常运行
- 确认端口 5000 未被占用
- 查看浏览器控制台错误信息

**问题2: 没有收到评测结果**
- 确认腾讯云密钥正确
- 检查音频格式是否符合要求
- 查看后端日志是否有错误

**问题3: 音频质量差**
- 调整麦克风位置
- 在安静环境下录音
- 检查采样率设置

## 📚 参考文档

- [腾讯云智聆口语评测 WebSocket API](https://cloud.tencent.com/document/product/1774/107497)
- [WebSocket API (MDN)](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket)
- [Flask-Sock 文档](https://flask-sock.readthedocs.io/)

## 🆚 版本对比

| 特性 | HTTP 版本 | WebSocket 版本 |
|------|-----------|----------------|
| 实时反馈 | ❌ | ✅ |
| 延迟 | 较高 | 低 |
| 连接复用 | ❌ | ✅ |
| 流式传输 | ❌ | ✅ |
| 实现复杂度 | 简单 | 中等 |
| 适用场景 | 短音频 | 实时对话 |

## 💡 使用建议

1. **短句评测** - 使用 HTTP 版本更简单
2. **实时对话** - 使用 WebSocket 版本体验更好
3. **生产环境** - 建议使用 HTTPS/WSS 加密传输
4. **音频质量** - 确保在安静环境下录音

---

⭐ WebSocket 版本提供更好的实时体验，推荐使用！

