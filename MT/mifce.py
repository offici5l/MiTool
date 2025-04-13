#!/usr/bin/python

import requests, json

print("\n\033[1;36m\nGet file.img from a ROM without downloading the ROM!\n")
print("*Firmware-Content-Extractor* is here to help:\n")
print("➤ Step 1: Analyzes the ROM on external servers")
print("➤ Step 2: Provides you with a direct download link")
print("\n✨ **Saving both data and time** by avoiding the download of large ROM files!\n\033[0m\n")

c1="\033[1;32m"
c2="\033[0m"

response = requests.get("https://raw.githubusercontent.com/offici5l/Firmware-Content-Extractor/main/option.json")
data = json.loads(response.text)
formatted = ', '.join(f'"{item}"' for item in data)
print(formatted)

urll = input("\nEnter the https://firmware.zip URL\n: ").strip()
url = f"https://fce.offici5l.workers.dev?url={urll}"
response = requests.get(url)
print(response.text)