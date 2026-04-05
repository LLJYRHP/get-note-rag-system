Write-Host "启动健医融合·科学健康管理系统..." -ForegroundColor Green

# 设置绝对路径
$pythonPath = "C:\Users\30314\python-sdk\python3.13.2\python.exe"
$appPath = "d:\销售\.trae\Get笔记学习系统\app.py"

# 检查文件是否存在
if (-not (Test-Path $pythonPath)) {
    Write-Host "错误: Python可执行文件不存在: $pythonPath" -ForegroundColor Red
    Read-Host "按 Enter 键退出..."
    exit 1
}

if (-not (Test-Path $appPath)) {
    Write-Host "错误: app.py文件不存在: $appPath" -ForegroundColor Red
    Read-Host "按 Enter 键退出..."
    exit 1
}

Write-Host "Python路径: $pythonPath" -ForegroundColor Cyan
Write-Host "App路径: $appPath" -ForegroundColor Cyan

# 启动应用
Write-Host "正在启动应用..." -ForegroundColor Yellow
try {
    & $pythonPath -m streamlit run $appPath --server.port 8502
} catch {
    Write-Host "启动失败！错误信息: $($_.Exception.Message)" -ForegroundColor Red
    Read-Host "按 Enter 键退出..."
    exit 1
}

Write-Host "系统已关闭。" -ForegroundColor Green
Read-Host "按 Enter 键退出..."