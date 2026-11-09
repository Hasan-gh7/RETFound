@echo off
setlocal
set "RETFOUND_PYTHON=%USERPROFILE%\.conda\envs\ml-homework\python.exe"
if not exist "%RETFOUND_PYTHON%" (
  echo The ml-homework Python environment was not found.
  exit /b 1
)
"%RETFOUND_PYTHON%" -B "%~dp0scripts\evaluate_aptos.py" "%~dp0APTOS2019.zip" --count 1000 --open-report %*
if errorlevel 1 (
  echo Evaluation did not complete. Review the error above.
  pause
  exit /b 1
)
endlocal
