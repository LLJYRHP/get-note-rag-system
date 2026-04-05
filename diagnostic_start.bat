@echo off
chcp 65001 >nul
echo ========================================
echo   健医融合·科学健康管理系统诊断启动器
 echo ========================================
echo.
echo 正在诊断系统环境...
echo.

rem 检查当前目录
echo 当前目录: %cd%
echo.

rem 检查Python是否存在
echo 检查Python路径...
if exist "C:\Users\30314\python-sdk\python3.13.2\python.exe" (
    echo ✓ Python 可执行文件存在
    echo Python路径: C:\Users\30314\python-sdk\python3.13.2\python.exe
) else (
    echo × Python 可执行文件不存在
    echo 路径: C:\Users\30314\python-sdk\python3.13.2\python.exe
    pause
    exit /b 1
)

echo.
echo 检查app.py文件...
if exist "app.py" (
    echo ✓ app.py 文件存在
) else (
    echo × app.py 文件不存在
    pause
    exit /b 1
)

echo.
echo 正在启动应用...
echo 命令: "C:\Users\30314\python-sdk\python3.13.2\python.exe" -m streamlit run app.py --server.port 8502
echo.

rem 运行应用
"C:\Users\30314\python-sdk\python3.13.2\python.exe" -m streamlit run app.py --server.port 8502

rem 检查退出码
if %errorlevel% neq 0 (
    echo.
    echo × 启动失败！错误码: %errorlevel%
    echo 请检查上述错误信息
    pause
    exit /b %errorlevel%
)

echo.
echo ✓ 启动成功！
echo 系统已关闭。
pause