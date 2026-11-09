@echo off
setlocal
set "RETFOUND_PYTHON=%USERPROFILE%\.conda\envs\ml-homework\python.exe"
if not exist "%RETFOUND_PYTHON%" (
    echo The ml-homework Python environment was not found.
    exit /b 1
)
pushd "%~dp0"
"%RETFOUND_PYTHON%" -u prepare_benchmark.py
if errorlevel 1 (
    popd
    exit /b 1
)
"%RETFOUND_PYTHON%" -u evaluate_benchmark.py
set "RETFOUND_RESULT=%errorlevel%"
popd
exit /b %RETFOUND_RESULT%
