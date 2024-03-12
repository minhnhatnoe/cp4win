$ErrorActionPreference = "Stop"

$ShortcutFile = "$env:Public\Desktop\" + $Args[1] + ".lnk"
$WScriptShell = New-Object -ComObject WScript.Shell
$Shortcut = $WScriptShell.CreateShortcut($ShortcutFile)
$Shortcut.TargetPath = $Args[0]
$Shortcut.WorkingDirectory = $Shortcut.TargetPath.parent
$Shortcut.Save()
