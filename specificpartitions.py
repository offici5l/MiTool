import os
import sys

while True:
    if len(sys.argv) < 2:
        target_filename = input("\nEnter target file name: ")
    else:
        target_filename = sys.argv[1]

    if target_filename:
        break 

file_paths = []
for root, dirs, files in os.walk("/sdcard"):
    if target_filename in files:
        file_paths.append(os.path.join(root, target_filename))

if file_paths:
    for i, file in enumerate(file_paths, start=1):
        print(f"{i}. {file}")

    while True:
        try:
            selected_index = int(input("\nEnter the number corresponding to the correct file For confirmation: "))
            if 1 <= selected_index <= len(file_paths):
                break
            else:
                print("\nInvalid selection. Please enter a valid number\n")
        except ValueError:
            print("\nInvalid input. Please enter a valid number\n")

    selected_file = file_paths[selected_index - 1]
    print(f"\nSelected file '{selected_file}'\n")
else:
    print(f"file {file_paths} not found")
    exit()

input("\nMake sure your device is in fastboot mode. Connect your device using OTG, then press Enter when ready\n")

while True:
    status = os.popen("fastboot devices | grep -o 'fastboot'").read().strip()
    if status == "fastboot":
        break
    else:
        input("\nVerify that the device is in fastboot mode! If so, check that it is connected via OTG! Then press Enter\n")
        continue

if os.path.isfile(selected_file):
    print(f"\nflashing {selected_file} ...\n")


    if selected_file.endswith("crclist.txt"):
        os.system(f"fastboot flash crclist {selected_file}")
    elif selected_file.endswith("sparsecrclist.txt"):
        os.system(f"fastboot flash sparsecrclist {selected_file}")
    elif selected_file.endswith("xbl.elf"):
        os.system(f"fastboot flash xbl {selected_file}")
    elif selected_file.endswith("xbl_config.elf"):
        os.system(f"fastboot flash xbl_config {selected_file}")
    elif selected_file.endswith("rpm.mbn"):
        os.system(f"fastboot flash rpm {selected_file}")
    elif selected_file.endswith("tz.mbn"):
        os.system(f"fastboot flash tz {selected_file}")
    elif selected_file.endswith("hyp.mbn"):
        os.system(f"fastboot flash hyp {selected_file}")
    elif selected_file.endswith("featenabler.mbn"):
        os.system(f"fastboot flash featenabler {selected_file}")
    elif selected_file.endswith("NON-HLOS.bin"):
        os.system(f"fastboot flash modem {selected_file}")
    elif selected_file.endswith("BTFM.bin"):
        os.system(f"fastboot flash bluetooth {selected_file}")
    elif selected_file.endswith("abl.elf"):
        os.system(f"fastboot flash abl {selected_file}")
    elif selected_file.endswith("dspso.bin"):
        os.system(f"fastboot flash dsp {selected_file}")
    elif selected_file.endswith("km4.mbn"):
        os.system(f"fastboot flash keymaster {selected_file}")
    elif selected_file.endswith("boot.img"):
        os.system(f"fastboot flash boot {selected_file}")
    elif selected_file.endswith("cmnlib.mbn"):
        os.system(f"fastboot flash cmnlib {selected_file}")
    elif selected_file.endswith("cmnlib64.mbn"):
        os.system(f"fastboot flash cmnlib64 {selected_file}")
    elif selected_file.endswith("devcfg.mbn"):
        os.system(f"fastboot flash devcfg {selected_file}")
    elif selected_file.endswith("qupv3fw.elf"):
        os.system(f"fastboot flash qupfw {selected_file}")
    elif selected_file.endswith("vbmeta.img"):
        os.system(f"fastboot flash vbmeta {selected_file}")
    elif selected_file.endswith("vbmeta_system.img"):
        os.system(f"fastboot flash vbmeta_system {selected_file}")
    elif selected_file.endswith("recovery.img"):
        os.system(f"fastboot flash recovery {selected_file}")
    elif selected_file.endswith("metadata.img"):
        os.system(f"fastboot flash metadata {selected_file}")
    elif selected_file.endswith("dtbo.img"):
        os.system(f"fastboot flash dtbo {selected_file}")
    elif selected_file.endswith("imagefv.elf"):
        os.system(f"fastboot flash imagefv {selected_file}")
    elif selected_file.endswith("uefi_sec.mbn"):
        os.system(f"fastboot flash uefisecapp {selected_file}")
    elif selected_file.endswith("logfs_ufs_8mb.bin"):
        os.system(f"fastboot flash logfs {selected_file}")
    elif selected_file.endswith("storsec.mbn"):
        os.system(f"fastboot flash storsec {selected_file}")
    elif selected_file.endswith("multi_image.mbn"):
        os.system(f"fastboot flash multiimgoem {selected_file}")
    elif selected_file.endswith("cache.img"):
        os.system(f"fastboot flash cache {selected_file}")
    elif selected_file.endswith("super.img"):
        os.system(f"fastboot flash super {selected_file}")
    elif selected_file.endswith("userdata.img"):
        os.system(f"fastboot flash userdata {selected_file}")
    elif selected_file.endswith("cust.img"):
        os.system(f"fastboot flash cust {selected_file}")
    else:
        print("Unknown file type.")