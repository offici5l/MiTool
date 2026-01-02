#!/usr/bin/env python3

import subprocess
import sys
import os

version = "1.5.9"

ORANGE = "\033[38;5;208m"
DIM = "\033[2m"
BOLD = "\033[1m"
RED = "\033[1;31m"
GREEN = "\033[1;32m"
RESET = "\033[0m"

TOOLS = {
    "1": ("Unlock Bootloader", "$PREFIX/bin/miunlock"),
    "2": ("Flash Fastboot ROM", "$PREFIX/bin/miflashf"),
    "3": ("Mi Assistant", "$PREFIX/bin/miasst"),
    "4": ("Firmware Content Extractor", "$PREFIX/bin/mifcetool")
}

try:
    term_width = os.get_terminal_size().columns
except:
    term_width = 80

def get_center(text):
    clean = text.replace(ORANGE, '').replace(RESET, '').replace(DIM, '')
    pad = (term_width - len(clean)) // 2
    return ' ' * pad + text

separator = f"{DIM}{'━' * min(term_width, 70)}{RESET}"

print("\n")
print(get_center(f"{DIM}{'═' * min(term_width, 70)}{RESET}"))

title = f"MiTool v{version}"
box_width = len(title) + 4
print(get_center(f"┏{'━' * (box_width - 2)}┓"))
print(get_center(f"┃  {ORANGE}MiTool{RESET} {DIM}v{version}{RESET}  ┃"))
print(get_center(f"┗{'━' * (box_width - 2)}┛"))

print(get_center(f"{DIM}github.com/offici5l/MiTool{RESET}"))
print(get_center(f"{DIM}{'═' * min(term_width, 70)}{RESET}"))
print()

print(f"{BOLD}Available Operations:{RESET}\n")
for key, (desc, _) in TOOLS.items():
    print(f"  {DIM}▸{RESET} [{ORANGE}{key}{RESET}] {desc}")
print(f"\n  {DIM}▸{RESET} [{ORANGE}q{RESET}] Quit\n")

if len(sys.argv) > 1:
    choice = sys.argv[1].lower()
    print(f"{ORANGE}►{RESET} Selected: {ORANGE}{choice}{RESET}\n")
else:
    try:
        choice = input(f"{BOLD}►{RESET} Enter choice: ").strip().lower()
    except (KeyboardInterrupt, EOFError):
        print(f"\n\n{ORANGE}Cancelled{RESET}")
        sys.exit(0)

if choice in ['q', 'quit', 'exit']:
    print(f"{ORANGE}Exiting...{RESET}\n")
    sys.exit(0)

if choice in TOOLS:
    desc, cmd = TOOLS[choice]
    print(f"\n{ORANGE}►{RESET} Executing: {DIM}{cmd}{RESET}\n")
    print(f"{DIM}{'─' * min(term_width, 70)}{RESET}\n")
    subprocess.run(cmd, shell=True)
else:
    print(f"{RED}✗ Invalid:{RESET} '{choice}'")
    print(f"{DIM}Select 1-4 or 'q' to quit{RESET}\n")
    sys.exit(1)
