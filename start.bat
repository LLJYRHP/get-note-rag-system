@echo off

REM 启动脚本 - Get笔记RAG问答系统

REM 检查Python是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: 未找到Python，请先安装Python 3.8+
    pause
    exit /b 1
)

REM 检查pip是否安装
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: 未找到pip，请确保Python安装正确
    pause
    exit /b 1
)

REM 安装依赖
 echo 正在安装依赖...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo 错误: 依赖安装失败
    pause
    exit /b 1
)

REM 检查环境变量文件
if not exist .env (
    echo 错误: .env文件不存在，请根据.env.example创建.env文件并配置API_KEY和KB_ID
    pause
    exit /b 1
)

REM 启动Streamlit应用
echo 正在启动Streamlit应用...
streamlit run app.py

pause
