#!/bin/bash
# export DISPLAY adalah agar tidak error pada qt.qpa.plugin
export DISPLAY=:0
script_directory="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

cd $script_directory
cd ..

echo $(date)>>./logs/logs_cron.txt
lazy_attend="./lazy_attend.py"
while true
do
    $lazy_attend
    sleep 10
done
