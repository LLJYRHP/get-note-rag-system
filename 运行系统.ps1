# 启动 Get 笔记 RAG 问答系统
Write-Host "========================================"
Write-Host "  启动 Get 笔记 RAG 问答系统"
Write-Host "========================================"
Write-Host ""

# 切换到脚本所在目录
Set-Location -Path $PSScriptRoot
Write-Host "正在启动 Streamlit 应用..."
Write-Host ""

# 检查虚拟环境是否存在
if (Test-Path ".env\Scripts\python.exe") {
    Write-Host "使用虚拟环境启动..."
    & ".env\Scripts\python.exe" -m streamlit run app.py
} else {
    Write-Host "使用系统 Python 启动..."
    # 使用用户提供的 Python 路径
    $pythonPath = "C:\Users\30314\python-sdk\python3.13.2\python.exe"
    if (Test-Path $pythonPath) {
        Write-Host "使用指定的 Python 路径: $pythonPath"
        & $pythonPath -m streamlit run app.py
    } else {
        Write-Host "使用默认 Python..."
        python -m streamlit run app.py
    }
}

Write-Host ""
Write-Host "应用已关闭。"
Read-Host "按 Enter 键继续..."
