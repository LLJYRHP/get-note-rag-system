Set WshShell = WScript.CreateObject("WScript.Shell")

' 获取桌面路径
strDesktop = WshShell.SpecialFolders("AllUsersDesktop")

' 如果公共桌面不存在，使用用户桌面
If strDesktop = "" Then
    strDesktop = WshShell.SpecialFolders("Desktop")
End If

' 创建快捷方式
Set oShellLink = WshShell.CreateShortcut(strDesktop & "\Get 笔记 RAG 问答系统.lnk")
oShellLink.TargetPath = "C:\Users\Administrator\AppData\Local\Programs\Python\Python312\python.exe"
oShellLink.Arguments = "-m streamlit run app.py"
oShellLink.WorkingDirectory = "d:\销售\.trae\Get 笔记学习系统"
oShellLink.Description = "Get 笔记 RAG 问答系统 - 基于 RAG 的智能问答学习工具"
oShellLink.IconLocation = "%SystemRoot%\System32\shell32.dll,13"
oShellLink.Save

MsgBox "桌面快捷方式已创建成功！" & vbCrLf & vbCrLf & "您可以在桌面找到 ""Get 笔记 RAG 问答系统"" 快捷方式，双击即可运行。", vbInformation, "创建成功"

Set oShellLink = Nothing
Set WshShell = Nothing
