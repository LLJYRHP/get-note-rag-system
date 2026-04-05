# 创建桌面快捷方式脚本
$targetPath = "d:\销售\.trae\Get笔记学习系统\start_system.bat"
$shortcutPath = "$env:USERPROFILE\Desktop\健医融合·科学健康管理系统.lnk"

# 检查目标文件是否存在
if (Test-Path $targetPath) {
    # 创建 WScript.Shell 对象
    $WScriptShell = New-Object -ComObject WScript.Shell
    
    # 创建快捷方式
    $shortcut = $WScriptShell.CreateShortcut($shortcutPath)
    $shortcut.TargetPath = $targetPath
    $shortcut.WorkingDirectory = "d:\销售\.trae\Get笔记学习系统"
    $shortcut.Description = "启动健医融合·科学健康管理系统"
    $shortcut.IconLocation = "$targetPath"
    $shortcut.Save()
    
    Write-Host "快捷方式已创建到桌面：$shortcutPath"
} else {
    Write-Host "错误：目标文件不存在：$targetPath"
}
