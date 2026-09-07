<div align="center">

  <a href="https://github.com/MiForge/MiTool"><img src="https://img.shields.io/badge/MiTool-%23FF6900?style=flat&logo=xiaomi&logoColor=white" alt="MiTool" style="width: 200px; vertical-align: middle;" /></a><br>


  Windows, macOS, Linux, and Termux.

  [![Version](https://img.shields.io/pypi/v/pymitool?label=Version&labelColor=black&color=brightgreen)](https://pypi.org/project/pymitool/)
  [![Changelog](https://img.shields.io/badge/Changelog-blue?style=flat)](CHANGELOG.md)
  [![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](./LICENSE)
  ___

</div>

___

### Dependencies

* Linux: `sudo apt install libusb-1.0-0`
* macOS: `brew install libusb`
* Termux: `pkg install libusb`
* Windows: No extra steps required (uses standard USB drivers).

### Install

```bash
pip install pymitool
```

### Usage

```bash
mitool
```

## Notes

On Termux (without root) you'll need the [Termux:API](https://github.com/termux/termux-api/releases/latest) app, and `pkg install termux-api`.

### Quick Installation (for Termux):

```sh
curl -sS https://raw.githubusercontent.com/MiForge/MiTool/main/install.sh | bash
```
