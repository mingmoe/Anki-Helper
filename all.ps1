# 两个愿望，一次满足！
Push-Location $PSScriptRoot
&python "$PSScriptRoot/start.py"
&python "$PSScriptRoot/gen.py"
Pop-Location
