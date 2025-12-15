@echo off
chcp 65001 >nul
echo ========================================
echo 英文口语评测系统 - 环境设置
echo ========================================
echo.

cd /d "%~dp0"

:: 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到 Python，请先安装 Python 3.7+
    pause
    exit /b 1
)

echo [1/4] 检测到 Python 版本:
python --version

:: 创建虚拟环境
if not exist "venv" (
    echo.
    echo [2/4] 正在创建虚拟环境...
    python -m venv venv
    echo [成功] 虚拟环境创建完成
) else (
    echo.
    echo [2/4] 虚拟环境已存在
)

:: 激活虚拟环境
echo.
echo [3/4] 正在激活虚拟环境...
call venv\Scripts\activate.bat

:: 安装依赖
echo.
echo [4/4] 正在安装依赖...
pip install -r requirements.txt
echo.
echo [成功] WebSocket 版本依赖安装完成
echo [提示] 使用 start.bat 启动服务

echo.
echo ========================================
echo 安装完成！
echo ========================================
pause

