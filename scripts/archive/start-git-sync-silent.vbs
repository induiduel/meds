Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
scriptDir = fso.GetParentFolderName(WScript.ScriptFullName)
projectDir = fso.GetParentFolderName(scriptDir)

WshShell.CurrentDirectory = projectDir
WshShell.Run "node scripts\auto-git-sync.mjs --interval=20", 0, False
