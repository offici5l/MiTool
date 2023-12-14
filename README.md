<div align="center">

<h1> MiTool</h1>

without pc(with termux)

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](./LICENSE) [![channel icon](https://img.shields.io/badge/-telegram-red?color=white&logo=telegram&logoColor=blue)](https://t.me/Offici5l_Channel)

<div align="left">

### Description:
<sub>- MiTool is a tool to retrieve the encryptData(token) for Xiaomi devices, with `unlockbootloader.py`, which requires essential packages such as Python, pycryptodomex, and requests.. These packages will be installed via the `install.sh`.</sub>

<sub>- To obtain device product and device token and unlocking process, we need `fastboot` tool sourced from [nohajc](https://github.com/nohajc/termux-adb). will also be installed using `install.sh`</sub>

[Additionally](#to-do-list), MiTool includes simple features, such as the ability to flash Fastboot ROM and Recovery ROM with `flashrecoveryrom.py` and `flashfastbootrom.py`

<div align="left">

# Install

<b>1.Install </b> <a href="https://github.com/termux/termux-app/releases">Termux</a>

<b>2.Install </b> <a href="https://github.com/termux/termux-api/releases/download/v0.50.1/termux-api_v0.50.1+github-debug.apk">Termux API</a>

3.From termux command line:


  ```bash
termux-setup-storage
  ```
  ```bash
pkg install git && git clone https://github.com/offici5l/MiTool && cd MiTool && bash install.sh
  ```

**Usage:**
run command:
```bash
mitool
```


### To-Do List

- [x] [Flash Fastboot ROM]. command:`mitool (Then choose number 1)`
- [x] [Flash Recovery Rom]. command:`mitool (Then choose number 2)`
- [x] [Unlock Xiaomi Bootloader]. command:`mitool (Then choose number 3)`
- [x] [root device]. command:`adb sideload patch/Magisk.zip`
