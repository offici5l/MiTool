#!/usr/bin/python

import os
import sys
import time
import subprocess

def check_mode():
    spinner = "|/-\\"
    message = "\r device not connected ! "
    while True:
        for char in spinner:
            process = subprocess.Popen(['fastboot', 'devices'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            line = process.stdout.readline()

            if not line and process.poll() is not None:
                sys.stdout.write(message + char + '\r')
                sys.stdout.flush()
                time.sleep(0.1)
                continue

            if "No permission" in line:
                process.terminate()
                sys.stdout.write(message + char + '\r')
                sys.stdout.flush()
                time.sleep(0.1)
                continue

            sys.stdout.write('\r\033[K')
            sys.stdout.flush()
            print("\ndevice is connected\n")
            return

def translate_file_name(file_name):
    translations = {
        "flash_all.sh": "Flash all \033[92mwithout locking bootloader\033[0m",
        "flash_all_lock.sh": "Flash all \033[91mwith lock bootloader\033[0m",
        "flash_all_except_data_storage.sh": "Flash all \033[92mexcept data storage\033[0m",
        "flash_all_except_storage.sh": "Flash all \033[92mexcept storage\033[0m"
    }
    return translations.get(file_name, file_name)

def flash_selected_result(selected_result):
    file_names = ["flash_all.sh", "flash_all_lock.sh", "flash_all_except_data_storage.sh", "flash_all_except_storage.sh"]

    while True:
        found_files = [file for file in os.listdir(selected_result) if file in file_names]

        if found_files:
            for index, file in enumerate(found_files, start=1):
                translated_name = translate_file_name(file)
                print(f"\n \033[92m{index}\033[0m -  {translated_name}")

            choice = input("\nEnter your \033[92mchoice\033[0m: ").strip()

            if not choice.isdigit():
                print("\nInvalid input! Please enter a valid number.\n")
                continue

            choice = int(choice)

            if 1 <= choice <= len(found_files):
                selected_file = found_files[choice - 1]
                [print(char, end='', flush=True) or time.sleep(0.01) for char in "\nEnsure you're in Fastboot mode\n\n"]
                check_mode()
                print("\nFlashing process will start now...\n")
                os.system(f"sh {selected_result}/{selected_file}")
                exit()
            else:
                print(f"\nInvalid choice! Please select a number between 1 and {len(found_files)}.\n")
        else:
            print("\nThe required files were not found!\n")
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

    if os.path.exists(os.path.join(RF, "images")) and any(os.path.exists(os.path.join(RF, file)) for file in ["flash_all_lock.sh", "flash_all.sh", "flash_all_except_data_storage.sh"]):
        flash_selected_result(RF)
    else:
        print("\ninvalid tgz 'exit'\n")
        exit()

target_extension = ".tgz"
target_files = ["flash_all_lock.sh", "flash_all.sh", "flash_all_except_data_storage.sh", "flash_all_except_storage.sh"]
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