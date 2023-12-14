import os

print("Flashing Fastboot ROM...")

ROM_FOLDER = "/sdcard/Download/mi-flash-fastboot-rom"

if not os.path.exists(ROM_FOLDER):
    os.makedirs(ROM_FOLDER)

input("Please make sure to place the ROM file in the {} folder .. Then press Enter".format(ROM_FOLDER))

if any(file.endswith((".sh", ".lock.sh")) for file in os.listdir(ROM_FOLDER)):
    flashOption = int(input("Choose an option:\n1. Flash ROM without locking bootloader\n2. Flash ROM with bootloader lock\nEnter the option number: "))

    if flashOption == 1:
        flashAllScript = next((os.path.join(ROM_FOLDER, file) for file in os.listdir(ROM_FOLDER) if file == "flash_all.sh"), None)

        if flashAllScript:
            input("Make sure your device is connected in fastboot mode. Connect your device using OTG, then press Enter when ready.")
            os.system(f"sh {flashAllScript}")
        else:
            print("Could not find flash_all.sh file.")
            exit(1)
    elif flashOption == 2:
        flashAllLockScript = next((os.path.join(ROM_FOLDER, file) for file in os.listdir(ROM_FOLDER) if file == "flash_all_lock.sh"), None)

        if flashAllLockScript:
            input("Make sure your device is connected in fastboot mode. Connect your device using OTG, then press Enter when ready.")
            os.system(f"sh {flashAllLockScript}")
        else:
            print("Could not find flash_all_lock.sh file.")
            exit(1)
    else:
        print("Invalid option")
        exit(1)
else:
    tgzFile = next((os.path.join(ROM_FOLDER, file) for file in os.listdir(ROM_FOLDER) if file.endswith(".tgz")), None)

    if tgzFile:
        print("ROM file detected in mi-flash-fastboot-rom folder.")
        print("The ROM file is being decompressed, please wait")
        os.system(f"pv {tgzFile} | tar --strip-components=1 -xzf- -C {ROM_FOLDER}/ --wildcards --no-anchored 'flash_all.sh' 'flash_all_lock.sh' 'images'")
    else:
        print("No .tgz file detected, assuming ROM files are already uncompressed.")

    if any(file.endswith((".sh", ".lock.sh")) for file in os.listdir(ROM_FOLDER)):
        flashOption = int(input("Choose an option:\n1. Flash ROM without locking bootloader\n2. Flash ROM with bootloader lock\nEnter the option number: "))

        if flashOption == 1:
            flashAllScript = next((os.path.join(ROM_FOLDER, file) for file in os.listdir(ROM_FOLDER) if file == "flash_all.sh"), None)

            if flashAllScript:
                input("Make sure your device is connected in fastboot mode. Connect your device using OTG, then press Enter when ready.")
                os.system(f"sh {flashAllScript}")
            else:
                print("Could not find flash_all.sh file.")
                exit(1)
        elif flashOption == 2:
            flashAllLockScript = next((os.path.join(ROM_FOLDER, file) for file in os.listdir(ROM_FOLDER) if file == "flash_all_lock.sh"), None)

            if flashAllLockScript:
                input("Make sure your device is connected in fastboot mode. Connect your device using OTG, then press Enter when ready.")
                os.system(f"sh {flashAllLockScript}")
            else:
                print("Could not find flash_all_lock.sh file.")
                exit(1)
        else:
            print("Invalid option")
            exit(1)
    else:
        print("No Rom file detected in mi-flash-fastboot-rom folder. Please make sure to place the ROM file in the mi-flash-fastboot-rom folder.")
        exit(1)
