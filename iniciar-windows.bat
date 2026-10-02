@echo off
setlocal
cd /d "%~dp0"

set "PY="
where py >nul 2>nul
if not errorlevel 1 set "PY=py"
if defined PY goto run
where python >nul 2>nul
if not errorlevel 1 set "PY=python"
if defined PY goto run

echo Python nao foi encontrado neste computador.
echo Instale em https://www.python.org/downloads/ e marque "Add python.exe to PATH".
echo Depois, execute este arquivo novamente.
pause
exit /b 1

:run
%PY% servidor.py
pause
endlocal
