import os
import sys

if len(sys.argv) != 2:
    flash_type = input("\nEnter type img you want to flash (recovery/boot/vbmeta/vbmeta_system/metadata/metadata/dtbo/cust/super/userdata): ").lower()
    if flash_type not in ["recovery", "boot", "vbmeta", "vbmeta_system", "metadata", "dtbo", "cust", "super", "userdata"]:
        print("\nInvalid input!\n")
        sys.exit(1)
else:
    flash_type = sys.argv[1].lower()
    if flash_type not in ["recovery", "boot", "vbmeta", "vbmeta_system", "metadata", "dtbo", "cust", "super", "userdata"]:
        print("Invalid image type!")
        sys.exit(1)


result_paths = []

for root, dirs, files in os.walk("/sdcard"):
    if "Android" in root:
        continue

    img_files = [f for f in files if f.endswith(".img")]
    result_paths.extend([os.path.join(root, f) for f in img_files])

if not result_paths:
    print("No '.img' files found.")
    exit()

for i, result in enumerate(result_paths, start=1):
    print(f"\n \033[92m{i}\033[0m - {result}\n")

while True:
    try:
        selected_index = int(input(f"\nType the correct \033[92mnumber\033[0m for {flash_type} you want to flash: "))
        if 1 <= selected_index <= len(result_paths):
            break
        else:
            print("\nInvalid selection!")
    except ValueError:
        print("\nInvalid input!")

selected_result = result_paths[selected_index - 1]

print(f"\nImg selected: \033[92m{selected_result}\033[0m\n\nCheck if the device is connected via OTG! ..\n")

os.system(f"fastboot flash {flash_type} {selected_result}")