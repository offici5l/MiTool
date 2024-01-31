import re, requests, json, hmac, random, binascii, urllib, hashlib, os, urllib.parse, time, codecs, io, sys, shutil
from urllib3.util.url import Url
from base64 import b64encode, b64decode
from Cryptodome.Cipher import AES
from termcolor import colored
from urllib.parse import urlparse, parse_qs

def print_result_info(key=None, value=None):
    if key is not None:
        padding = ' ' * ((shutil.get_terminal_size().columns - len(f'{key}: {value}') - 0) // 2)
        border_line = f"┏{'━' * (len(f'{key}: {value}') + 4)}┓"
        content_line = f"┃  {key}: {value}  ┃"
        bottom_line = f"┗{'━' * (len(f'{key}: {value}') + 4)}┛"
    else:
        padding = ' ' * ((shutil.get_terminal_size().columns - len(f'{value}') - 0) // 2)
        border_line = f"┏{'━' * (len(f'{value}') + 4)}┓"
        content_line = f"┃  {value}  ┃"
        bottom_line = f"┗{'━' * (len(f'{value}') + 4)}┛"
    
    print(f"\n{padding}{border_line}\n{padding}{content_line}\n{padding}{bottom_line}")

def check_mode():
    while True:
        status1 = os.popen("adb get-state 2>/dev/null").read().strip()
        if status1 == "sideload":
            print(f"\n{status1} mode .. reboot to fastboot mode ... wait ..\n\n")
            os.system("adb reboot bootloader")
            continue
        status2 = os.popen("adb get-state 2>/dev/null").read().strip()
        if status2 == "device":
            print(f"\n{status2} mode .. reboot to fastboot mode ... wait ..\n\n")
            os.system("adb reboot bootloader")
            continue
        status3 = os.popen("fastboot devices 2>/dev/null | awk '{print $NF}'").read().strip()
        if status3 == "fastboot":
            print(f"\n {status1} ok \n")
            break

filedata = "/sdcard/Download/data.json"
filetp = "/sdcard/Download/device_token_product.json"
session = requests.Session()
headers = {"User-Agent": "XiaomiPCSuite"}

def login_confirmation():
    input("\nPress Enter to open login confirmation page\nWhen you see:\033[92m {{\"R\":\"\",\"S\":\"OK\"}}\033[0m copy link \nand return here\n")
    os.system(f"termux-open-url 'https://account.xiaomi.com/pass/serviceLogin?sid=unlockApi&checkSafeAddress=true'")
    url = input("Please enter the link: ")
    expected_part = "unlock.update.miui.com/sts?d="

    while True:
        if expected_part in url:
            break
        else:
            print("\n\033[91mInvalid link!\033[0m\n")
            print("\n(\033[38;5;208mIf you're having trouble obtaining a valid link !\nuse command\033[0m \033[92mr\033[0 \033[38;5;208m to reopen login confirmation page.\033[0m)\n")
            url = input("\nplease enter a valid link: ")
            if url.lower() == 'r':
                os.system(f"termux-open-url 'https://account.xiaomi.com/pass/serviceLogin?sid=unlockApi&checkSafeAddress=true'")

    query_parameters = parse_qs(urlparse(url).query)
    idd = {key if key != "d" else "deviceId": value[0] for key, value in query_parameters.items()}
    cookies_json = json.dumps(idd, indent=2)

    return cookies_json

def login_user():
    while True:
        user = input("Please enter your username: ")
        pwd = input("Please enter your password: ")
        response = requests.post("https://account.xiaomi.com/pass/serviceLoginAuth2?sid=unlockApi&_json=true", data={"user": user, "hash": hashlib.md5(pwd.encode()).hexdigest().upper()}).text
        login_response = json.loads(response.replace("&&&START&&&", ""))
        if "code" in login_response and login_response["code"] == 70016:
            print("Invalid credentials. Please enter the correct username and password.")
            continue
        else:
            login_c = login_confirmation()
            userId = login_response.get('userId')
            with open(filedata, "a") as json_file:
                json_file.write(f'{{\n  "user": "{userId}",\n  "hash": "{hashlib.md5(pwd.encode()).hexdigest().upper()}", {login_c.strip("{}")}}}')
            print(f"\n\nsave data in {filedata}\n\n")
            break



print_result_info(value="github.com/offici5l/MiTool")

choice = input("\n\n- \033[92m1\033[0m Unlock\n- \033[92m2\033[0m Lock\n\nEnter your \033[92mchoice\033[0m: ")

if choice == "1":
    pass
elif choice == "2":
    input("\nEnsure your device is in fastboot mode, connected via OTG. Press Enter when ready to unlock the device\n")
    print("\ncheck device it is connected via OTG! ...\n")
    check_mode()
    os.system(f"fastboot oem lock")
    exit()
else:
    print("\nInvalid choice.\n")
    exit()

def remove_file(file_path):
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            print(f"\n\n{file_path} has been removed\n\n")
        except Exception as e:
            print(f"\n\nError removing {file_path}: {e}\n\n")

while True:
    if os.path.exists(filedata):
        with open(filedata, 'r') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = None

            if data:
                print(f"\n\nuserId: \033[92m{data['user']}\033[0m Data exists !\n")
                choice = input("\n- \033[92m1\033[0m use previous data\n- \033[92m2\033[0m delete previous data\n\nEnter your \033[92mchoice\033[0m: ")
                if choice == "1":
                    break
                elif choice == "2":
                    remove_file(filedata)
                    remove_file(filetp)
                    login_user()
                    break
                else:
                    print("\nInvalid choice!\n")
                    continue
            else:
                remove_file(filedata)
                remove_file(filetp)
                login_user()
                break
    else:
        remove_file(filedata)
        remove_file(filetp)
        login_user()
        break



with open(filedata, 'r') as file:
    datafile = json.load(file)

url = "https://account.xiaomi.com/pass/serviceLoginAuth2?sid=unlockApi&_json=true"

response = session.post(url, data=datafile, headers=headers, cookies=datafile).text.replace("&&&START&&&", "")

# securityStatus16 temporary line (delete later)
if json.loads(response)["securityStatus"] == 16:
    error_message = f'\n\033[91msecurityStatus {json.loads(response)["securityStatus"]}\033[0m\n\n\033[92mPlease go to: settings > Mi Account > Devices > select Current device > Find device "enable Find device"\033[0m\n'
    print(error_message)
    exit()

region = re.search(r'p_idc=(.*?)&nonce', response).group(1)

final_region = region if region.lower() in ['india', 'europe', 'russia', 'china'] else 'Global'

region_urls = {
    "India": "https://in-unlock.update.intl.miui.com",
    "Global": "https://unlock.update.intl.miui.com",
    "China": "https://unlock.update.miui.com",
    "Russia": "https://ru-unlock.update.intl.miui.com",
    "Europe": "https://eu-unlock.update.intl.miui.com"
}

url = region_urls.get(final_region, '')

result2 = response.replace(response.split('"location":"')[1].split('/sts?d=')[0], url)

data = json.loads(result2)

ssecurity, psecurity, userid, c_userid, code, nonce, location = (data["ssecurity"], data["psecurity"], data["userId"], data["cUserId"], data["code"], data["nonce"], data["location"])

response_cookies = session.get( location + "&clientSign=" + urllib.parse.quote_plus(b64encode(hashlib.sha1(f"nonce={nonce}".encode("utf-8") + b"&" + ssecurity.encode("utf-8")).digest())), headers=headers ).cookies

cookies = response_cookies

deviceId = datafile.get("deviceId", {})

if not cookies:
    wbe = deviceId
    error_message = f'\n\033[91mdescEN: Error information not obtained from server.\nInvalid wb_value: {wbe} \n\033[0m\033[92m'
    print(error_message)
    exit()
else:
    pass

try:
    with open(filetp, "r") as file:
        try:
            content = json.load(file)
        except json.JSONDecodeError:
            content = {}
except FileNotFoundError:
    content = {}

if "deviceToken" not in content or "product" not in content:
    print("\nCheck device; it is connected via OTG! ...\n")
    check_mode()
    output = os.popen("fastboot getvar all 2>&1").read()
    token, product = [os.popen(f'echo "{output}" | grep -Po "(?<={var}:).*"').read().strip() for var in ["token", "product"]]
    data = {"deviceToken": token, "product": product}
    with open(filetp, "w") as file:
        json.dump(data, file, indent=2)
        print(f"\n\nsave deviceToken and product in {filetp}\n\n")

with open(filetp, 'r') as file:
    data = json.load(file)

for key, value in data.items():
    print(f"\n{key}: \033[92m{value}\033[0m\n")

token_value = data.get("deviceToken", {})
product_value = data.get("product", {})

params = {k.encode("utf-8") if isinstance(k, str) else k: v.encode("utf-8") if isinstance(v, str) else b64encode(json.dumps(v).encode("utf-8")) if not isinstance(v, bytes) else v for k, v in {"appId": "1", "data": {"clientId": "2", "clientVersion": "5.5.224.55", "language": "en", "operate": "unlock", "pcId": hashlib.md5(deviceId.encode("utf-8")).hexdigest(), "product": product_value, "deviceInfo": {"product": product_value}, "deviceToken": token_value}
}.items()}


psiggn = bytes.fromhex("327442656f45794a54756e6d57554771376251483241626e306b324e686875724f61714266797843754c56676e3441566a3773776361776535337544556e6f")

def get_params(sep):
    return b"POST" + sep + "/api/v3/ahaUnlock".encode("utf-8") + sep + b"&".join([k + b"=" + v for k, v in params.items()])

def add_sign():
    params[b"sign"] = binascii.hexlify(hmac.digest(psiggn, get_params(b"\n"), "sha1"))

def _encrypt(value):
    return b64encode(AES.new(b64decode(ssecurity), AES.MODE_CBC, b"0102030405060708").encrypt((lambda s: s + (16 - len(s) % 16) * bytes([16 - len(s) % 16]))(value)))

def encrypt():
    params.update({k: _encrypt(v) for k, v in params.items()})

def add_signature():
    params[b"signature"] = b64encode(hashlib.sha1(get_params(b"&") + b"&" + ssecurity.encode("utf-8")).digest())

def add_nonce():
    r = unlock_device_request("/api/v2/nonce", {"r": ''.join(random.choices(list("abcdefghijklmnopqrstuvwxyz"), k=16)), "sid": "miui_unlocktool_client"})
    params[b"nonce"], params[b"sid"] = r["nonce"].encode("utf-8"), b"miui_unlocktool_client"

def _decrypt(value):
    ret = b64decode((lambda s: s[:-s[-1]])(AES.new(b64decode(ssecurity), AES.MODE_CBC, b"0102030405060708").decrypt(b64decode(value))))
    return ret

def run():
    add_sign()
    encrypt()
    add_signature()
    return json.loads(send())

def send():
    response = session.request("POST", Url(host=url, path="/api/v3/ahaUnlock").url, data=params, headers=headers, cookies=cookies)
    response.raise_for_status()
    return _decrypt(response.text)

def unlock_device_request(endpoint, params):
    request_params = {k.encode("utf-8") if isinstance(k, str) else k: v.encode("utf-8") if isinstance(v, str) else b64encode(json.dumps(v).encode("utf-8")) if not isinstance(v, bytes) else v for k, v in params.items()}

    def get_request_params(sep):
        return b"POST" + sep + endpoint.encode("utf-8") + sep + b"&".join([k + b"=" + v for k, v in request_params.items()])

    def add_sign():
        request_params[b"sign"] = binascii.hexlify(hmac.digest(psiggn, get_request_params(b"\n"), "sha1"))

    def _encrypt(value):
        return b64encode(AES.new(b64decode(ssecurity), AES.MODE_CBC, b"0102030405060708").encrypt((lambda s: s + (16 - len(s) % 16) * bytes([16 - len(s) % 16]))(value)))

    def encrypt():
        request_params.update({k: _encrypt(v) for k, v in request_params.items()})

    def add_signature():
        request_params[b"signature"] = b64encode(hashlib.sha1(get_request_params(b"&") + b"&" + ssecurity.encode("utf-8")).digest())

    def add_nonce():
        r = unlock_device_request("/api/v2/nonce", {"r": ''.join(random.choices(list("abcdefghijklmnopqrstuvwxyz"), k=16)), "sid": "miui_unlocktool_client"})
        request_params[b"nonce"], request_params[b"sid"] = r["nonce"].encode("utf-8"), b"miui_unlocktool_client"

    def _decrypt(value):
        ret = b64decode((lambda s: s[:-s[-1]])(AES.new(b64decode(ssecurity), AES.MODE_CBC, b"0102030405060708").decrypt(b64decode(value))))
        return ret

    def run():
        add_sign()
        encrypt()
        add_signature()
        return json.loads(send())

    def send():
        response = session.request("POST", Url(host=url, path=endpoint).url, data=request_params, headers=headers, cookies=cookies)
        response.raise_for_status()
        return _decrypt(response.text)

    return run()

add_nonce()
result = run()
session.close()

code = result.get("code", "")
descEN = result.get("descEN", "")

if "code" in result and result["code"] == 10000:
    print(f"\ncode: {code} descEN: {descEN}\nInvalid device token or product.\n")
    remove_file(filetp)
    exec("\n".join(line for i, line in enumerate(codecs.open('/data/data/com.termux/files/usr/bin/un-lock.py', 'r', 'utf-8').read().split('\n'), 1) if i not in range(82, 141)))
    exit()

if "code" in result and result["code"] == 20036:
    print(f"\n\n\033[92m{descEN}\033[0m\n\n")
    exit()

if "encryptData" in result:
    unlock_token = result["encryptData"]
    binary_data = bytes.fromhex(unlock_token)
    bytes_io_data = io.BytesIO(binary_data)
    with open("token.bin", "wb") as token_file:
        token_file.write(bytes_io_data.getvalue())
    print("\ncheck device it is connected via OTG! ...\n")
    check_mode()
    os.system("fastboot stage token.bin")
    os.system("fastboot oem unlock")
else:
    if "uid" in result:
        print_result_info("userId", result["uid"])
    if "code" in result:
        print(f"\n{colored('code: ' + str(result['code']), 'green')}\n")
    if "description" in result:
        print(f"\n{colored(result['description'], 'green')}\n")
    if "descEN" in result:
        print(f"\n{colored(result['descEN'], 'green')}\n")
    print("\n\n")

