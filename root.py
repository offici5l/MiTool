import os

download_path = "/sdcard/Download/rmagisk"

os.makedirs(download_path, exist_ok=True)

has_magisk = input("\nDo you want to download Magisk? (y/n): ")

if has_magisk == "n":
    input(f"\nPlease copy Magisk to {download_path}. Then press Enter")
    for file in os.listdir(download_path):
        if file.endswith(".apk"):
            new_file = os.path.join(download_path, f"{os.path.splitext(file)[0]}.zip")
            os.rename(os.path.join(download_path, file), new_file)
            print(f"File {file} converted to {new_file}")
elif has_magisk == "y":
    versions = os.popen("curl -s https://api.github.com/repos/topjohnwu/Magisk/releases | grep 'tag_name' | cut -d '\"' -f 4 | grep -v 'manager-'").read().strip().split("\n")
    print("Available versions:")
    print("\n".join(versions))
    selected_version = input("\nPlease choose the version you want to download: ")
    os.system(f"curl -L -o {download_path}/Magisk-{selected_version}.zip https://github.com/topjohnwu/Magisk/releases/download/{selected_version}/Magisk-{selected_version}.apk")
    print(f"Version {selected_version} downloaded successfully to {download_path}")
else:
    print("\nInvalid choice")
    exit(1)

input("\nMake sure your device is in sideload mode. Connect your device using OTG, then press Enter when ready\n")

while True:
    status = os.popen("adb get-state").read().strip()
    print(status)
    if status == "sideload":
        break
    else:
        input("\nplease Verify that device is in sideload mode ! If so, check that it is connected via otg ! then press Enter\n")
        continue

os.system(f"adb sideload {download_path}/*.zip")

