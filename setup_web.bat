@echo off
setlocal
set "RETFOUND_PYTHON=%USERPROFILE%\.conda\envs\ml-homework\python.exe"
if not exist "%RETFOUND_PYTHON%" (
  echo The ml-homework Python environment was not found.
  exit /b 1
)
"%RETFOUND_PYTHON%" -B -m pip install --only-binary=:all: --target "%~dp0.runtime\web" -r "%~dp0requirements-web.txt"
exit /b %errorlevel%
