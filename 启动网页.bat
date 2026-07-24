@echo off
chcp 65001 >nul
title mdtoolkit 在线体验

echo ============================================
echo   mdtoolkit 网页版启动中，请稍候...
echo ============================================
echo.

cd /d "%~dp0"

REM 检查 flask 是否已安装，没装就自动安装
python -c "import flask" 2>nul
if errorlevel 1 (
    echo 首次运行，正在安装依赖 flask，请稍候...
    python -m pip install flask
    echo.
)

echo 正在启动服务，浏览器马上自动打开。
echo 用完直接关闭这个黑窗口即可停止。
echo.

python web_api.py

pause
