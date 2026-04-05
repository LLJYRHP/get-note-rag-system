@echo off
chcp 65001 >nul
echo ========================================
echo   启动健医融合·科学健康管理系统
echo ========================================
echo.
echo 正在启动...
echo.
"C:\Users\30314\python-sdk\python3.13.2\python.exe" -m streamlit run app.py --server.port 8502
echo.
echo 系统已关闭。
pause