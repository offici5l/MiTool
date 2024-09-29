#!/usr/bin/python

RESET="\033[0m"
GREEN="\033[1;32m"
GRAY="\033[1;30m"
LINE=f"{GRAY}\n\n{'*'*56}\n\n{RESET}"

print(f"\033[H\033[J")

print(f"""{LINE}{GRAY}To report issues or share feedback, visit:\n- GitHub Issues: github.com/offici5l/MiTool/issues\n- Telegram Group: t.me/Offici5l_Group\n\n{RESET}{GREEN}fastboot{RESET}{GRAY} and{GREEN} adb {GRAY}commands can be used in the terminal.\n\nMiTool is automatically updated when a new version is available, but you can do this manually by: {GREEN}mitool u{RESET}{LINE}{LINE}{LINE}""")

message = f"""

Lock Bootloader:

notice: Prior to initiating the process, ensure that the partitions are clean (If you've previously rooted your device, flash the clean boot.img or if any modifications have been made to any partition, flash the clean partition-name.img) to prevent any potential issues in the future.
Type: {GREEN}fastboot oem lock{RESET}

{LINE}

Flash Custom Recovery:

Type: {GREEN}fastboot flash recovery /path/name.img{RESET}
Example:
fastboot flash recovery /sdcard/download/recovery.img

{LINE}

Flash Root(Magisk):
1. Download and install Magisk app
2. Open Magisk app, press Install in the Magisk card
3. Choose 'Select and Patch a File', select boot.img
   (Note: Choose boot.img for the device you want to root)
Type: {GREEN}fastboot flash boot /path/name.img{RESET}
Example: fastboot flash boot /sdcard/download/boot.img

{LINE}

Flash Specific Partitions:
('recovery', 'boot', 'vbmeta', 'vbmeta_system', 'metadata', 'dtbo', 'cust', 'super', 'userdata', ...)
Type:
{GREEN}fastboot flash PatitionName /path/FilePartitionName{RESET}
Example:
fastboot flash super /sdcard/download/super.img

"""

print(message)