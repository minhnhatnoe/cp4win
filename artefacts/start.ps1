$ErrorActionPreference="Stop"

Expand-Archive -Path "$pwd/dstr.zip" -DestinationPath "$pwd/dstr"
Set-Location .\dstr

./python-embed/python.exe run.py install
