@echo off
setlocal
set "RETFOUND_PYTHON=%USERPROFILE%\.conda\envs\ml-homework\python.exe"
if not exist "%RETFOUND_PYTHON%" (
  echo The ml-homework Python environment was not found.
  pause
  exit /b 1
)
"%RETFOUND_PYTHON%" -B "%~dp0scripts\serve_web.py" --open-browser %*
if errorlevel 1 pause
endlocal
