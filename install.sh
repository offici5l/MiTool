#!/data/data/com.termux/files/usr/bin/bash

echo -e "\033[32mpkg update ...\033[0m" && yes | pkg update
echo -e "\033[32mpkg upgrade ...\033[0m" && yes | pkg upgrade

if [ ! -f "$PREFIX/var/lib/dpkg/info/openssl-tool.list" ]; then
  yes | pkg install openssl-tool
  yes | pkg install openssl
else
  echo -e "\033[32mopenssl-tool is installed.\033[0m"
fi

if [ ! -f "$PREFIX/share/doc/gnupg/OpenPGP" ]; then
  yes | pkg install gnupg
else
  echo -e "\033[32mgnupg is installed.\033[0m"
fi

if [ ! -f "$PREFIX/bin/coreutils" ]; then
  yes | pkg install coreutils
else
  echo -e "\033[32mcoreutils is installed.\033[0m"
fi

if [ ! -f "$PREFIX/bin/wget" ]; then
  yes | pkg install wget
else
  echo -e "\033[32mwget is installed.\033[0m"
fi

if [ ! -f "$PREFIX/bin/pv" ]; then
  yes | pkg install pv
else
  echo -e "\033[32mpv is installed.\033[0m"
fi

if [ ! -f "$PREFIX/bin/python" ]; then
  yes | pkg install python
else
  echo -e "\033[32mpython is installed.\033[0m"
fi

if [ ! -f "$PREFIX/lib/python3.11/site-packages/requests/sessions.py" ]; then
  yes | pip install requests
else
  echo -e "\033[32mrequests is installed.\033[0m"
fi

if [ ! -f "$PREFIX/lib/python3.11/site-packages/pyshorteners/base.py" ]; then
  yes | pip3 install pyshorteners
else
  echo -e "\033[32mpyshorteners is installed.\033[0m"
fi

if [ ! -f "$PREFIX/lib/python3.11/site-packages/Cryptodome/Random/random.py" ]; then
  yes | pip3 install pycryptodomex
else
  echo -e "\033[32mpycryptodomex is installed.\033[0m"
fi

if [ ! -f "$PREFIX/lib/python3.11/site-packages/termcolor/termcolor.py" ]; then
  yes | pip install termcolor
else
  echo -e "\033[32mtermcolor is installed.\033[0m"
fi

echo -e "\033[32mapt-get update ...\033[0m" && yes | apt-get update > /dev/null 2>&1
echo -e "\033[32mapt-get upgrade ...\033[0m" && yes | apt-get upgrade > /dev/null 2>&1

if [ ! -f "$PREFIX/etc/apt/sources.list.d/termux-adb.list" ]; then
  mkdir -p $PREFIX/etc/apt/sources.list.d
  echo -e "deb https://nohajc.github.io termux extras" > $PREFIX/etc/apt/sources.list.d/termux-adb.list
  wget -qP $PREFIX/etc/apt/trusted.gpg.d https://nohajc.github.io/nohajc.gpg
  yes | apt update
  yes | apt install termux-adb
  cp $PREFIX/bin/termux-adb $PREFIX/bin/adb && cp $PREFIX/bin/termux-fastboot $PREFIX/bin/fastboot
else
  echo -e "\033[32madb&fastboot is installed.\033[0m"
  echo -e "\033[32mupdate adb&fastboot ...\033[0m"
  yes | apt install termux-adb > /dev/null 2>&1
  cp $PREFIX/bin/termux-adb $PREFIX/bin/adb && cp $PREFIX/bin/termux-fastboot $PREFIX/bin/fastboot
fi

files=("mitool" "flashfastbootrom.py" "unlockbootloader.py" "flashrecoveryrom.py" "root.py" "flashcustomrecovery.py" "mitoolV")

for file in "${files[@]}"; do
    echo -e "\033[32mupdate $file...\033[0m"
    curl -# "https://raw.githubusercontent.com/offici5l/MiTool/master/$file" -o "$PREFIX/bin/$file" &&
    chmod +x "$PREFIX/bin/$file"
done


printf "
use command: \e[1;32mmitool\e[0m\n
"