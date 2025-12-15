# 英文口语评测系统 - 腾讯智聆

基于腾讯云智聆口语评测（SOE）API 开发的英文口语评测 Web 应用，支持实时录音评测，提供发音准确度、流畅度和完整度等多维度评分。

## ✨ 功能特性

- 🎤 **实时录音评测** - 支持浏览器麦克风录音
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
git clone https://github.com/你的用户名/语音评测-腾讯智聆.git
cd 语音评测-腾讯智聆
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
```bash
python app.py
```

6. **访问应用**

打开浏览器访问：http://localhost:5000

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
4. 点击"停止并评测"获取结果

## 📁 项目结构

```
语音评测-腾讯智聆/
├── venv/              # 虚拟环境（不提交到 Git）
├── app.py             # Flask 后端服务
├── index.html         # 前端页面
├── requirements.txt   # Python 依赖
├── README.md          # 腾讯云 SDK 文档
├── README_PROJECT.md  # 项目说明文档
└── .gitignore         # Git 忽略文件
```

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

## 🔧 技术栈

### 后端
- **Flask** - Python Web 框架
- **Flask-CORS** - 跨域资源共享
- **tencentcloud-sdk-python** - 腾讯云 SDK

### 前端
- **原生 JavaScript** - 无框架依赖
- **WebRTC** - 浏览器录音 API
- **CSS3** - 现代化样式和动画

## 📄 API 接口

### POST /evaluate

评测音频接口

**请求参数：**
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

**响应示例：**
```json
{
  "success": true,
  "data": {
    "SuggestedScore": 85.5,
    "PronAccuracy": 88.0,
    "PronFluency": 82.0,
    "PronCompletion": 86.0,
    "Words": [...]
  }
}
```

## 🔒 安全说明

- ⚠️ **不要将密钥提交到 Git 仓库**
- ⚠️ **生产环境建议使用临时密钥或后端代理**
- ⚠️ **定期轮换密钥以保证安全**

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

### 3. 音频格式问题

浏览器录制的音频会自动转换为 base64 格式发送。

## 📚 参考文档

- [腾讯云智聆口语评测 API 文档](https://cloud.tencent.com/document/product/1774)
- [Flask 文档](https://flask.palletsprojects.com/)
- [WebRTC API](https://developer.mozilla.org/en-US/docs/Web/API/WebRTC_API)

## 📄 开源协议

MIT License

## 👥 贡献

欢迎提交 Issue 和 Pull Request！

## 📮 联系方式

如有问题，请提交 GitHub Issue。

---

⭐ 如果这个项目对您有帮助，请给个 Star！

