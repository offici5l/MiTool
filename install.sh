#!/data/data/com.termux/files/usr/bin/bash

echo -e "\n\033[32mpkg update&upgrade...\033[0m"

yes | pkg update 2> >(grep -v "WARNING: apt does not have a stable CLI interface" >&2) > /dev/null && yes | pkg upgrade 2> >(grep -v "WARNING: apt does not have a stable CLI interface" >&2) > /dev/null

if ! command -v adb &>/dev/null || ! command -v fastboot &>/dev/null; then
    curl -s https://raw.githubusercontent.com/offici5l/termux-adb-fastboot/main/install | bash
fi

if ! command -v pv &>/dev/null; then
    echo "Installing pv..."
    yes | pkg install pv
fi

if ! command -v python3 &>/dev/null; then
    echo "Installing Python3..."
    yes | pkg install python3
fi

if ! python3 -c "import Cryptodome" &>/dev/null; then
    echo "Installing Cryptodome..."
    yes | pip install pycryptodomex --extra-index-url https://termux-user-repository.github.io/pypi/
fi

if ! python3 -c "import urllib3" &>/dev/null; then
    echo "Installing urllib3..."
    yes | pip install urllib3
fi

if ! python3 -c "import requests" &>/dev/null; then
    echo "Installing requests..."
    yes | pip install requests
fi

if ! dpkg -l | grep -q libusb; then
    echo "Installing libusb..."
    yes | pkg install libusb
fi

echo -e "\033[32mupdate MiTool...\033[0m"
curl -s "https://raw.githubusercontent.com/offici5l/MiTool/master/MT/mitool.py" -o "$PREFIX/bin/mitool" && chmod +x "$PREFIX/bin/mitool"

echo -e "\033[32mupdate MiHelp...\033[0m"
curl -s "https://raw.githubusercontent.com/offici5l/MiTool/master/MT/mihelp.py" -o "$PREFIX/bin/mihelp" && chmod +x "$PREFIX/bin/mihelp"

echo -e "\033[32mupdate MiFlashF...\033[0m"
curl -s "https://raw.githubusercontent.com/offici5l/MiTool/master/MT/miflashf.py" -o "$PREFIX/bin/miflashf" && chmod +x "$PREFIX/bin/miflashf"

echo -e "\033[32mupdate MiFlashS...\033[0m"
curl -s "https://raw.githubusercontent.com/offici5l/MiTool/master/MT/miflashs.py" -o "$PREFIX/bin/miflashs" && chmod +x "$PREFIX/bin/miflashs"

echo -e "\033[32mupdate MiUnlockTool...\033[0m"
curl -s "https://raw.githubusercontent.com/offici5l/MiUnlockTool/master/MiUnlockTool.py" -o "$PREFIX/bin/miunlock" && chmod +x "$PREFIX/bin/miunlock"

echo -e "\033[32mupdate MiBypassTool...\033[0m"
curl -s "https://raw.githubusercontent.com/offici5l/MiBypassTool/master/MiBypassTool.py" -o "$PREFIX/bin/mibypass" && chmod +x "$PREFIX/bin/mibypass"

echo -e "\033[32mupdate MiAssistantTool...\033[0m"
if [ $(uname -m) == "aarch64" ]; then
    curl -s -L -o $PREFIX/bin/miasst $(curl -s "https://api.github.com/repos/offici5l/MiAssistantTool/releases/latest" | grep "browser_download_url.*miasst_termux_aarch64" | cut -d '"' -f 4)
    chmod +x $PREFIX/bin/miasst
else
    curl -s -L -o $PREFIX/bin/miasst $(curl -s "https://api.github.com/repos/offici5l/MiAssistantTool/releases/latest" | grep "browser_download_url.*miasst_termux_arm" | cut -d '"' -f 4)
    chmod +x $PREFIX/bin/miasst
fi

curl -L -s https://raw.githubusercontent.com/offici5l/MiTool/main/CHANGELOG.md | tac | awk '/^#/{exit} {print "\033[0;34m" $0 "\033[0m"}' | tac

printf "\nuse command: \e[1;32mmitool\e[0m\n\n"