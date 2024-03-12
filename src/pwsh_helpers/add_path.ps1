$ErrorActionPreference = "Stop"

$USER_PATH = $Args[0] + ";" + [Environment]::GetEnvironmentVariable("Path", [System.EnvironmentVariableTarget]::User)
[Environment]::SetEnvironmentVariable("Path", $USER_PATH, [System.EnvironmentVariableTarget]::User)
