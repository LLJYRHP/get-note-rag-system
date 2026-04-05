@echo off
echo 启动健医融合·科学健康管理系统...

rem 使用绝对路径启动Python
"C:\Users\30314\python-sdk\python3.13.2\python.exe" -m streamlit run "d:\销售\.trae\Get笔记学习系统\app.py" --server.port 8502

if errorlevel 1 (
    echo 启动失败！请检查错误信息
    pause
    exit /b 1
)

echo 系统已关闭。
pause