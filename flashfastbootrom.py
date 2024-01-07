import os

text1 = "\nChoose an option:\n\n\033[92m1 -\033[0m Flash without locking bootloader\n\033[92m2 -\033[0m Flash with lock bootloader\n\033[92m2 -\033[0m Flash all except data storage\n\nEnter the option number: "

text2 = "\n\033[92mMake sure your device is connected in fastboot mode. Connect your device using OTG, then press Enter when ready.\033[0m\n"

def check_fastboot_mode():
    while True:
        status = os.popen("fastboot devices | grep -o 'fastboot'").read().strip()
        if status == "fastboot":
            break
        else:
            input("\nVerify that the device is in fastboot mode! If so, check that it is connected via OTG! Then press Enter\n")
            continue


def flash_selected_result(selected_result):
    flashOption = int(input(text1))

    if flashOption == 1:
        input(text2)
        check_fastboot_mode()
        flash = "flash_all.sh"
        os.system(f"sh {selected_result}/{flash}")
    elif flashOption == 2:
        input(text2)
        check_fastboot_mode()
        flash_lock = "flash_all_lock.sh"
        os.system(f"sh {selected_result}/{flash_lock}")
        elif flashOption == 3:
            input(text2)
            check_fastboot_mode()
            flash_all_except_data_storage = "flash_all_except_data_storage.sh"
            os.system(f"sh {RF}/{flash_all_except_data_storage.sh}")
    else:
        print("\nInvalid option\n")
        exit(1)

def decompress_and_flash_rom(tgz_file_name):
    RF = "/sdcard/Download/mi-flash-fastboot-rom"
    if not os.path.exists(RF):
        os.makedirs(RF)
    print(f"\n\033[92mdecompressed..., please wait\033[0m\n")
    tar_command = f"pv -bpe {tgz_file_name} | tar --strip-components=1 -xzf- -C {RF}/"
    return_code = os.system(tar_command)
    if return_code != 0:
        print(f"\nError during extraction with tar (Exit Code: {return_code})\n")
        exit(1)

    if all(os.path.exists(os.path.join(RF, file)) for file in ["flash_all_lock.sh", "flash_all.sh", flash_all_except_data_storage.sh]) and os.path.exists(os.path.join(RF, "images")):
        flashOption = int(input(text1))
        if flashOption == 1:
            input(text2)
            check_fastboot_mode()
            flash = "flash_all.sh"
            os.system(f"sh {RF}/{flash}")
        elif flashOption == 2:
            input(text2)
            check_fastboot_mode()
            flash_lock = "flash_all_lock.sh"
            os.system(f"sh {RF}/{flash_lock}")
        elif flashOption == 3:
            input(text2)
            check_fastboot_mode()
            flash_all_except_data_storage = "flash_all_except_data_storage.sh"
            os.system(f"sh {RF}/{flash_all_except_data_storage.sh}")
        else:
            print("\nInvalid option\n")
            exit(1)
    else:
        print("\ninvalid tgz 'exit'\n")
        exit(1)

target_extension = ".tgz"
target_files = ["flash_all_lock.sh", "flash_all.sh"]
target_folder = "images"

result_paths = []

for root, dirs, files in os.walk("/sdcard"):
    if "Android" in root:
        continue

    tgz_files = [f for f in files if f.endswith(target_extension)]
    result_paths.extend([os.path.join(root, f) for f in tgz_files])

    for dir_name in dirs:
        dir_path = os.path.join(root, dir_name)
        dir_files = set(os.listdir(dir_path))

        if all(target_file in dir_files for target_file in target_files) and target_folder in dir_files:
            result_paths.append(dir_path)

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

    if selected_result.endswith(".tgz"):
        decompress_and_flash_rom(selected_result)        
    elif os.path.isdir(selected_result):
        flash_selected_result(selected_result)

