#!/usr/bin/python
import os
import shutil

print(f"\033[H\033[J")

RESET = "\033[0m"
GREEN = "\033[1;32m"
GRAY = "\033[1;30m"

terminal_width = shutil.get_terminal_size().columns

print(f"""
{GRAY}━{'━' * (terminal_width - 2)}━
- {GREEN}fastboot{RESET}{GRAY} and {GREEN}adb {GRAY}commands can be used in the terminal.
{GRAY}━{'━' * (terminal_width - 2)}━
- MiTool is automatically updated when a new version is available, but you can do this manually by: {GREEN}mitool u{RESET}
{GRAY}━{'━' * (terminal_width - 2)}━
Mitool shortcuts commands:
Unlock-Bootloader = {GREEN}miunlock{RESET}{GRAY}
Flash-Fastboot-ROM = {GREEN}miflashf{RESET}{GRAY}
Flash-Zip-With-Sideload = {GREEN}miflashs{RESET}{GRAY}
Bypass = {GREEN}mibypass{RESET}{GRAY}
Mi-Assistant = {GREEN}miasst{RESET}{GRAY}
Help = {GREEN}mihelp{RESET}
{GRAY}━{'━' * (terminal_width - 2)}━
To report issues or share feedback, visit:  
- GitHub Issues: github.com/offici5l/MiTool/issues  
- Telegram Group: t.me/Offici5l_Group
{GRAY}━{'━' * (terminal_width - 2)}━
{GRAY}⚙️{'⚙️' * (terminal_width - 2)}⚙️
""")

print(f"""

{'━' * os.get_terminal_size().columns}\n{'Lock 🔒 Bootloader'.center(os.get_terminal_size().columns)}

Method 1:
Flash-Fastboot-ROM ↓
Flash all with lock bootloader

Method 2:
Before starting the process, ensure that the partitions are clean. If you have previously rooted your device, flash the clean boot.img. If any modifications have been made to any partition, flash the clean partition to avoid potential issues in the future.
To lock the bootloader, type: {GREEN}fastboot oem lock{RESET}{GRAY}

""")