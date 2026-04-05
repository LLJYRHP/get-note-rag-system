Write-Host "启动健医融合·科学健康管理系统..."

# 使用绝对路径启动Python
$pythonPath = "C:\Users\30314\python-sdk\python3.13.2\python.exe"
$appPath = "d:\销售\.trae\Get笔记学习系统\app.py"

try {
    & $pythonPath -m streamlit run $appPath --server.port 8502
} catch {
    Write-Host "启动失败！错误信息: $($_.Exception.Message)"
    Read-Host "按 Enter 键继续..."
    exit 1
}

Write-Host "系统已关闭。"
Read-Host "按 Enter 键继续..."