import os
import sys

text = "\n\033[92mMake sure your device is connected in fastboot mode. Connect your device using OTG, then press Enter when ready.\033[0m\n"

def check_fastboot_mode():
    while True:
        status = os.popen("fastboot devices | grep -o 'fastboot'").read().strip()
        if status == "fastboot":
            break
        else:
            input("\nVerify that the device is in fastboot mode! If so, check that it is connected via OTG! Then press Enter\n")
            continue


def flash_selected_result(selected_result):
    if any(file.endswith(("flash_all.sh", "flash_all_lock.sh")) for file in os.listdir(selected_result)):
        flashOption = int(input("\nChoose an option:\n\n\033[92m1 -\033[0m Flash without locking bootloader\n\033[92m2 -\033[0m Flash with lock bootloader\n\nEnter the option number: "))

        if flashOption == 1:
            input(text)
            check_fastboot_mode()
            flash = "flash_all.sh"
            os.system(f"sh {selected_result}/{flash}")
        elif flashOption == 2:
            input(text)
            check_fastboot_mode()
            flash_lock = "flash_all_lock.sh"
            os.system(f"sh {selected_result}/{flash_lock}")
        else:
            print("\nInvalid option\n")
            exit(1)
    else:
        print("\ninvalid directory 'exit'\n")
        exit(1)

def decompress_and_flash_rom(tgz_file_name):
    ROM_FOLDER = "/sdcard/Download/mi-flash-fastboot-rom"
    
    if not os.path.exists(ROM_FOLDER):
        os.makedirs(ROM_FOLDER)

    print(f"\n\033[92mdecompressed..., please wait\033[0m\n")
    
    os.system(f"pv -bpe {tgz_file_name} | tar --strip-components=1 -xzf- -C {ROM_FOLDER}/ --wildcards --no-anchored 'flash_all.sh' 'flash_all_lock.sh' 'images' 2>/dev/null")
    
    if any(file.endswith(("flash_all.sh", "flash_all_lock.sh")) for file in os.listdir(ROM_FOLDER)):
        flashOption = int(input("\nChoose an option:\n\n\033[92m1 -\033[0m Flash without locking bootloader\n\033[92m2 -\033[0m Flash with lock bootloader\n\nEnter the option number: "))

        if flashOption == 1:
            input(text)
            check_fastboot_mode()
            flash = "flash_all.sh"
            os.system(f"sh {ROM_FOLDER}/{flash}")
        elif flashOption == 2:
            input(text)
            check_fastboot_mode()
            flash_lock = "flash_all_lock.sh"
            os.system(f"sh {ROM_FOLDER}/{flash_lock}")
        else:
            print("\nInvalid option\n")
            exit(1)
    else:
        print("\ninvalid tgz 'exit'\n")
        exit(1)


while True:
    if len(sys.argv) < 2:
        target_name = input("\n\033[92mEnter target name\033[0m: ")
    else:
        target_name = sys.argv[1]

    if target_name:
        break

result_paths = []
for root, dirs, files in os.walk("/sdcard"):
    if target_name in files or target_name in dirs:
        result_paths.append(os.path.join(root, target_name))

if result_paths:
    for i, result in enumerate(result_paths, start=1):
        print(f"\n \033[92m{i}\033[0m - {result}\n")

    while True:
        try:
            selected_index = int(input(f"\nEnter correct \033[92mnumber\033[0m for confirmation: "))
            if 1 <= selected_index <= len(result_paths):
                break
            else:
                print("\nInvalid selection !")
        except ValueError:
            print("\nInvalid input !")

    selected_result = result_paths[selected_index - 1]

    if selected_result.endswith(".tgz"):
        decompress_and_flash_rom(selected_result)        
    elif os.path.isdir(selected_result):
        flash_selected_result(selected_result)
    elif os.path.isfile(selected_result):
        print(f"\n'{selected_result}' is not .tgz file\n")
        exit()
    else:
        print(f"\nUnable to determine the type of {selected_result} \n")
else:
    print(f"Result '{target_name}' not found")
    exit()