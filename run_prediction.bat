@echo off
setlocal
set "RETFOUND_PYTHON=%USERPROFILE%\.conda\envs\ml-homework\python.exe"
if not exist "%RETFOUND_PYTHON%" (
    echo ml-homework environment missing. See the Windows prediction section in README.md.
    exit /b 1
)
if "%~1"=="" (
    "%RETFOUND_PYTHON%" "%~dp0predict_aptos.py" "%~dp0sample_images\idrid_test.jpg"
) else (
    "%RETFOUND_PYTHON%" "%~dp0predict_aptos.py" %*
)
exit /b %errorlevel%
