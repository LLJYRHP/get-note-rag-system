@echo off
chcp 65001 >nul
echo 启动健医融合·科学健康管理系统...

rem 使用与手动启动相同的命令格式
"C:\Users\30314\python-sdk\python3.13.2\python.exe" -m streamlit run "d:\销售\.trae\Get笔记学习系统\app.py" --server.port 8502

echo 系统已关闭。
pause