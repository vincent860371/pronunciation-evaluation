# -*- coding: utf-8 -*-
"""
英文口语评测服务 - 基于腾讯智聆
"""

import base64
import json
import os
import uuid
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.soe.v20180724 import soe_client, models

app = Flask(__name__, static_folder='.')
CORS(app)

# 配置信息（可通过环境变量或直接填写）
SECRET_ID = os.environ.get('TENCENT_SECRET_ID', '')
SECRET_KEY = os.environ.get('TENCENT_SECRET_KEY', '')


@app.route('/')
def index():
    """返回前端页面"""
    return send_from_directory('.', 'index.html')


@app.route('/evaluate', methods=['POST'])
def evaluate():
    """口语评测接口"""
    try:
        data = request.json
        
        # 获取参数
        secret_id = data.get('secret_id') or SECRET_ID
        secret_key = data.get('secret_key') or SECRET_KEY
        ref_text = data.get('ref_text', '')
        audio_data = data.get('audio_data', '')  # base64编码的音频数据
        eval_mode = int(data.get('eval_mode', 1))
        score_coeff = float(data.get('score_coeff', 1.5))
        
        if not secret_id or not secret_key:
            return jsonify({'error': '请配置腾讯云密钥'}), 400
        
        if not audio_data:
            return jsonify({'error': '音频数据不能为空'}), 400
        
        if not ref_text and eval_mode != 3:
            return jsonify({'error': '评测文本不能为空'}), 400
        
        # 创建腾讯云认证
        cred = credential.Credential(secret_id, secret_key)
        
        # 配置HTTP请求
        http_profile = HttpProfile()
        http_profile.endpoint = "soe.tencentcloudapi.com"
        
        # 配置客户端
        client_profile = ClientProfile()
        client_profile.httpProfile = http_profile
        
        # 创建SOE客户端
        client = soe_client.SoeClient(cred, "", client_profile)
        
        # 创建评测请求
        req = models.TransmitOralProcessWithInitRequest()
        
        # 生成唯一会话ID (UUID格式)
        session_id = str(uuid.uuid4())
        
        # 设置评测参数
        req.SessionId = session_id  # 必传参数，用于标识语音段的唯一性
        req.SeqId = 1
        req.IsEnd = 1
        req.VoiceFileType = 3  # mp3格式
        req.VoiceEncodeType = 1  # 音频编码类型
        req.UserVoiceData = audio_data  # base64编码的音频
        req.RefText = ref_text
        req.WorkMode = 0  # 流式评测
        req.EvalMode = eval_mode
        req.ScoreCoeff = score_coeff
        req.ServerType = 0  # 0=英文(默认), 1=中文
        req.TextMode = 0
        req.SentenceInfoEnabled = 1
        
        # 发起评测请求
        resp = client.TransmitOralProcessWithInit(req)
        
        # 解析响应
        result = json.loads(resp.to_json_string())
        
        return jsonify({
            'success': True,
            'data': result
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/init_evaluate', methods=['POST'])
def init_evaluate():
    """初始化评测会话"""
    try:
        data = request.json
        
        secret_id = data.get('secret_id') or SECRET_ID
        secret_key = data.get('secret_key') or SECRET_KEY
        ref_text = data.get('ref_text', '')
        eval_mode = int(data.get('eval_mode', 1))
        score_coeff = float(data.get('score_coeff', 1.5))
        session_id = data.get('session_id', '')
        
        if not secret_id or not secret_key:
            return jsonify({'error': '请配置腾讯云密钥'}), 400
        
        # 创建腾讯云认证
        cred = credential.Credential(secret_id, secret_key)
        
        http_profile = HttpProfile()
        http_profile.endpoint = "soe.tencentcloudapi.com"
        
        client_profile = ClientProfile()
        client_profile.httpProfile = http_profile
        
        client = soe_client.SoeClient(cred, "", client_profile)
        
        # 创建初始化请求
        req = models.InitOralProcessRequest()
        req.SessionId = session_id
        req.RefText = ref_text
        req.WorkMode = 0
        req.EvalMode = eval_mode
        req.ScoreCoeff = score_coeff
        req.ServerType = 0  # 0=英文, 1=中文
        req.TextMode = 0
        req.SentenceInfoEnabled = 1
        
        resp = client.InitOralProcess(req)
        result = json.loads(resp.to_json_string())
        
        return jsonify({
            'success': True,
            'data': result
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


if __name__ == '__main__':
    print("=" * 50)
    print("英文口语评测服务已启动")
    print("访问地址: http://localhost:5000")
    print("=" * 50)
    app.run(host='0.0.0.0', port=5000, debug=True)

