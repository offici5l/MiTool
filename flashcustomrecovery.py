import os
import zipfile

print("\nFlashing Custom Recovery...\n")

C_FOLDER = "/sdcard/Download/mi-flash-CustomRecovery"

if not os.path.exists(C_FOLDER):
    os.makedirs(C_FOLDER)

input("\nMake sure to place the recovery file in the {} folder, then press Enter\n".format(C_FOLDER))

while True:
    img_files = [f for f in os.listdir(C_FOLDER) if f.endswith(".img")]
    zip_files = [f for f in os.listdir(C_FOLDER) if f.endswith(".zip")]

    if img_files:
        break
    elif zip_files:
        zip_file = os.path.join(C_FOLDER, zip_files[0])
        recovery_img = "recovery.img"
        
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extract(recovery_img, C_FOLDER)
        
        break
    else:
        input("\nPlease make sure to place the recovery file in the {} folder, then press Enter\n".format(C_FOLDER))
        continue

input("\nMake sure your device is in fastboot mode. Connect your device using OTG, then press Enter when ready\n")

while True:
    status = os.popen("fastboot devices | grep -o 'fastboot'").read().strip()
    if status == "fastboot":
        break
    else:
        input("\nVerify that the device is in fastboot mode! If so, check that it is connected via OTG! Then press Enter\n")
        continue

os.system("fastboot flash recovery {}/{}".format(C_FOLDER, [f for f in os.listdir(C_FOLDER) if f.endswith(".img")][0]))