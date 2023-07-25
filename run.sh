#!/usr/bin/env bash

function get_python3() {
    if command -v python3 &> /dev/null
    then
        echo "python3"
    else
        echo "Python3 not found. Please install Python3.7 or higher."
        exit 1
    fi
}

function get_config_value() {
    local yaml_file="env.yaml"
    local key="$1"

    local value=$(grep "$key:" "$yaml_file" | awk -F': ' '{print $2}')

    if [[ -z "$value" ]]; then
        echo "Error: Key '$key' not found in config file '$yaml_file'."
        exit 1
    fi

    echo "$value"
}

function start_frontend() {
    PYTHON_CMD="$1"
    frontend_port=$(get_config_value "FRONTEND_PORT")
    $PYTHON_CMD -m http.server $frontend_port --directory frontend &

    echo $!

    backend_port=$(get_config_value "BACKEND_PORT")
    for ((i=1; i<=15; i++))
    do
    response=$(curl -s -o /dev/null -w "%{http_code}" 127.0.0.1:$backend_port)

    echo $response
    if [ "$response" = "404" ] || [ "$response" = "200" ]; then
        echo -e "\n\nService started successfully, please use browser to visit: http://127.0.0.1:$frontend_port"
        break
    else
        echo "Service has not started yet, please wait..."
        sleep 10
    fi
    done
}

function kill_by_port() {
    port="$1"
    os_type=$(uname -s)
    case "$os_type" in
        Linux*)
            pid=$(lsof -t -i ":$port")
            ;;
        Darwin*)
            pid=$(lsof -t -i ":$port")
            ;;
        *)
            echo "unknown os type: $os_type"
            exit 1
            ;;
    esac
    if [ -z "$pid" ]; then
        echo "The port is not in use: $port"
        exit 1
    fi
    kill -9 $pid
}

PYTHON_CMD=$(get_python3)

if $PYTHON_CMD -c "import sys; sys.exit(sys.version_info < (3, 7))"; then
    echo Installing missing packages...
    $PYTHON_CMD -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
else
    echo "Python 3.7 or higher is required to run DevOpsGPT."
    exit 1
fi

# start the frontend service
start_frontend $PYTHON_CMD &
frontend_pid=$!

# start the backend service
$PYTHON_CMD backend/run.py 

# or run the `ps -ef | grep 8080` command to get the PID and `kill PID` to stop
kill_by_port $(get_config_value "FRONTEND_PORT")
