#!/data/data/com.termux/files/usr/bin/bash

echo

if [ ! -d "$HOME/storage" ]; then
    echo -e "\nGrant permission: termux-setup-storage\nThen rerun the command.\n"
    exit 1
fi

if ! cmd package list packages com.termux.api 2>/dev/null | grep -q 'com.termux.api'; then
    echo -e '\ncom.termux.api app is not installed\nPlease install it first\n'
    exit 1
fi

arch=$(dpkg --print-architecture)

if [[ "$arch" != "aarch64" && "$arch" != "arm" ]]; then
    echo "MiTool does not support architecture $arch"
    exit 1
fi

mitoolusers="$PREFIX/bin/.mitoolusersok"
miunlockusers="$PREFIX/bin/.miunlockusersok"

if [ ! -f "$mitoolusers" ]; then
    if [ ! -f "$miunlockusers" ]; then
        echo -ne "\rapt upgrade ..."
        apt upgrade > /dev/null 2> >(grep -v "apt does not have a stable CLI interface")
    fi
    curl -Is https://github.com/offici5l/MiTool/releases/download/tracking/totalusers> /dev/null 2>&1
    touch "$mitoolusers"
fi

echo -ne "\rurl check ..."

main_repo=$(grep -E '^deb ' /data/data/com.termux/files/usr/etc/apt/sources.list | awk '{print $2}' | head -n 1)

curl -s --retry 4 $main_repo > /dev/null
exit_code=$?

if [ $exit_code -eq 6 ]; then
    echo -e "\nRequest to $main_repo failed. Please check your internet connection.\n"
    exit 6
elif [ $exit_code -eq 35 ]; then
    echo -e "\nThe $main_repo is blocked in your current country.\n"
    exit 35
fi

git_repo="https://raw.githubusercontent.com"

curl -s --retry 4 $git_repo > /dev/null
exit_code=$?

if [ $exit_code -eq 6 ]; then
    echo -e "\nRequest to $git_repo failed. Please check your internet connection.\n"
    exit 6
elif [ $exit_code -eq 35 ]; then
    echo -e "\nThe $git_repo is blocked in your current country.\n"
    exit 35
fi

echo -ne "\rapt update ..."
apt update > /dev/null 2> >(grep -v "apt does not have a stable CLI interface")

charit=-1
total=31
start_time=$(date +%s)

_progress() {
    charit=$((charit + 1)) 
    percentage=$((charit * 100 / total))
    echo -ne "\rProgress: $charit/$total ($percentage%)"
    if [ $percentage -eq 100 ]; then
        end_time=$(date +%s)
        elapsed_time=$((end_time - start_time))
        echo -ne "\rProgress: $charit/$total ($percentage%) Took: $elapsed_time seconds"
    else
        echo -ne "\rProgress: $charit/$total ($percentage%)"
    fi
}

_progress

url="https://raw.githubusercontent.com/nohajc/nohajc.github.io/master/dists/termux/extras/binary-${arch}"

get_version() {
  package_name="$1"
  local __resultvar=$2

  version=$(curl -s "$url/Packages" | awk -v package="$package_name" '
    $1 == "Package:" && $2 == package {found=1} 
    found && /^Version:/ {print $2; exit}
  ')
  eval $__resultvar="'$version'"
}

libprotobuf_version_c=""
termux_adb_version_c=""

get_version "libprotobuf-tadb-core" libprotobuf_version_c
get_version "termux-adb" termux_adb_version_c

libprotobuf_version_i=$(pkg show libprotobuf-tadb-core 2>/dev/null | grep Version | cut -d ' ' -f 2)
termux_adb_version_i=$(pkg show termux-adb 2>/dev/null | grep Version | cut -d ' ' -f 2)

# Function to compare versions without printing anything if the package is already updated
compare_versions() {
  package_name="$1"
  available_version="$2"
  installed_version="$3"
  if [ "$installed_version" != "$available_version" ]; then
    curl -s -O "$url/${package_name}_${available_version}_${arch}.deb"
    dpkg --force-overwrite -i "${package_name}_${available_version}_${arch}.deb" >/dev/null 2>&1
    rm -f "${package_name}_${available_version}_${arch}.deb"
  fi

  _progress

}

compare_versions "libprotobuf-tadb-core" "$libprotobuf_version_c" "$libprotobuf_version_i"
compare_versions "termux-adb" "$termux_adb_version_c" "$termux_adb_version_i"

ln -sf "$PREFIX/bin/termux-fastboot" "$PREFIX/bin/fastboot" && ln -sf "$PREFIX/bin/termux-adb" "$PREFIX/bin/adb"

packages=(
    "libffi"
    "abseil-cpp"
    "termux-api"
    "libusb"
    "brotli"
    "python"
    "python-pip"
    "libexpat"
    "pkg-config"
    "openssl"
    "libc++"
    "zlib"
    "zstd"
    "liblz4"
    "pv"
    "tur-repo"
    "python-pycryptodomex"
)

for package in "${packages[@]}"; do
    installed=$(apt policy "$package" 2>/dev/null | grep 'Installed' | awk '{print $2}')
    candidate=$(apt policy "$package" 2>/dev/null | grep 'Candidate' | awk '{print $2}')
    if [ "$installed" != "$candidate" ]; then
        apt download "$package" >/dev/null 2>&1
        dpkg --force-overwrite -i "${package}"*.deb >/dev/null 2>&1
        rm -f "${package}"*.deb
    fi

    _progress

done

libs=(
    "urllib3"
    "requests"
    "colorama"
)

for lib in "${libs[@]}"; do
    installed_version=$(pip show "$lib" 2>/dev/null | grep Version | awk '{print $2}')
    latest_version=$(pip index versions "$lib" 2>/dev/null | grep 'LATEST:' | awk '{print $2}')
    if [ -z "$installed_version" ]; then
        pip install "$lib" -q
    elif [ "$installed_version" != "$latest_version" ]; then
        pip install --upgrade "$lib" -q
    fi

    _progress

done

curl -s "https://raw.githubusercontent.com/offici5l/MiTool/master/MT/mitool.py" -o "$PREFIX/bin/mitool" && chmod +x "$PREFIX/bin/mitool"

_progress

curl -s "https://raw.githubusercontent.com/offici5l/MiTool/master/MT/mihelp.py" -o "$PREFIX/bin/mihelp" && chmod +x "$PREFIX/bin/mihelp"

_progress

curl -s "https://raw.githubusercontent.com/offici5l/MiTool/master/MT/miflashf.py" -o "$PREFIX/bin/miflashf" && chmod +x "$PREFIX/bin/miflashf"

_progress

curl -s "https://raw.githubusercontent.com/offici5l/MiTool/master/MT/miflashs.py" -o "$PREFIX/bin/miflashs" && chmod +x "$PREFIX/bin/miflashs"

_progress

curl -s "https://raw.githubusercontent.com/offici5l/MiTool/master/MT/mifce.sh" -o "$PREFIX/bin/mifce" && chmod +x "$PREFIX/bin/mifce"

_progress


curl -s "https://raw.githubusercontent.com/offici5l/MiTool/master/MT/miasst.py" -o "$PREFIX/bin/miasst" && chmod +x "$PREFIX/bin/miasst"

_progress

if [ ! -f "$miunlockusers" ]; then
    curl -sSL -o "$PREFIX/bin/miunlock" https://github.com/offici5l/MiUnlockTool/releases/latest/download/MiUnlockTool.py
    touch "$miunlockusers"
else
    curl -sSL -o "$PREFIX/bin/miunlock" https://raw.githubusercontent.com/offici5l/MiUnlockTool/master/MiUnlockTool.py
fi

chmod +x "$PREFIX/bin/miunlock"

_progress

curl -s "https://raw.githubusercontent.com/offici5l/MiBypassTool/master/MiBypassTool.py" -o "$PREFIX/bin/mibypass" && chmod +x "$PREFIX/bin/mibypass"

_progress

curl -s -L -o $PREFIX/bin/miasst_termux $(curl -s "https://api.github.com/repos/offici5l/MiAssistantTool/releases/latest" | grep "browser_download_url.*miasst_termux_${arch}" | cut -d '"' -f 4) && chmod +x $PREFIX/bin/miasst_termux

_progress

echo

curl -L -s https://raw.githubusercontent.com/offici5l/MiTool/main/CHANGELOG.md | tac | awk '/^#/{exit} {print "\033[0;34m" $0 "\033[0m"}' | tac

printf "\nuse command: \e[1;32mmitool\e[0m\n\n"
