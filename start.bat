@echo off
chcp 65001 >nul
title Get 笔记 RAG 问答系统启动器

echo ========================================
echo   Get 笔记 RAG 问答系统启动器
echo ========================================
echo.
echo 正在启动应用...
echo.

REM 获取当前脚本所在目录
set "CURRENT_DIR=%~dp0"

REM 检查 Python 是否存在
if exist "C:\Users\30314\python-sdk\python3.13.2\python.exe" (
    echo ✓ Python 已检测到
    cd /d "%CURRENT_DIR%"
    echo 当前目录：%CD%
    "C:\Users\30314\python-sdk\python3.13.2\python.exe" -m streamlit run app.py --server.port 8502
) else (
    echo × 未找到 Python
    echo 请确保已安装 Python 3.13.2
    echo Python 路径：C:\Users\30314\python-sdk\python3.13.2\python.exe
    pause
    exit /b 1
)

echo.
echo ========================================
echo 应用已关闭
echo ========================================
pause
