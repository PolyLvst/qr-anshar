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
lazy_attend="./lazy_attend.py"
while true
do
    $lazy_attend
    sleep 10
done
