import os

print("Flashing Recovery ROM...")

ROM_FOLDER = "/sdcard/Download/mi-flash-recovery-rom"

if not os.path.exists(ROM_FOLDER):
    os.makedirs(ROM_FOLDER)

input("Please make sure to place the ROM file in the {} folder .. Then press Enter".format(ROM_FOLDER))

rom_files = [f for f in os.listdir(ROM_FOLDER) if f.endswith(".zip")]

if rom_files:
    input("\nMake sure your device is in sideload mode. Connect your device using OTG, then press Enter when ready\n")
else:
    print("Could not find rom.zip file.")
    exit(1)

while True:
    status = os.popen("adb get-state").read().strip()
    print(status)
    if status == "sideload":
        break
    else:
        input("\nplease Verify that device is in sideload mode ! If so, check that it is connected via otg ! then press Enter\n")
        continue

os.system("adb sideload {}/{}".format(ROM_FOLDER, rom_files[0]))