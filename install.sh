#!/data/data/com.termux/files/usr/bin/bash

yes | pkg update && yes | pkg upgrade && yes | pkg install openssl-tool && yes | pkg install openssl && yes | pkg install gnupg && yes | pkg install coreutils && yes | pkg install wget && yes | pkg install pv && yes | pkg install python3 && yes | pip install requests && yes | pip3 install pyshorteners && yes | pip3 install pycryptodomex && yes | pip install termcolor && mkdir -p $PREFIX/etc/apt/sources.list.d && echo -e "deb https://nohajc.github.io termux extras" > $PREFIX/etc/apt/sources.list.d/termux-adb.list && wget -qP $PREFIX/etc/apt/trusted.gpg.d https://nohajc.github.io/nohajc.gpg && yes | apt update && yes | apt install termux-adb && cp -f $PREFIX/bin/termux-adb $PREFIX/bin/adb && cp -f $PREFIX/bin/termux-fastboot $PREFIX/bin/fastboot

files=("mitool" "flashfastbootromatest.py" "flashfastbootrom.py" "un-lock.py" "flashwithsideloadmode.py" "mitoolV")

for file in "${files[@]}"; do
    echo -e "\033[32mupdate $file...\033[0m"
    curl "https://raw.githubusercontent.com/offici5l/MiTool/master/MT/$file" -o "$PREFIX/bin/$file" &&
    chmod +x "$PREFIX/bin/$file"
done

printf "
use command: \e[1;32mmitool\e[0m\n
"