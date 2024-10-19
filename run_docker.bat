@echo off
setlocal

set PROD_MODE=false

for /f "tokens=2 delims=:" %%i in ('ipconfig ^| findstr /C:"IPv4" ^| findstr /v "127.0.0.1"') do (
    set "HOST_IP_ADDRESS=%%i"
    goto :done
)

:done
if "%~1"=="" (
    echo "Usage: %0 -b | -x"
    exit /b 1
)

set "option=%~1"
if /i "%option%"=="-b" (
    docker-compose up --build -d
) else if /i "%option%"=="-x" (
    docker-compose exec app /bin/bash
) else (
    echo "Usage: %0 -b | -x"
    exit /b 1
)

endlocal