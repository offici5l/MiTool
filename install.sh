#!/data/data/com.termux/files/usr/bin/bash

set -e

R='\033[0;31m'
G='\033[0;32m'
N='\033[0m'

TOTAL_STEPS=7
STEP=0

run_step() {
    STEP=$((STEP + 1))
    local msg="$1" cmd="$2" output

    printf "[%d/%d] %s... " "$STEP" "$TOTAL_STEPS" "$msg"

    if output=$(bash -c "$cmd" 2>&1); then
        echo -e "${G}✔${N}"
    else
        echo -e "${R}✘${N}"
        echo -e "${R}Error occurred during: $msg${N}"
        echo "$output"
        exit 1
    fi
}

echo

arch=$(dpkg --print-architecture)
if [[ "$arch" != "aarch64" && "$arch" != "arm" ]]; then
    echo "MiTool does not support architecture $arch"
    exit 1
fi

if [ ! -d "$HOME/storage" ]; then
    echo -e "\nGrant permission: termux-setup-storage\nThen rerun the command.\n"
    exit 1
fi

if ! cmd package list packages --user 0 com.termux.api < /dev/null 2>/dev/null | grep -q 'com.termux.api'; then
    echo -e "\ncom.termux.api app is not installed\nPlease install it first\n"
    exit 1
fi

run_step "Updating system & fixing broken packages" \
    "yes | apt --fix-broken install && yes | apt update && yes | apt upgrade"

run_step "Installing Python3" \
    "yes | pkg install python3"

run_step "Installing python-pip" \
    "yes | pkg install python-pip"

run_step "Installing libusb" \
    "yes | pkg install libusb"

run_step "Installing termux-api" \
    "yes | pkg install termux-api"

run_step "Installing termux-adb" \
    "curl -fsS https://raw.githubusercontent.com/nohajc/termux-adb/master/install.sh | bash && ln -sf \$PREFIX/bin/termux-fastboot \$PREFIX/bin/fastboot && ln -sf \$PREFIX/bin/termux-adb \$PREFIX/bin/adb"

run_step "Installing mitool" \
    "pip install -U pymitool"

echo -e "\n${G}✔ Installation completed successfully${N}"
echo -e "\nRun command: ${G}mitool${N}\n"