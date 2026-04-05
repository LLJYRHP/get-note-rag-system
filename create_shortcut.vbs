' 创建桌面快捷方式脚本
Set WshShell = CreateObject("WScript.Shell")

' 目标文件路径
TargetPath = "d:\销售\.trae\Get笔记学习系统\start_system.bat"

' 桌面快捷方式路径
DesktopPath = WshShell.SpecialFolders("Desktop")
ShortcutPath = DesktopPath & "\健医融合·科学健康管理系统.lnk"

' 创建快捷方式
Set Shortcut = WshShell.CreateShortcut(ShortcutPath)
Shortcut.TargetPath = TargetPath
Shortcut.WorkingDirectory = "d:\销售\.trae\Get笔记学习系统"
Shortcut.Description = "启动健医融合·科学健康管理系统"
Shortcut.Save

' 显示创建成功信息
MsgBox "Shortcut created on desktop: " & ShortcutPath, vbInformation, "Create Shortcut"
