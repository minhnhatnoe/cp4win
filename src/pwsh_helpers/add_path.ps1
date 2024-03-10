$USER_PATH = [Environment]::GetEnvironmentVariable("Path", [System.EnvironmentVariableTarget]::User) + $Args[0]
[Environment]::SetEnvironmentVariable("Path", $USER_PATH, [System.EnvironmentVariableTarget]::User)
