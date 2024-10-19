#!/bin/bash

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    IP_ADDRESS=$(hostname -I | awk '{print $1}')  # Linux
elif [[ "$OSTYPE" == "darwin"* ]]; then
    IP_ADDRESS=$(ifconfig | grep 'inet ' | awk '$1 != "127.0.0.1" {print $2}')  # macOS
elif [[ "$OSTYPE" == "cygwin" ]]; then
    IP_ADDRESS=$(hostname -I | awk '{print $1}')  # Cygwin
elif [[ "$OSTYPE" == "msys" ]]; then
    IP_ADDRESS=$(hostname -I | awk '{print $1}')  # Git Bash on Windows
else
    echo "Unsupported OS"
    exit 1
fi

export PROD_MODE=false
export HOST_IP_ADDRESS="$IP_ADDRESS"

while getopts "bx" option; do
    case "${option}" in
        b)
            docker-compose up --build -d
            ;;
        x)
            docker-compose exec app /bin/bash
            ;;
        *)
            echo "Usage: $0 -b | -x"
            exit 1
            ;;
    esac
done

# Check if no option was provided
if [ "$OPTIND" -eq 1 ]; then
    echo "Usage: $0 -b | -x"
    exit 1
fi