#!/bin/bash

case $1 in
    "app"|"")
        python3 -m pip install -r requirements.txt
        clear
        python3 main.py
        ;;
    "init"|"update")
        echo "Updating libraries....."
        python3 -m pip install -r requirements.txt
        echo "Done!"
        ;;
    "test")
        pytest tests/unit/
        ;;
esac