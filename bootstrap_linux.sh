#!/bin/bash
VERS="1.0"
# Check if build-essential is installed
if ! dpkg -l | grep -q "build-essential"; then
    echo "build-essential is not installed. Installing..."
    sudo apt-get update
    sudo apt-get install -y build-essential
fi

# Check if python3-dev is installed
if ! dpkg -l | grep -q "python3-dev"; then
    echo "python3-dev is not installed. Installing..."
    sudo apt-get update
    sudo apt-get install -y python3-dev
fi

# Check if cmake is installed
if ! dpkg -l | grep -q "cmake"; then
    echo "cmake is not installed. Installing..."
    sudo apt-get update
    sudo apt-get install -y cmake
fi

# Check if pip is installed
if ! dpkg -l | grep -q "python3-pip"; then
    echo "cmake is not installed. Installing..."
    sudo apt-get update
    sudo apt-get install -y python3-pip
fi

# Check if dos2unix is installed
if ! command -v dos2unix &>/dev/null; then
    echo "dos2unix is not installed. Installing..."
    sudo apt-get update
    sudo apt-get install -y dos2unix
fi

echo "Converting python to unix"
script_directory="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
if [ -d "$script_directory" ]; then
    # Convert from dos to unix
    find "$script_directory" -type f -name "*.py" -exec dos2unix {} \;
    echo "Conversion complete."
else
    echo "Directory not found: $script_directory"
fi

if [ -d "$script_directory/linux" ]; then
    # Convert from dos to unix
    find "$script_directory/linux" -type f -name "*.sh" -exec dos2unix {} \;
    echo "Conversion complete [linux]."
else
    echo "Directory not found: $script_directory/linux"
fi

echo "Installing requirements"
pip install -r $script_directory/requirements.txt

# Check if the .env file exists
env_file="./.env"
if [ -f "$env_file" ]; then
    echo ".env file exist"
else
    echo "File .env does not exist."
fi
# xampp_path="/opt/lampp/xampp"
# if [ -f "$xampp_path" ]; then
#     echo "xampp ready to be used"
# else
#     echo "#### Warning xampp is missing ####"
# fi
crontab_main="$script_directory/crontab.txt"
echo "Buka terminal lalu ketik crontab -e"> $crontab_main
echo "Copy & Paste :">> $crontab_main
# Change the path for xampp
# echo "@reboot sleep 20;cd $script_directory;XDG_RUNTIME_DIR=/run/user/$(id -u) sudo $xampp_path startmysql >> $script_directory/logs/logs_cron.txt 2>&1">> $crontab_main
# Change the path for web_server
echo "@reboot sleep 30;cd $script_directory;XDG_RUNTIME_DIR=/run/user/$(id -u) $script_directory/linux/run.sh >> $script_directory/logs/logs_cron.txt 2>&1">> $crontab_main
# Change the path for lazy_attend.py
echo "*/5 * * * 1-6 cd $script_directory && $script_directory/lazy_attend.py >> $script_directory/logs/logs_cron.txt 2>&1">> $crontab_main
# echo "Crontab.txt is ready to be copied by user"

find "$script_directory" -type f -name "*.py" -exec chmod +x {} \;
echo "Executing permission granted for all py file"
find "$script_directory/linux" -type f -name "*.sh" -exec chmod +x {} \;
echo "Executing permission granted for all sh file inside linux folder"
echo "Making desktop icon and shortcuts .. "
run_sh="$script_directory/linux/run.sh"
desktop_entry="$script_directory/qr_web.desktop"
desktop_entry_temp="$script_directory/qr_web-$VERS.desktop"
cp $desktop_entry $desktop_entry_temp
icon_app="$script_directory/resources/desktop.png"
if [ -f "$desktop_entry_temp" ]; then
    sed -i "s|Exec=path|Exec=$run_sh|" "$desktop_entry_temp"
    sed -i "s|Icon=path|Icon=$icon_app|" "$desktop_entry_temp"
    if [ $? -eq 0 ]; then
        echo "$desktop_entry_temp updated."
    else
        echo "Failed to update $desktop_entry_temp."
    fi
else
    echo "File $desktop_entry_temp does not exist."
fi
chmod +x $run_sh
cd ~
cp $desktop_entry_temp "Desktop/"
cp $desktop_entry_temp ".local/share/applications/"
rm $desktop_entry_temp

chmod +x "Desktop/qr_web-$VERS.desktop"
chmod +x ".local/share/applications/qr_web-$VERS.desktop"
echo "All required packages are installed."
echo "Klik kanan shortcut desktop lalu klik allow launching"
echo "Bootstrap done .. dont forget to add the cron job inside the crontab.txt file"
