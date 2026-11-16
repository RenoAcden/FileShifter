Set FSO = CreateObject("Scripting.FileSystemObject")
ScriptDir = FSO.GetParentFolderName(WScript.ScriptFullName)

Set WshShell = CreateObject("WScript.Shell")
WshShell.CurrentDirectory = ScriptDir
WshShell.Run "pythonw.exe """ & ScriptDir & "\automates-files.py""", 0, False
