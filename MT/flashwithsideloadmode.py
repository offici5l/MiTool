#!/usr/bin/python

import os

def check_mode():
    while True:
        status1 = os.popen("adb get-state 2>/dev/null").read().strip()
        if status1 == "sideload":
            print(f"\n{status1} ok\\n")
            break
        status2 = os.popen("adb get-state 2>/dev/null").read().strip()
        if status2 == "device":
            print(f"\n{status2} mode .. reboot to sideload mode ... wait ..\n\n")
            os.system("adb reboot sideload")
            continue
        status3 = os.popen("fastboot devices 2>/dev/null | awk '{print $NF}'").read().strip()
        if status3 == "fastboot":
            print(f"\n{status3} mode .. reboot to sideload mode\n\n")
            os.system("fastboot reboot")
            continue

result_paths = []

for root, dirs, files in os.walk("/sdcard"):
    if "Android" in root:
        continue

    tgz_files = [f for f in files if f.endswith(".zip")]
    result_paths.extend([os.path.join(root, f) for f in tgz_files])

if result_paths:
    for i, result in enumerate(result_paths, start=1):
        print(f"\n \033[92m{i}\033[0m - {result}\n")
        
    while True:
        try:
            selected_index = int(input(f"\ntype correct \033[92mnumber\033[0m you want to flash: "))
            if 1 <= selected_index <= len(result_paths):
                break
            else:
                print("\nInvalid selection !")
        except ValueError:
            print("\nInvalid input !")

    selected_result = result_paths[selected_index - 1]
    print(f"\nzip selected: \033[92m{selected_result}\033[0m\n\ncheck device it is connected via otg ! ..\n")
    check_mode()
    os.system(f"adb sideload {selected_result}")


if not result_paths:
    print("\n \033[91mNo ROMs.zip found on the device !\033[0m")
    print("\n   Please download or transfer a ROM.zip to your device.\n")
else:
    for i, result in enumerate(result_paths, start=1):
        print(f"\n \033[92m{i}\033[0m - {result}\n")