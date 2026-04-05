' 创建桌面快捷方式的 VBScript
Set WshShell = CreateObject("WScript.Shell")
strDesktop = WshShell.SpecialFolders("Desktop")
Set oShellLink = WshShell.CreateShortcut(strDesktop & "\健医融合·科学健康管理系统.lnk")

' 设置快捷方式的目标路径
oShellLink.TargetPath = "d:\销售\.trae\Get笔记学习系统\start_app.bat"

' 设置快捷方式的工作目录
oShellLink.WorkingDirectory = "d:\销售\.trae\Get笔记学习系统"

' 设置快捷方式的描述
oShellLink.Description = "启动健医融合·科学健康管理系统"

' 保存快捷方式
oShellLink.Save

' 显示创建成功的消息
MsgBox "桌面快捷方式已创建成功！", vbInformation, "创建快捷方式"