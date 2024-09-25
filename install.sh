#!/data/data/com.termux/files/usr/bin/bash

if [ ! -d "$HOME/storage" ]; then
    echo -e "\nYou must first grant permission using the following command:\ntermux-setup-storage\n\nThen run the command again.\n"
    exit 1
fi

if [ ! -d "/data/data/com.termux.api" ]; then
    echo -e "\ncom.termux.api app is not installed\nPlease install it first\n"
    exit 1
fi

arch=$(uname -m)

if [ "$arch" = "aarch64" ]; then
    arch="aarch64"
elif [ "$arch" = "armv7l" ]; then
    arch="arm"
else
    echo -e "\nArchitecture $arch not supported\n"
    exit 1
fi

main_repo=$(grep -E '^deb ' /data/data/com.termux/files/usr/etc/apt/sources.list | awk '{print $2}' | head -n 1)

echo -e "\nChecking $main_repo ...\n"
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

echo -e "\nChecking $git_repo ...\n"

curl -s --retry 4 $git_repo > /dev/null
exit_code=$?

if [ $exit_code -eq 6 ]; then
    echo -e "\nRequest to $git_repo failed.Please check your internet connection.\n"
    exit 6
elif [ $exit_code -eq 35 ]; then
    echo -e "\nThe $git_repo is blocked in your current country.\n"
    exit 35
fi

apt update > /dev/null 2> >(grep -v "apt does not have a stable CLI interface")

url="https://raw.githubusercontent.com/nohajc/nohajc.github.io/master/dists/termux/extras/binary-${arch}"

get_version() {
  package_name="$1"
  local __resultvar=$2

  version=$(curl -s "$url/Packages" | awk -v package="$package_name" '
    $0 ~ "^Package: " package {found=1} 
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

# Function to compare versions
compare_versions() {
  package_name="$1"
  available_version="$2"
  installed_version="$3"

  if [ "$installed_version" == "$available_version" ]; then
    echo -e "\n$package_name is already the newest version.\n"
  else
    curl -s -O "$url/${package_name}_${available_version}_${arch}.deb"
    dpkg -i "${package_name}_${available_version}_${arch}.deb" >/dev/null 2>&1
    rm -f "${package_name}_${available_version}_${arch}.deb"
  fi
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
)

for package in "${packages[@]}"; do
    installed=$(apt policy "$package" 2>/dev/null | grep 'Installed' | awk '{print $2}')
    candidate=$(apt policy "$package" 2>/dev/null | grep 'Candidate' | awk '{print $2}')
    if [ "$installed" == "$candidate" ]; then
        echo -e "\n$package is already the newest version.\n"
    else
        echo -e "\nDownloading $package...\n"
        apt download "$package" >/dev/null 2>&1
        echo -e "\nInstalling $package...\n"
        dpkg -i "${package}"*.deb >/dev/null 2>&1
        rm -f "${package}"*.deb
    fi
done

check_package() {
    package_name=$1
    install_cmd=$2
    installed_version=$(pip show "$package_name" 2>/dev/null | grep Version | awk '{print $2}')
    latest_version=$(pip index versions "$package_name" 2>/dev/null | grep 'LATEST:' | awk '{print $2}')

    if [ -z "$installed_version" ]; then
        echo -e "\nInstalling $package_name ...\n"
        eval "$install_cmd -q"
    else
        if [ "$installed_version" != "$latest_version" ]; then
            echo -e "\nUpdating $package_name ...\n"
            eval "$install_cmd --upgrade -q"
        else
            echo -e "\n$package_name is already the newest version.\n"
        fi
    fi
}

check_package "urllib3" "pip install urllib3"
check_package "pycryptodomex" "pip install pycryptodomex --extra-index-url https://termux-user-repository.github.io/pypi/"
check_package "requests" "pip install requests"
check_package "colorama" "pip install colorama"

if [ -f "$PREFIX/bin/mitool" ] && [ -f "$PREFIX/bin/mihelp" ] && [ -f "$PREFIX/bin/miflashf" ] && [ -f "$PREFIX/bin/miflashs" ] && [ -f "$PREFIX/bin/miunlock" ] && [ -f "$PREFIX/bin/mibypass" ] && [ -f "$PREFIX/bin/miasst" ]; then    miurl="https://raw.githubusercontent.com/offici5l/MiTool/main/MT/mitool.py"
    miv_c=$(curl -s "$miurl" | grep version | grep -oP '(?<=version = ")[^"]+')
    miv_i=$(grep version "$PREFIX/bin/mitool" | grep -oP '(?<=version = ")[^"]+')
    if [ -z "$miv_i" ]; then
      cmd="2"
    elif [ "$miv_i" == "$miv_c" ]; then
      cmd="0"
    else
      cmd="1"
    fi
else
    cmd="3"
fi


if [ "$1" == "f" ]; then
    cmd="3"
fi

if [ "$cmd" == "0" ]; then
    echo -e "\nMiTool is already the newest\nversion installed: $miv_i.\nLatest available version: $miv_c.\n"
    exit
elif [ "$cmd" == "1" ]; then
    echo -e "\nAn update is available! Updating from version $miv_i to $miv_c...\n"
elif [ "$cmd" == "2" ]; then
    echo -e "\nNo version installed. Downloading the latest version: $miv_c...\n"
elif [ "$cmd" == "3" ]; then
    echo -e "\nMiTool is being updated now ...\n"
fi

curl -s "https://raw.githubusercontent.com/offici5l/MiTool/master/MT/mitool.py" -o "$PREFIX/bin/mitool" && chmod +x "$PREFIX/bin/mitool"

curl -s "https://raw.githubusercontent.com/offici5l/MiTool/master/MT/mihelp.py" -o "$PREFIX/bin/mihelp" && chmod +x "$PREFIX/bin/mihelp"

curl -s "https://raw.githubusercontent.com/offici5l/MiTool/master/MT/miflashf.py" -o "$PREFIX/bin/miflashf" && chmod +x "$PREFIX/bin/miflashf"

curl -s "https://raw.githubusercontent.com/offici5l/MiTool/master/MT/miflashs.py" -o "$PREFIX/bin/miflashs" && chmod +x "$PREFIX/bin/miflashs"

curl -s "https://raw.githubusercontent.com/offici5l/MiUnlockTool/master/MiUnlockTool.py" -o "$PREFIX/bin/miunlock" && chmod +x "$PREFIX/bin/miunlock"

curl -s "https://raw.githubusercontent.com/offici5l/MiBypassTool/master/MiBypassTool.py" -o "$PREFIX/bin/mibypass" && chmod +x "$PREFIX/bin/mibypass"

curl -s -L -o $PREFIX/bin/miasst $(curl -s "https://api.github.com/repos/offici5l/MiAssistantTool/releases/latest" | grep "browser_download_url.*miasst_termux_${arch}" | cut -d '"' -f 4) && chmod +x $PREFIX/bin/miasst

curl -L -s https://raw.githubusercontent.com/offici5l/MiTool/main/CHANGELOG.md | tac | awk '/^#/{exit} {print "\033[0;34m" $0 "\033[0m"}' | tac

printf "\nuse command: \e[1;32mmitool\e[0m\n\n"