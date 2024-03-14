MiTool version 1.4.4:

- Device verification has been added in any mode, automatically restarting it to the appropriate mode

- A trial version for Flashing Fastboot Rom (v2) has been added (only for those facing issues with the following errors: "error: current device antirollback version is greater than this package" or "error: antirollback check error" or "Erase boot error")
Usage: run command: mitool t

- Improved handling of some errors automatically during bootloader unlocking, such as error code 10000, and more..

- delete the region selection request while unlocking the bootloader Let mitool take care of that

- Other improvements and additions


MiTool version 1.4.5:

- to facilitate the bootloader unlocking step:
  Now, when the browser is opened, you don't need to enter login credentials again; you only need to confirm login
(this improvement has been canceled due to some unexpected problems.)




- suggestions or issue reports can now be directly sent to t.me/Offici5l_Group through mitool. with command : m
(this is especially useful for users who do not have a telegram account.)

- other improvements.


MiTool version 1.4.6:

- Improve Flash-Fastboot-ROM and Fastboot-Flash-Rom-V2

- Other improvements



MiTool version 1.4.8 :

- add Bypass HyperOS BootLoader Restrictions

  bypass message "Cloudn't verify, wait a minute or two and try again" for miui and hyperos

- improvements


MiTool version 1.4.9 :

- Improvements:
It is now expected that the securityStatus16 error will not occur. If it does happen, please report it.

- Other improvements

MiTool version 1.5.0 :

- MiTool now directly utilizes MiUnlockTool for bootloader unlocking. If you only need to unlock the bootloader, you can use MiUnlockTool directly without MiTool. ([Changelog](https://github.com/offici5l/MiUnlockTool/blob/main/Show-Version-History.md))

- MiTool now directly utilizes MiBypassTool for bypassing. If you only need to bypass, you can use MiBypassTool directly without MiTool. (Changelog)

- Converted MiTool from mitool.sh to mitool.py.

- Removed many unnecessary features.

- (Some tools have been temporarily disabled.)

- Various improvements.



