Set WshShell = CreateObject("WScript.Shell")
' MedSoru yerel senkronizasyon servisini arka planda sessizce (pencere açmadan) başlatır
WshShell.Run "node ""C:\Users\indui\Desktop\meds\scripts\meds-local-sync.mjs"" --daemon", 0, False
Set WshShell = Nothing
