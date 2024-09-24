#!/usr/bin/python

version = "1.5.4"

import subprocess, requests, shutil, re, sys, os
from os import get_terminal_size

if not os.path.isdir(os.path.expanduser('~/storage')):
    print("\nPlease grant permission via command:\ntermux-setup-storage\n\nthen restart the tool\n")
    exit()

if 'u' in sys.argv or 'update' in sys.argv:
    subprocess.run("curl -s https://raw.githubusercontent.com/offici5l/MiTool/master/install.sh | bash -s -- f", shell=True)
    exit()

try:
    response = requests.get("https://raw.githubusercontent.com/offici5l/MiTool/master/MT/mitool.py", timeout=3)
    response.raise_for_status()
    if response.status_code == 200:
        version_match = re.search(r'version\s*=\s*"([^"]+)"', response.text)
        if version_match:
            vcloud = version_match.group(1)
            if vcloud > version:
                subprocess.run("curl -s https://raw.githubusercontent.com/offici5l/MiTool/master/install.sh | bash", shell=True)
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
print(furl + f" ━ {c1}help{c2}")

print(f"""


━ {c1}1{c2} Unlock-Bootloader

━ {c1}2{c2} Flash-Fastboot-ROM

━ {c1}3{c2} Flash-Zip-With-Sideload

━ {c1}4{c2} Bypass

━ {c1}5{c2} Mi-Assistant

""")

if len(sys.argv) > 1:
    choice = sys.argv[1]
    print(choice)
else:
    choice = input(f'Enter your {c1}choice{c2}: ')

if choice == "1":
    subprocess.run("$PREFIX/bin/miunlock", shell=True)
elif choice == "2":
    subprocess.run("$PREFIX/bin/miflashf", shell=True)
elif choice == "3":
    subprocess.run("$PREFIX/bin/miflashs", shell=True)
elif choice == "4":
    subprocess.run("$PREFIX/bin/mibypass", shell=True)
elif choice == "5":
    subprocess.run("$PREFIX/bin/miasst", shell=True)
elif choice == "h" or choice == "help":
    subprocess.run("$PREFIX/bin/mihelp", shell=True)
elif choice == "u" or choice == "update":
    subprocess.run("curl -s https://raw.githubusercontent.com/offici5l/MiTool/master/install.sh | bash -s -- f", shell=True)
    exit()
else:
    print("\nInvalid choice\n")
    exit()




