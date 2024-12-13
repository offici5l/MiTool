#!/usr/bin/python

import subprocess
import time

for i, choice in enumerate(["Read Info", "ROMs that can be flashed", "Flash Official Recovery ROM", "Format Data", "Reboot"], start=1):
    print(f"\n\033[0;32m{i}\033[0m => {choice}")

while True:
    choice = input("\nEnter your \033[0;32mchoice\033[0m: ")
    if choice.isdigit() and 1 <= int(choice) <= 5:
        print("\n")
        break
    print("\nInvalid choice !\n")

subprocess.run(["pkill", "-9", "-f", "tcp"])

while True:
    devices = subprocess.run("termux-usb -l | tr -d '[]\\\"'", shell=True, capture_output=True, text=True).stdout.strip()
    if devices:
        result = subprocess.run(f"echo \"{devices}\" | xargs -I{{}} $PREFIX/libexec/termux-api Usb -a permission --ez request true --es device {{}}", shell=True, capture_output=True, text=True)
        if "yes" in result.stdout:
            break
        print("\nGrant permission to termux-api")
    else:
        for i in range(4):
            print(f"\rNo USB devices connected {'.' * (i % 4)}", end="")
            time.sleep(0.5)

subprocess.run(f"termux-usb -E -e '/data/data/com.termux/files/usr/bin/miasst_termux {choice}' -r {devices}", shell=True)