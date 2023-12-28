#!/data/data/com.termux/files/usr/bin/bash

yes | pkg update && yes | pkg upgrade

if command -v termux-adb &>/dev/null || command -v termux-fastboot &>/dev/null; then
    echo "adb and fastboot is installed."
else
    yes | pkg remove termux-adb &>/dev/null
    curl -s https://raw.githubusercontent.com/nohajc/termux-adb/master/install.sh | bash
    mv $PREFIX/bin/termux-fastboot $PREFIX/bin/fastboot && mv $PREFIX/bin/termux-adb $PREFIX/bin/adb
fi

if command -v pv &>/dev/null; then
    echo "pv is installed."
else
    pkg install pv
fi

if command -v python &>/dev/null || command -v python3 &>/dev/null; then
    echo "Python is installed."
else
    yes | pkg install python
fi

if python3 -c "import requests" &>/dev/null || python -c "import requests" &>/dev/null; then
    echo "requests is installed."
else
    pip install requests
fi

if python3 -c "import pyshorteners" &>/dev/null; then
    echo "pyshorteners is installed."
else
    pip3 install pyshorteners
fi

if python3 -c "import Cryptodome" &>/dev/null; then
    echo "pycryptodomex is installed."
else
    pip3 install pycryptodomex
fi

if python -c "import termcolor" &>/dev/null || python3 -c "import termcolor" &>/dev/null; then
    echo "termcolor is installed."
else
    pip install termcolor
fi

files=("mitool" "flashfastbootrom.py" "unlockbootloader.py" "flashrecoveryrom.py" "root.py")

for file in "${files[@]}"; do
    curl -s "https://raw.githubusercontent.com/offici5l/MiTool/master/$file" -o "$PREFIX/bin/$file" &&
    chmod +x "$PREFIX/bin/$file"
done

echo -e "
use command: \033[32mmitool\033[0m
"