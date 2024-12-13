#!/usr/bin/python

import requests

print("\n\033[1;36m\nGet file.img from a ROM without downloading the ROM!\n")
print("*Firmware-Content-Extractor* is here to help:\n")
print("➤ Step 1: Analyzes the ROM on external servers")
print("➤ Step 2: Provides you with a direct download link")
print("\n✨ **Saving both data and time** by avoiding the download of large ROM files!\n\033[0m\n")

c1="\033[1;32m"
c2="\033[0m"

while True:

    print("\nGet:\n")
    print(f"  ━ {c1}1{c2} boot.img")
    print(f"  ━ {c1}2{c2} init_boot.img")

    choice = input(f"\nEnter your {c1}choice{c2}: ").strip()

    option_map = {"1": "boot_img", "2": "init_boot_img"}

    if choice in option_map:
        option = option_map[choice]
        break
    else:
        print("\nInvalid choice !\n")

while True:

    url = input("\nEnter the firmware URL\n    (Recovery/Custom Rom): ").strip()

    if url.startswith("http"):
        break
    else:
        print("\nInvalid URL. Please enter a valid URL starting with http:// or https://\n")


url = f"https://fce.offici5l.workers.dev?get={option}&url={url}"

response = requests.get(url)

print(response.text)