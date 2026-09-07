import subprocess
import sys
from rich.console import Console

VERSION = "1.6.0"

console = Console()

ORANGE = "bold color(208)"
WHITE = "bold white"
DIM = "dim"
RED = "bold red"

TOOLS = {
    "1": ("Unlock Bootloader", "miunlock"),
    "2": ("Flash Fastboot ROM.tgz", "miflash"),
    "3": ("Mi Assistant", "miasst"),
    "4": ("Firmware Content Extractor", "fcetool"),
    "5": ("Apply Unlock Permission", "miapply"),
}


def print_header():
    console.print()
    console.print(f"[{ORANGE}]▌[/] [{WHITE}]Mi[/][{ORANGE}]Tool[/]  [{DIM}]v{VERSION}[/]")
    console.print(f"  [{DIM}]offici5l.github.io[/]\n")


def print_menu():
    console.print(f"[{ORANGE}]▌[/] [{WHITE}]Operations[/]\n")
    for key, (desc, _) in TOOLS.items():
        console.print(f"  [{ORANGE}]{key}[/]  {desc}")
    console.print(f"\n  [{ORANGE}]q[/]  Quit\n")


def get_choice():
    if len(sys.argv) > 1:
        return sys.argv[1].lower()
    try:
        return console.input(f"[{ORANGE}]▌[/] [{WHITE}]Choice[/] [{DIM}]›[/] ").strip().lower()
    except (KeyboardInterrupt, EOFError):
        console.print(f"\n[{ORANGE}]Cancelled[/]")
        sys.exit(0)


def main():
    print_header()
    print_menu()

    choice = get_choice()

    if choice in ("q", "quit", "exit"):
        sys.exit(0)

    if choice not in TOOLS:
        console.print(f"[{RED}]✗[/] Invalid choice: {choice}")
        sys.exit(1)

    desc, cmd = TOOLS[choice]
    console.print(f"\n[{ORANGE}]▌[/] {desc}\n")
    subprocess.run(cmd, shell=True)


if __name__ == "__main__":
    main()
