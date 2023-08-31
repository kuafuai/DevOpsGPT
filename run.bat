@echo off
setlocal enabledelayedexpansion

call :get_python3

if errorlevel 1 (
    echo Python 3.7 or higher is required to run DevOpsGPT.
    exit /b 1
)

copy .\.github\hooks\pre-commit .\.git\hooks\

echo Installing missing packages...
call %PYTHON_CMD% -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

start "" %PYTHON_CMD% backend\run.py

call :start_frontend %PYTHON_CMD%

call :kill_by_port %%BACKEND_PORT%%

exit /b 0

REM function
:get_python3
    for /f "delims=" %%i in ('where python 2^>nul') do (
        set "PYTHON_CMD=%%i"
        goto :pyCheck
    )
    :pyCheck
    if not defined PYTHON_CMD (
        echo Python3 not found. Please install Python3.7 or higher.
        exit /b 1
    )
GOTO:EOF

:get_config_value
    set "yaml_file=env.yaml"
    set "key=%~1"

    for /f "usebackq tokens=2 delims=: " %%a in (`findstr /C:"%key%:" "%yaml_file%"`) do (
        set "value=%%a"
    )

    if not defined value (
        echo Error: Key '%key%' not found in config file '%yaml_file%'. Please copy a new env.yaml from env.yaml.tpl and reconfigure it according to the documentation.
        exit /b 1
    )
    set "%key%=!value!"
GOTO:EOF

:start_frontend
    set "PYTHON_CMD=%~1"
    call :get_config_value FRONTEND_PORT
    call :get_config_value BACKEND_PORT
    if %errorlevel%==1 (
        pause
        exit /b 1
    )

    REM Wait for the backend service to start
    for /l %%i in (1, 1, 20) do (
        set "response="
        for /f "delims=" %%a in ('set HTTP_PROXY= ^& set HTTPS_PROXY= ^& set ALL_PROXY= ^& set http_proxy= ^& set https_proxy= ^& set all_proxy= ^& curl -s -o nul -w "%%{http_code}" http://127.0.0.1:%BACKEND_PORT%') do set "response=%%a"

        echo !response!
        if "!response!"=="404" (
            echo.
            echo Service started successfully, please use a browser to visit: http://127.0.0.1:!FRONTEND_PORT!
            GOTO :starFrontend
        ) else (
            timeout /t 5 > nul
        )
    )
    :starFrontend
    call %PYTHON_CMD% -m http.server %FRONTEND_PORT% --directory frontend
GOTO:EOF

:kill_by_port
    set "port=%~1"
    for /f "delims=" %%a in ('netstat -aon ^| findstr "LISTENING" ^| findstr ":!port!"') do (
        set "line=%%a"
        for /f "tokens=5" %%b in ("!line!") do set "pid=%%b"
    )

    if not defined pid (
        echo The port is not in use: %port%
        exit /b 1
    )

    taskkill /f /pid %pid%
GOTO:EOF
