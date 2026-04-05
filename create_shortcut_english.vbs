' Create desktop shortcut script
Set WshShell = CreateObject("WScript.Shell")

' Target file path
TargetPath = "d:\销售\.trae\Get笔记学习系统\start_system.bat"

' Desktop shortcut path
DesktopPath = WshShell.SpecialFolders("Desktop")
ShortcutPath = DesktopPath & "\Health Management System.lnk"

' Create shortcut
Set Shortcut = WshShell.CreateShortcut(ShortcutPath)
Shortcut.TargetPath = TargetPath
Shortcut.WorkingDirectory = "d:\销售\.trae\Get笔记学习系统"
Shortcut.Description = "Start Health Management System"
Shortcut.Save

' Show success message
MsgBox "Shortcut created on desktop: " & ShortcutPath, vbInformation, "Create Shortcut"
