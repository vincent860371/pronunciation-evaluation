@echo off
chcp 65001 >nul
echo ========================================
echo 启动 HTTP 版本口语评测服务
echo ========================================
echo.

cd /d "%~dp0"

if not exist "venv\Scripts\activate.bat" (
    echo [错误] 虚拟环境不存在，请先运行 setup.bat
    pause
    exit /b 1
)

call venv\Scripts\activate.bat

echo [信息] 正在启动 HTTP 版本服务...
echo [信息] 访问地址: http://localhost:5000
echo.
python app.py

pause

