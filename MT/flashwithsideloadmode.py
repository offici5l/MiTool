import os
import sys

while True:
    if len(sys.argv) < 2:
        target_filename = input("\n\033[92mEnter target name\033[0m: ")
    else:
        target_filename = sys.argv[1]

    if target_filename:
        break 

file_paths = []
for root, dirs, files in os.walk("/sdcard"):
    if target_filename in files:
        file_paths.append(os.path.join(root, target_filename))

if file_paths:
    for i, file in enumerate(file_paths, start=1):
        print(f"{i}. {file}")

    while True:
        try:
            selected_index = int(input("\nEnter the number corresponding to the correct file For confirmation: "))
            if 1 <= selected_index <= len(file_paths):
                break
            else:
                print("\nInvalid selection. Please enter a valid number\n")
        except ValueError:
            print("\nInvalid input. Please enter a valid number\n")

    selected_file = file_paths[selected_index - 1]
    print(f"\nSelected file '{selected_file}'\n")
else:
    print(f"file {file_paths} not found")
    exit()

zipfile = selected_file.endswith(".zip")

if zipfile:
    print(f"\nfile {selected_file} {zipfile} is zip 'ok'\n")
else:
    print(f"\nfile {selected_file} {zipfile} is not zip 'exit'\n")
    exit(1)

input("\nMake sure your device is in sideload mode. Connect your device using OTG, then press Enter when ready\n")

while True:
    status = os.popen("adb get-state").read().strip()
    print(status)
    if status == "sideload":
        break
    else:
        input("\nplease Verify that device is in sideload mode ! If so, check that it is connected via otg ! then press Enter\n")
        continue

os.system(f"adb sideload {selected_file}")
