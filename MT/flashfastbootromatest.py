import os

def check_mode():
    while True:
        status1 = os.popen("adb get-state 2>/dev/null").read().strip()
        if status1 == "sideload":
            print(f"\n{status1} mode .. reboot to fastboot mode ... wait ..\n\n")
            os.system("adb reboot bootloader")
            continue
        status2 = os.popen("adb get-state 2>/dev/null").read().strip()
        if status2 == "device":
            print(f"\n{status2} mode .. reboot to fastboot mode ... wait ..\n\n")
            os.system("adb reboot bootloader")
            continue
        status3 = os.popen("fastboot devices 2>/dev/null | awk '{print $NF}'").read().strip()
        if status3 == "fastboot":
            print(f"\n{status1} ok\\n")
            break

def modify_file(file_path):
    print("\nDo you have an issue with :\n\n \033[92m1\033[0m - nothing\n \033[92m2\033[0m - erase boot\n \033[92m3\033[0m - antirollback\n \033[92m4\033[0m - erase boot and antirollback\n")

    user_choice = input("\nEnter your \033[92mchoice\033[0m: ")

    with open(file_path, 'r') as file:
        lines = file.readlines()

    if user_choice == '2':
        lines = [line for line in lines if 'fastboot $* erase boot' not in line and 'if [ $? -ne 0 ] ; then echo "Erase boot error"; exit 1; fi' not in line]
        print("\n\nSuccessfully deleted erase boot...\n\n")
    elif user_choice == '3':
        for i, line in enumerate(lines):
            if 'CURRENT_ANTI_VER=' in line:
                current_value = int(line.split('=')[1])
                lines[i] = f'CURRENT_ANTI_VER=9\n'
                print(f"\n\nSuccessfully changed CURRENT_ANTI_VER from {current_value} to 9.\n\n")
                break
    elif user_choice == '4':
        lines = [line for line in lines if 'fastboot $* erase boot' not in line and 'if [ $? -ne 0 ] ; then echo "Erase boot error"; exit 1; fi' not in line]
        for i, line in enumerate(lines):
            if 'CURRENT_ANTI_VER=' in line:
                current_value = int(line.split('=')[1])
                lines[i] = f'CURRENT_ANTI_VER=9\n'
                print(f"\n\nSuccessfully deleted erase boot and changed ANTI VER to 9.\n\n")
                break
    elif user_choice == '1':
        print("\n\nSkip...\n\n")
    else:
        print("\n\nInvalid choice... Skip ..\n\n")

    with open(file_path, 'w') as file:
        file.writelines(lines)

def translate_file_name(file_name):
    translations = {
        "flash_all.sh": "Flash without locking bootloader",
        "flash_all_except_data_storage.sh": "Flash all except data storage"
    }
    return translations.get(file_name, file_name)

def flash_selected_result(selected_result):
    file_names = ["flash_all.sh", "flash_all_except_data_storage.sh"]
    
    while True:
        found_files = [file for file in os.listdir(selected_result) if file in file_names]

        if found_files:
            for index, file in enumerate(found_files, start=1):
                translated_name = translate_file_name(file)
                print(f"\n \033[92m{index}\033[0m -  {translated_name}")
            
            choice = input("\nEnter your \033[92mchoice\033[0m: ")

            try:
                choice = int(choice)
                if 1 <= choice <= len(found_files):
                    selected_file = found_files[choice - 1]
                    translated_file = translate_file_name(selected_file)
                    modify_file(f"{selected_result}/{selected_file}")
                    print("\ncheck device it is connected via OTG ! ...\n")
                    check_mode()
                    os.system(f"sh {selected_result}/{selected_file}")
                    exit()
                else:
                    print("\nInvalid choice !\n")
            except ValueError:
                print("\nInvalid input !\n")
        else:
            print("\nThe required files were not found !\n")
            exit()  


def decompress_and_flash_rom(tgz_file_name):
    RF = "/sdcard/Download/mi-flash-fastboot-rom"
    if not os.path.exists(RF):
        os.makedirs(RF)
    print(f"\n\033[92mdecompressed..., please wait\033[0m\n")
    tar_command = f"pv -bpe '{tgz_file_name}' | tar --strip-components=1 -xzf- -C {RF}/"
    return_code = os.system(tar_command)
    if return_code != 0:
        print(f"\nError during extraction with tar (Exit Code: {return_code})\n")
        exit()

    if os.path.exists(os.path.join(RF, "images")) and any(os.path.exists(os.path.join(RF, file)) for file in ["flash_all.sh", "flash_all_except_data_storage.sh"]):
        flash_selected_result(RF)
    else:
        print("\ninvalid tgz 'exit'\n")
        exit()

target_extension = ".tgz"
target_files = ["flash_all.sh", "flash_all_except_data_storage.sh"]
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

        if any(target_file in dir_files for target_file in target_files) and target_folder in dir_files and any(file in target_files for file in dir_files):
            result_paths.append(dir_path)

if result_paths:
    for i, result in enumerate(result_paths, start=1):
        print(f"\n \033[92m{i}\033[0m - {result}\n")
        
    while True:
        try:
            selected_index = int(input("\nEnter your \033[92mchoice\033[0m: "))
            if 1 <= selected_index <= len(result_paths):
                break
            else:
                print("\nInvalid choice !\n")
        except ValueError:
            print("\nInvalid input !")

    selected_result = result_paths[selected_index - 1]

    if selected_result.endswith(".tgz"):
        decompress_and_flash_rom(selected_result)        
    elif os.path.isdir(selected_result):
        flash_selected_result(selected_result)

else:
    print("\n \033[91mNo ROMs found on the device !\033[0m")
    print("\n   Please download or transfer a ROM to your device.\n")