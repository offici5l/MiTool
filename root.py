import os

print("\nFlashing root with fastboot mode...\n")

R_FOLDER = "/sdcard/Download/mi-flash-root"

if not os.path.exists(R_FOLDER):
    os.makedirs(R_FOLDER)

input("\nRequirements: boot.img ,Bootloader unlocked\n\n"
      "1. Download and install Magisk app\n"
      "2. Open Magisk app and press the Install button in the Magisk card\n"
      "3. Choose 'Select and Patch a File' in method, and select the boot.img\n"
      f"4. Copy magisk_patched-*.img to {R_FOLDER}\n"
      "5. If you complete the steps, press Enter\n")

while True:
    img_files = [file for file in os.listdir(R_FOLDER) if file.endswith(".img")]

    if img_files:
        print(f"\nFile found: {img_files[0]}")
        break
    else:
        user_input = input(f"\nNo .img file found in {R_FOLDER}. Please check for the file and press Enter\n")
        continue

input("\nMake sure your device is in fastboot mode. Connect your device using OTG, then press Enter when ready\n")

while True:
    status = os.popen("fastboot devices | grep -o fastboot").read().strip()
    if status == "fastboot":
        break
    else:
        input("\nplease Verify that device is in fastboot mode ! If so, check that it is connected via otg ! then press Enter\n")
        continue

os.system(f"fastboot flash boot {R_FOLDER}/{img_files[0]}")
