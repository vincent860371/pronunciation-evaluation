# -*- coding: utf-8 -*-
"""
英文口语评测服务 - WebSocket 版本
基于腾讯云智聆口语评测 WebSocket API
"""

import asyncio
import base64
import json
import os
import uuid
import hmac
import hashlib
import time
from datetime import datetime
from urllib.parse import urlencode
from flask import Flask, render_template, send_from_directory
from flask_sock import Sock
import websocket
import threading

app = Flask(__name__, static_folder='.')
sock = Sock(app)

# 配置信息
SECRET_ID = os.environ.get('TENCENT_SECRET_ID', '')
SECRET_KEY = os.environ.get('TENCENT_SECRET_KEY', '')


def generate_signature(secret_id, secret_key, params):
    """生成腾讯云 API 签名"""
    # 拼接签名原文字符串
    sign_str = "POST" + "soe.cloud.tencent.com/soe/api/" + "?"
    
    # 对参数排序
    sorted_params = sorted(params.items())
    sign_str += urlencode(sorted_params)
    
    # 计算签名
    sign = hmac.new(
        secret_key.encode('utf-8'),
        sign_str.encode('utf-8'),
        hashlib.sha1
    ).digest()
    
    signature = base64.b64encode(sign).decode('utf-8')
    return signature


class TencentSOEWebSocket:
    """腾讯云口语评测 WebSocket 客户端"""
    
    def __init__(self, secret_id, secret_key, params, callback):
        self.secret_id = secret_id
        self.secret_key = secret_key
        self.params = params
        self.callback = callback
        self.ws = None
        self.voice_id = str(uuid.uuid4())
        self.message_id = 0
        
    def connect(self):
        """连接到腾讯云 WebSocket 服务"""
        # 构建请求参数
        request_params = {
            'secretid': self.secret_id,
            'timestamp': str(int(time.time())),
            'expired': str(int(time.time()) + 24 * 60 * 60),
            'nonce': str(int(time.time() * 1000)),
            'engine_model_type': '16k_en',  # 英文引擎
            'voice_id': self.voice_id,
            'voice_format': '1',  # 1: pcm
            'needvad': '1',
        }
        
        # 添加评测参数
        if 'ref_text' in self.params:
            request_params['text'] = self.params['ref_text']
        if 'eval_mode' in self.params:
            request_params['eval_mode'] = str(self.params['eval_mode'])
        if 'score_coeff' in self.params:
            request_params['score_coeff'] = str(self.params['score_coeff'])
        
        # 生成签名
        signature = generate_signature(self.secret_id, self.secret_key, request_params)
        request_params['signature'] = signature
        
        # 构建 WebSocket URL
        url = f"wss://soe.cloud.tencent.com/soe/api/?{urlencode(request_params)}"
        
        # 连接 WebSocket
        self.ws = websocket.WebSocketApp(
            url,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
            on_open=self.on_open
        )
        
        # 在新线程中运行
        wst = threading.Thread(target=self.ws.run_forever)
        wst.daemon = True
        wst.start()
        
    def on_open(self, ws):
        """WebSocket 连接建立"""
        print(f"[{datetime.now()}] WebSocket 连接已建立")
        self.callback({
            'code': 0,
            'message': '连接成功',
            'voice_id': self.voice_id
        })
        
    def on_message(self, ws, message):
        """接收到消息"""
        try:
            data = json.loads(message)
            print(f"[{datetime.now()}] 收到消息: {data.get('code', 'unknown')}")
            
            # 发送给前端
            self.callback(data)
            
            # 如果是最终结果，关闭连接
            if data.get('final') == 1:
                print(f"[{datetime.now()}] 收到最终结果，准备关闭连接")
                
        except Exception as e:
            print(f"[{datetime.now()}] 解析消息失败: {str(e)}")
            self.callback({
                'code': -1,
                'message': f'解析消息失败: {str(e)}'
            })
    
    def on_error(self, ws, error):
        """连接错误"""
        print(f"[{datetime.now()}] WebSocket 错误: {error}")
        self.callback({
            'code': -1,
            'message': f'连接错误: {str(error)}'
        })
    
    def on_close(self, ws, close_status_code, close_msg):
        """连接关闭"""
        print(f"[{datetime.now()}] WebSocket 连接已关闭")
        self.callback({
            'code': 0,
            'message': '连接已关闭',
            'final': 1
        })
    
    def send_audio(self, audio_data):
        """发送音频数据"""
        if self.ws and self.ws.sock and self.ws.sock.connected:
            try:
                self.message_id += 1
                # 构建消息
                message = {
                    'voice_id': self.voice_id,
                    'message_id': str(self.message_id),
                    'voice_data': audio_data,  # base64 编码的音频数据
                }
                self.ws.send(json.dumps(message))
                return True
            except Exception as e:
                print(f"[{datetime.now()}] 发送音频失败: {str(e)}")
                return False
        return False
    
    def send_end(self):
        """发送结束标记"""
        if self.ws and self.ws.sock and self.ws.sock.connected:
            try:
                self.message_id += 1
                message = {
                    'voice_id': self.voice_id,
                    'message_id': str(self.message_id),
                    'final': 1
                }
                self.ws.send(json.dumps(message))
                print(f"[{datetime.now()}] 已发送结束标记")
                return True
            except Exception as e:
                print(f"[{datetime.now()}] 发送结束标记失败: {str(e)}")
                return False
        return False
    
    def close(self):
        """关闭连接"""
        if self.ws:
            self.ws.close()


# 存储活跃的 WebSocket 连接
active_connections = {}


@app.route('/')
def index():
    """返回前端页面"""
    return send_from_directory('.', 'index_websocket.html')


@sock.route('/ws/evaluate')
def websocket_evaluate(ws):
    """WebSocket 评测接口"""
    print(f"\n[{datetime.now()}] 新的 WebSocket 连接")
    
    tencent_ws = None
    session_id = str(uuid.uuid4())
    
    try:
        while True:
            message = ws.receive()
            
            if message is None:
                break
                
            data = json.loads(message)
            action = data.get('action')
            
            print(f"[{datetime.now()}] 收到动作: {action}")
            
            if action == 'start':
                # 开始评测
                secret_id = data.get('secret_id') or SECRET_ID
                secret_key = data.get('secret_key') or SECRET_KEY
                
                if not secret_id or not secret_key:
                    ws.send(json.dumps({
                        'code': -1,
                        'message': '请配置腾讯云密钥'
                    }))
                    continue
                
                params = {
                    'ref_text': data.get('ref_text', ''),
                    'eval_mode': data.get('eval_mode', 1),
                    'score_coeff': data.get('score_coeff', 1.5),
                }
                
                # 创建回调函数
                def callback(msg):
                    try:
                        ws.send(json.dumps(msg))
                    except Exception as e:
                        print(f"[{datetime.now()}] 发送消息到前端失败: {str(e)}")
                
                # 连接腾讯云 WebSocket
                tencent_ws = TencentSOEWebSocket(secret_id, secret_key, params, callback)
                tencent_ws.connect()
                active_connections[session_id] = tencent_ws
                
                # 等待连接建立
                time.sleep(0.5)
                
            elif action == 'audio':
                # 发送音频数据
                if tencent_ws:
                    audio_data = data.get('audio_data')
                    if audio_data:
                        success = tencent_ws.send_audio(audio_data)
                        if not success:
                            ws.send(json.dumps({
                                'code': -1,
                                'message': '发送音频数据失败'
                            }))
                else:
                    ws.send(json.dumps({
                        'code': -1,
                        'message': '请先开始评测'
                    }))
                    
            elif action == 'end':
                # 结束评测
                if tencent_ws:
                    tencent_ws.send_end()
                    time.sleep(1)  # 等待结果返回
                    tencent_ws.close()
                    if session_id in active_connections:
                        del active_connections[session_id]
                        
            elif action == 'stop':
                # 停止评测
                if tencent_ws:
                    tencent_ws.close()
                    if session_id in active_connections:
                        del active_connections[session_id]
                break
                
    except Exception as e:
        print(f"[{datetime.now()}] WebSocket 错误: {str(e)}")
        ws.send(json.dumps({
            'code': -1,
            'message': f'服务器错误: {str(e)}'
        }))
    finally:
        # 清理连接
        if tencent_ws:
            tencent_ws.close()
        if session_id in active_connections:
            del active_connections[session_id]
        print(f"[{datetime.now()}] WebSocket 连接关闭")


if __name__ == '__main__':
    print("=" * 50)
    print("英文口语评测服务已启动 (WebSocket 版本)")
    print("访问地址: http://localhost:5000")
    print("WebSocket 地址: ws://localhost:5000/ws/evaluate")
    print("=" * 50)
    app.run(host='0.0.0.0', port=5000, debug=True)

