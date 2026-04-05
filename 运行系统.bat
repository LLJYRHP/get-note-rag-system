@echo off
chcp 65001 >nul
echo ========================================
echo   启动 Get 笔记 RAG 问答系统
echo ========================================
echo.
cd /d %~dp0
echo 正在启动 Streamlit 应用...
echo.
if exist .env\Scripts\python.exe (
    echo 使用虚拟环境启动...
    .env\Scripts\python.exe -m streamlit run app.py
) else (
    echo 使用系统 Python 启动...
    python -m streamlit run app.py
)
echo.
echo 应用已关闭。
pause
