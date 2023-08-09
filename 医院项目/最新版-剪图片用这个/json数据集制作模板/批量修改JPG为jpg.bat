@echo off
setlocal enabledelayedexpansion

for /r "%cd%" %%f in (*.jpg *.JPG) do (
    set "filename=%%~nf"
    set "ext=%%~xf"
    ren "%%f" "!filename!.png"
)

for /r "%cd%" %%f in (*.png) do (
    set "filename=%%~nf"
    set "ext=%%~xf"
    ren "%%f" "!filename!.jpg"
)

echo 替换完成！
