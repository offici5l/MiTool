#!/data/data/com.termux/files/usr/bin/bash

echo -e "
\033[32mupdate pkg ...\033[0m
" && yes | pkg update && echo -e "
\033[32mupgrade pkg ...\033[0m
" && yes | pkg upgrade

if command -v openssl &>/dev/null; then
    echo -e "
\033[32mopenssl is installed\033[0m
"
else
    pkg install openssl-tool
    pkg install openssl
fi

if command -v coreutils &>/dev/null; then
    echo -e "
\033[32mcoreutils is installed\033[0m
"
else
    pkg install coreutils
fi

if command -v gpg &>/dev/null; then
    echo -e "
\033[32mGnuPG is installed.\033[0m
"
else
    pkg install gnupg
fi

if command -v wget &>/dev/null; then
    echo -e "
\033[32mwget is installed.\033[0m
"
else
    pkg install wget
fi

if [ ! -f "$PREFIX/etc/apt/sources.list.d/termux-adb.list" ]; then
  mkdir -p $PREFIX/etc/apt/sources.list.d
  echo -e "deb https://nohajc.github.io termux extras" > $PREFIX/etc/apt/sources.list.d/termux-adb.list
  wget -qP $PREFIX/etc/apt/trusted.gpg.d https://nohajc.github.io/nohajc.gpg
else
  echo -e "
\033[32msources exist.\033[0m
"
fi

if command -v termux-adb &>/dev/null; then
    echo -e "
\033[32madb is installed.\033[0m
"
else
    pkg uninstall termux-adb &>/dev/null
    apt update &>/dev/null
    apt install termux-adb
fi

if command -v termux-fastboot &>/dev/null; then
    echo -e "
\033[32mfastboot is installed.\033[0m
"
else
    pkg uninstall termux-adb &>/dev/null
    apt update &>/dev/null
    apt install termux-adb
fi

if command -v adb &>/dev/null; then
    echo -e "
\033[32madb file exist.\033[0m
"
else
    cp $PREFIX/bin/termux-adb $PREFIX/bin/adb
    echo "fix adb ..."
fi

if command -v fastboot &>/dev/null; then
    echo -e "
\033[32mfastboot file exist.\033[0m
"
else
    cp $PREFIX/bin/termux-fastboot $PREFIX/bin/fastboot
    echo "fix fastboot ..."
fi

if command -v pv &>/dev/null; then
    echo -e "
\033[32mpv is installed.\033[0m
"
else
    pkg install pv
fi

if command -v python &>/dev/null || command -v python3 &>/dev/null; then
    echo -e "
\033[32mpython is installed.\033[0m
"
else
    yes | pkg install python
fi

if python3 -c "import requests" &>/dev/null || python -c "import requests" &>/dev/null; then
    echo -e "
\033[32mrequests is installed.\033[0m
"
else
    pip install requests
fi

if python3 -c "import pyshorteners" &>/dev/null; then
    echo -e "
\033[32mpyshorteners is installed.\033[0m
"
else
    pip3 install pyshorteners
fi

if python3 -c "import Cryptodome" &>/dev/null; then
    echo -e "
\033[32mCryptodome is installed.\033[0m
"
else
    pip3 install pycryptodomex
fi

if python -c "import termcolor" &>/dev/null || python3 -c "import termcolor" &>/dev/null; then
    echo -e "
\033[32mtermcolor is installed.\033[0m
"
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