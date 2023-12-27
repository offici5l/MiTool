#!/data/data/com.termux/files/usr/bin/bash

files=("mitool" "flashfastbootrom.py" "unlockbootloader.py" "flashrecoveryrom.py" "root.py")

for file in "${files[@]}"; do
    curl -s "https://raw.githubusercontent.com/offici5l/MiTool/master/$file" -o "$PREFIX/bin/$file" &&
    chmod +x "$PREFIX/bin/$file"
done

yes | pkg update && curl -s https://raw.githubusercontent.com/nohajc/termux-adb/master/install.sh | bash && mv $PREFIX/bin/termux-fastboot $PREFIX/bin/fastboot && mv $PREFIX/bin/termux-adb $PREFIX/bin/adb && yes | pkg install python && yes | pkg install openssl-tool && pip install requests && pip3 install pyshorteners && pip3 install pycryptodomex && pip install termcolor && pkg install pv

echo -e "
use command: \033[32mmitool\033[0m
"