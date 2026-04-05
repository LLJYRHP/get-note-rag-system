@echo off
chcp 65001 >nul
echo 检查Python路径...

if exist "C:\Users\30314\python-sdk\python3.13.2\python.exe" (
    echo Python路径存在: C:\Users\30314\python-sdk\python3.13.2\python.exe
) else (
    echo Python路径不存在: C:\Users\30314\python-sdk\python3.13.2\python.exe
)

pause