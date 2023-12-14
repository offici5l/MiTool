#!/data/data/com.termux/files/usr/bin/bash

cp {mitool,flashfastbootrom.py,unlockbootloader.py,flashrecoveryrom.py} $PREFIX/bin/ && chmod +x $PREFIX/bin/{mitool,flashfastbootrom.py,unlockbootloader.py,flashrecoveryrom.py} && pkg install coreutils && yes | pkg install gnupg && yes | pkg install wget && mkdir -p $PREFIX/etc/apt/sources.list.d && echo -e "deb https://nohajc.github.io termux extras" > $PREFIX/etc/apt/sources.list.d/termux-adb.list && wget -qP $PREFIX/etc/apt/trusted.gpg.d https://nohajc.github.io/nohajc.gpg && apt update && yes | apt install termux-adb && mv $PREFIX/bin/termux-fastboot $PREFIX/bin/fastboot && mv $PREFIX/bin/termux-adb $PREFIX/bin/adb && yes | pkg install python && pkg install libexpat && yes | pkg install openssl-tool && pip install requests && pip3 install pyshorteners && pip3 install pycryptodomex && pip install termcolor

echo
echo -e "use command: \033[32mmitool\033[0m"
echo
