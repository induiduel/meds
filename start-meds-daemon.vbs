Set WshShell = CreateObject("WScript.Shell")
' MedSoru yerel senkronizasyon servisini arka planda sessizce (pencere açmadan) başlatır
WshShell.CurrentDirectory = "C:\Users\indui\Desktop\meds"
WshShell.Run "cmd /c node ""C:\Users\indui\Desktop\meds\scripts\meds-local-sync.mjs"" --daemon", 0, False
Set WshShell = Nothing
