#!/usr/bin/python

version = "1.5.0"

import subprocess, requests, shutil, re
from os import get_terminal_size

try:
    response = requests.get("https://raw.githubusercontent.com/offici5l/MiTool/master/MT/mitool.py", timeout=3)
    response.raise_for_status()
    if response.status_code == 200:
        version_match = re.search(r'version\s*=\s*"([^"]+)"', response.text)
        if version_match:
            vcloud = version_match.group(1)
            if vcloud > version:
                subprocess.run("curl https://raw.githubusercontent.com/offici5l/MiTool/master/install.sh | bash", shell=True)
                exit()
        else:
            pass
    else:
        pass
except requests.exceptions.ConnectionError:
    pass
except requests.exceptions.Timeout:
    pass

c1="\033[1;32m"
c2="\033[0m"

_l =  c1 + "_"*56 + c2 + "\n"

print(_l)

ver = f"MiTool {version}"
b = '━' * (len(ver) + 4)
p = ' ' * ((get_terminal_size().columns - len(b)) // 2)
furl = f"\n{p}┏{b}┓\n{p}┃  {ver}  ┃\n{p}┗{b}┛"
print(furl + f" ━ {c1}h{c2}elp")


print(f"""


━ {c1}1{c2} Unlock-Bootloader

━ {c1}2{c2} Flash-Fastboot-ROM

━ {c1}3{c2} Flash-Zip-With-Sideload

━ {c1}4{c2} Bypass


""")

choice = input(f'Enter your {c1}choice{c2}: ')

if choice == "1":
    subprocess.run(["miunlock"])
elif choice == "2":
    subprocess.run(["flashf"])
elif choice == "3":
    subprocess.run(["flashz"])
elif choice == "4":
    subprocess.run(["mibypass"])
elif choice == "u":
    subprocess.run(["curl", "-s", "https://raw.githubusercontent.com/offici5l/MiTool/master/install.sh", "|", "bash"])
    subprocess.run(["mitool"])
elif choice == "h":
    print(f"""
{_l}
Lock Bootloader:

Type: {c1}fastboot oem lock{c2}
{_l}
Flash Custom Recovery:

Type: {c1}fastboot flash recovery /path/name.img{c2}

Example:
fastboot flash recovery /sdcard/download/recovery.img
{_l}
Flash Root:
1. Download and install Magisk app
2. Open Magisk app, press Install in the Magisk card
3. Choose 'Select and Patch a File', select boot.img
   (Note: Choose boot.img for device you want to root)

Type: {c1}fastboot flash boot /path/name.img{c2}

Example: fastboot flash boot /sdcard/download/boot.img
{_l}
Flash Specific Partitions
('recovery', 'boot', 'vbmeta', 'vbmeta_system', 'metadata', 'dtbo', 'cust', 'super', 'userdata', ...):

Type:
{c1}fastboot flash PatitionName /path/FilePartitionName{c2}

Example:
fastboot flash super /sdcard/download/super.img
{_l}
For more fastboot and adb commands:

Type: {c1}fastboot help{c2} or {c1}adb help{c2}
{_l}
For updating MiTool:

Type: {c1}u{c2}
{_l}
To report issues or share feedback, visit:

- GitHub Issues: github.com/offici5l/MiTool/issues
- Telegram Group: t.me/Offici5l_Group
{_l}
""")
else:
    print("\nInvalid choice\n")
    exit()

