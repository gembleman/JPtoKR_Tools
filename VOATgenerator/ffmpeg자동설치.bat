@ECHO OFF
PowerShell.exe -Command "irm get.scoop.sh | iex"
PowerShell.exe -Command "scoop bucket add main"
PowerShell.exe -Command "scoop install ffmpeg"
PAUSE