@echo off

echo 检测Python安装状态...
echo =====================

REM 检查Python是否存在
where python >nul 2>&1
if %errorlevel% equ 0 (
    echo Python已安装
    echo Python版本：
    python --version
    echo Python路径：
    where python
) else (
    echo Python未安装
    echo 请安装Python 3.8或更高版本
)

echo =====================
echo 检测完成
pause
