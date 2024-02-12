#!/bin/bash
# export DISPLAY adalah agar tidak error pada qt.qpa.plugin
export DISPLAY=:0
script_directory="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

cd $script_directory
cd ..
folder_path="./logs"

if [ ! -d "$folder_path" ]; then
    # If the folder does not exist, create it
    mkdir -p "$folder_path"
    echo "Folder logs created successfully."
else
    # If the folder already exists, print a message
    echo "Logger ..."
fi

echo $(date)>>./logs/logs_cron.txt
web_server_py="python -m gunicorn -w 1 -b 0.0.0.0:5000 app:app"
lazy_attend="$script_directory/lazy_attend.py"
$web_server_py
echo "Closing, please wait [5s]"
echo "Uploading remaining students"
$lazy_attend
sleep 5s