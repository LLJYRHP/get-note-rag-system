@echo off
chcp 65001 >nul
echo 启动健医融合·科学健康管理系统...

rem 检查Python是否存在
if exist "C:\Users\30314\python-sdk\python3.13.2\python.exe" (
    echo Python路径正确
    "C:\Users\30314\python-sdk\python3.13.2\python.exe" -m streamlit run app.py --server.port 8502
) else (
    echo Python路径不存在
    pause
    exit /b 1
)

echo 系统已关闭。
pause