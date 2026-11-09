@echo off
setlocal
set "PYTHON_EXE=%USERPROFILE%\.conda\envs\ml-homework\python.exe"
if not exist "%PYTHON_EXE%" (
  set "PYTHON_EXE=python"
)
"%PYTHON_EXE%" -B "%~dp0run_demo.py"
if errorlevel 1 pause
endlocal
