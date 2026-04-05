@echo off
chcp 65001 >nul
echo ========================================
echo   启动健医融合·科学健康管理系统
echo ========================================
echo.
echo 正在启动...
echo.

rem 设置 Python 路径
set PYTHON_PATH=C:\Users\30314\python-sdk\python3.13.2\python.exe

rem 启动 Streamlit 应用
%PYTHON_PATH% -m streamlit run app.py --server.port 8502

echo.
echo 系统已关闭。
pause
