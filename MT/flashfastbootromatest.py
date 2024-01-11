import os
import sys
import requests

print(f"\n- Fastboot-Flash-Rom-V2")

print("\nThis version is designed for those encountering the following issues:")
print("1. error: current device antirollback version is greater than this package")
print("2. error: antirollback check error")
print("3. Erase boot error\n")

print(f"\n(\033[91mFastboot-Flash-Rom-V2 it's a trial version! please be aware that this is an experimental release. By continuing, you assume responsibility for any problems that may occur on your device\033[0m)")

while True:
    choice = input("\ntype 1 to continue type 2 to exit : ")
    if choice == "1":
        break
    if choice == "2":
        exit()
def send_log_to_telegram():
    log_path = '/sdcard/Download/mitoollog.text'

    if not os.path.isfile(log_path):
        print(f"\nLog file '{log_path}' not found. Exiting...\n")
        exit()

    while True:
        user_input = input(f"\nlog: {log_path}\n\nSend log to t.me/Offici5l_Group? (yes/no): ")

        if user_input.lower() == 'yes':
            file_size = os.path.getsize(log_path)
            send_method = 'Document' if file_size > 500 else 'Message'

            with open(log_path, 'rb' if send_method == 'Document' else 'r') as file:
                payload = {'chat_id': -1002017234802}
                if send_method == 'Document':
                    files = {'document': (log_path, file)}
                else:
                    payload['text'] = f'\n[flash-fastboot-rom-miui (a test)]:\n\ninfo device:\n\n{file.read()}'

                response = requests.post(
                    f'https://api.telegram.org/bot6772941553:AAHZ-ICe-4zeLWil2VYv4_WOgoDSD3Haz9o/send{send_method}',
                    data=payload,
                    files=files if send_method == 'Document' else None
                )

            if response.status_code == 200:
                print(f'\n{send_method} sent successfully! to t.me/Offici5l_Group\n')
            else:
                print(f'\nFailed to send {send_method} to t.me/Offici5l_Group. Status code: {response.status_code}\n')
            break
        elif user_input.lower() == 'no':
            exit()
        else:
            print('\nInvalid input. Please enter "yes" or "no".\n')



def get_fvm(fmisc):
    output_file = "/sdcard/Download/mitoollog.text"

    c = [
        "product",
        "unlocked",
        "rollback_ver",
        "partition-type:boot",
        "parallel-download-flash"
    ]

    rs = [os.popen(f"fastboot getvar {cmd} 2>&1 | grep \"{cmd}:\"").read() for cmd in c]
    results = [result.strip() for result in rs]

    try:
        with open(fmisc, "r") as fmisc_file:
            misc_content = fmisc_file.read().strip()
        results.append("\n#####\n\nInfo rom:\n\n" + misc_content + "\n\n#####\n\nlog cmd:\n")
    except FileNotFoundError:
        results.append(f"File '{fmisc}' not found, continuing without it.")

    with open(output_file, "w") as output_file:
        for result in results:
            output_file.write(result + "\n")
    
def run_command(selected_result, target):
    command = f"sh {selected_result}/{target} 2>&1 | tee -a /sdcard/Download/mitoollog.text"
    os.system(command)
    send_log_to_telegram()

def modify_file(file_path):
    try:
        with open(file_path, 'r+') as file:
            content = file.read()
            start_pattern_1 = 'CURRENT_ANTI_VER'
            end_pattern_1 = 'current device antirollback version is greater than this package" ; exit 1 ; fi'

            start_index_1 = content.find(start_pattern_1)
            end_index_1 = content.find(end_pattern_1, start_index_1) + len(end_pattern_1)

            pattern_2 = 'fastboot $* erase boot\nif [ $? -ne 0 ] ; then echo "Erase boot error"; exit 1; fi'

            if start_index_1 != -1 and end_index_1 != -1:
                content = content[:start_index_1] + content[end_index_1:]
                print("\nText section 1 found and removed...\033[92mdone\033[0m\n")
            else:
                print("\nText section 1 not found...\033[92mok\033[0m\n")

            if pattern_2 in content:
                content = content.replace(pattern_2, '')
                print("Text section 2 found and removed...\033[92mdone\033[0m\n")
            else:
                print("Text section 2 not found...\033[92mok\033[0m\n")

            file.seek(0)
            file.write(content)
            file.truncate()

    except FileNotFoundError:
        print(f"\nFile '{file_path}' not found. Exiting...")
        sys.exit()


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


text1 = "\nChoose an option:\n\n\033[92m1 -\033[0m Flash without locking bootloader\n\033[92m2 -\033[0m Flash with lock bootloader\n\033[92m3 -\033[0m Flash all except data storage\n\nEnter the option number: "

text2 = "\ncheck device it is connected via OTG! ...\n"


def flash_selected_result(selected_result):
    flashOption = int(input(text1))

    if flashOption == 1:
        Check1 = "flash_all.sh"
        modify_file(f"{selected_result}/{Check1}")
        print(text2)
        check_mode()
        get_fvm(f"{selected_result}/misc.txt")
        run_command(f"{selected_result}", f"{Check1}")
    elif flashOption == 2:
        Check2 = "flash_all_lock.sh"
        modify_file(f"{selected_result}/{Check2}")
        print(text2)
        check_mode()
        get_fvm(f"{selected_result}/misc.txt")
        run_command(f"{selected_result}", f"{Check2}")
    elif flashOption == 3:
        Check3 = "flash_all_except_data_storage.sh"
        modify_file(f"{selected_result}/{Check3}")
        print(text2)
        check_mode()
        get_fvm(f"{selected_result}/misc.txt")
        run_command(f"{selected_result}", f"{Check3}")
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

    if all(os.path.exists(os.path.join(RF, file)) for file in ["flash_all_lock.sh", "flash_all.sh", "flash_all_except_data_storage.sh"]) and os.path.exists(os.path.join(RF, "images")):
        flashOption = int(input(text1))

        if flashOption == 1:
            Check1 = "flash_all.sh"
            modify_file(f"{RF}/{Check1}")
            print(text2)
            check_mode()
            get_fvm(f"{RF}/misc.txt")
            run_command(f"{RF}", f"{Check1}")
        elif flashOption == 2:
            Check2 = "flash_all_lock.sh"
            modify_file(f"{RF}/{Check2}")
            print(text2)
            check_mode()
            get_fvm(f"{RF}/misc.txt")
            run_command(f"{RF}", f"{Check2}")
        elif flashOption == 3:
            Check3 = "flash_all_except_data_storage.sh"
            modify_file(f"{RF}/{Check3}")
            print(text2)
            check_mode()
            get_fvm(f"{RF}/misc.txt")
            run_command(f"{RF}", f"{Check3}")
        else:
            print("\nInvalid option\n")
            exit(1)
    else:
        print("\ninvalid tgz 'exit'\n")
        exit(1)

target_extension = ".tgz"
target_files = ["flash_all_lock.sh", "flash_all.sh", "flash_all_except_data_storage.sh"]
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