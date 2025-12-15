@echo off
chcp 65001 >nul
echo ========================================
echo 英文口语评测系统 - 腾讯智聆
echo WebSocket 实时流式评测
echo ========================================
echo.

cd /d "%~dp0"

if not exist "venv\Scripts\activate.bat" (
    echo [错误] 虚拟环境不存在，请先运行 setup.bat
    pause
    exit /b 1
)

call venv\Scripts\activate.bat

echo [信息] 正在检查 WebSocket 依赖...
pip show flask-sock >nul 2>&1
if errorlevel 1 (
    echo [信息] 安装 WebSocket 依赖...
    pip install flask-sock websocket-client
)

echo [信息] 正在启动服务...
echo [信息] 访问地址: http://localhost:5000
echo [信息] WebSocket: ws://localhost:5000/ws/evaluate
echo.
python app.py

pause

