import re, requests, json, hmac, random, binascii, urllib, hashlib, os, urllib.parse, time
from urllib3.util.url import Url
from base64 import b64encode, b64decode
from Cryptodome.Cipher import AES
from termcolor import colored

text_to_print = """
•Bind your Xiaomi account to your phone. 
\n•Go to Settings » About phone » MIUI version.
Tap repeatedly on the MIUI version until you see the pop-up You are now a developer!
\n•Go back to Settings, click on Additional settings, then Developer options.
\n•Enable OEM unlocking and USB debugging.
\nTap Mi Unlock status » Agree » Add account and device. (Make sure your device can connect to the internet using mobile data.)
Once the account is successfully bound, you should get a message Added successfully.
"""
print(text_to_print)

input(colored(f"\n If you complete the steps successfully. Press Enter  ", 'green'))

filename = "/sdcard/Download/account_info.txt"

while os.path.isfile(filename):
    use_previous = input(f"\ndo you want to use previous information in \033[92m{filename}\033[0m (yes/no) ? : ").lower()
    if use_previous == "yes":
        break
    elif use_previous == "no":
        os.remove(filename)
        break
    else:
        print("Invalid choice. Please enter 'yes' or 'no'.")

with open(filename, "a+") as file:
    file.seek(0)
    content = file.read()
    if "Username:" not in content:
        usernamee = input("Enter username or email or number (Xiaomi Account): ")
        file.write(f"\nUsername: {usernamee}\n")
    if "Password:" not in content:
        passwordd = input("Enter password: ")
        file.write(f"\nPassword: {passwordd}\n")
    if "region:" not in content:
        region = input("Choose a region (Account) (india, global, china, russia, europe): ")
        file.write(f"\nregion: {region}\n")
    if "token:" not in content or "product:" not in content:
        entry_choice = input("Do you want to input device token and product automatically or manually? (a/m): ").lower()
        if entry_choice == 'm':
            if "token:" not in content:
                 token = input("Enter output from `fastboot getvar token`: ")
                 file.write(f"\ntoken: {token}\n")
            if "product:" not in content:
                 product = input("Enter output from `fastboot getvar product`: ")
                 file.write(f"\nproduct: {product}\n")
        elif entry_choice == 'a':
            confirmation = input("Make sure your device is connected in fastboot mode. Connect your device using OTG, then press Enter when ready.")
            output = os.popen("fastboot getvar all 2>&1").read()
            token, product = [os.popen(f'echo "{output}" | grep -Po "(?<={var}:).*"').read().strip() for var in ["token", "product"]]
            if "token:" not in content:
                file.write(f"\ntoken: {token}\n")
            if "product" not in content:
                file.write(f"\nproduct: {product}\n")
        else:
            print("Invalid choice")

if "wb_value:" in open(filename).read():
    pass
else:
    input(f"\nWhen you press Enter The page will open in your default browser to confirm your login, after seeing {{\"R\":\"\",\"S\":\"OK\"}} in browser, copy URL from address bar Then come back here and paste link here ")
    os.system(f"termux-open-url 'https://account.xiaomi.com/pass/serviceLogin?sid=unlockApi&checkSafeAddress=true'")
    wbinput = input("\nlink: ")
    wb_value_match = re.search(r'sts\?d=[^&]*', wbinput)
    if wb_value_match:
        wb_value = wb_value_match.group(0).split('=')[1]
        with open(filename, "a") as file:
            file.write(f"\nwb_value: {wb_value}\n")
    else:
        print("Invalid URL")
        exit()

with open(filename, "r") as file:
    lines = file.readlines()
    tokenname = next((line.split(' ', 1)[1].strip() for line in lines if "token:" in line), None)
    productname = next((line.split(' ', 1)[1].strip() for line in lines if "product:" in line), None)
    username = next((line.split(' ', 1)[1].strip() for line in lines if "Username:" in line), None)
    password = next((line.split(' ', 1)[1].strip() for line in lines if "Password:" in line), None)
    wbvalueline = next((line.split(' ', 1)[1].strip() for line in lines if "wb_value:" in line), None)
    region = next((line.split(' ', 1)[1].strip() for line in lines if "region:" in line), None)

response = requests.post("https://account.xiaomi.com/pass/serviceLoginAuth2?sid=unlockApi&_json=true", data={"user": username, "hash": hashlib.md5(password.encode()).hexdigest().upper()}, headers={"User-Agent": "XiaomiPCSuite"}, cookies={"deviceId": wbvalueline}).text.replace("&&&START&&&", "")

m_value, tsl_value = urllib.parse.parse_qs(urllib.parse.urlparse(json.loads(response)["location"]).query).get('m', [''])[0], urllib.parse.parse_qs(urllib.parse.urlparse(json.loads(response)["location"]).query).get('tsl', [''])[0]

with open('/sdcard/Download/log.txt', 'a') as log_file:
    log_file.write(f"\n\n>>> m = {m_value}, tsl = {tsl_value}, ")

if json.loads(response)["securityStatus"] == 16:
    error_message = f'\n\033[91msecurityStatus {json.loads(response)["securityStatus"]}\033[0m\n\n\033[92mPlease go to: settings > Mi Account > Devices > select Current device > Find device "enable Find device"\033[0m\n'
    print(error_message)
    exit()

if json.loads(response)["code"] == 70016:
    error_message = f'\n\033[91mcodeStatus {json.loads(response)["code"]} Error descEN: The account ID or password you entered is incorrect. \n\033[0m'
    print(error_message)
    exit()

region_urls = {
    "india": "in-unlock.update.intl.miui.com",
    "global": "unlock.update.intl.miui.com",
    "china": "unlock.update.miui.com",
    "russia": "ru-unlock.update.intl.miui.com",
    "europe": "eu-unlock.update.intl.miui.com"
}

result2 = re.sub(r'[^/]+\.com', lambda match: region_urls.get(region, ''), response)

url = re.search(r'([^/]+)/sts', result2).group(1)

data = json.loads(result2)

ssecurity, psecurity, userid, c_userid, code, nonce, location = (data["ssecurity"], data["psecurity"], data["userId"], data["cUserId"], data["code"], data["nonce"], data["location"])

response_cookies = requests.Session().get(location + "&clientSign=" + urllib.parse.quote_plus(b64encode(hashlib.sha1(f"nonce={nonce}".encode("utf-8") + b"&" + ssecurity.encode("utf-8")).digest()))).cookies
cookies = response_cookies

if not cookies:
    error_message = f'\n\033[91mdescEN: Error information not obtained from server.\nInvalid wb_value: {wbvalueline}\n\033[0m\033[92m'
    print(error_message)
    exit()
else:
    pass

params = {k.encode("utf-8") if isinstance(k, str) else k: v.encode("utf-8") if isinstance(v, str) else b64encode(json.dumps(v).encode("utf-8")) if not isinstance(v, bytes) else v for k, v in {"appId": "1", "data": {"clientId": "2", "clientVersion": "5.5.224.55", "language": "en", "operate": "unlock", "pcId": hashlib.md5(wbvalueline.encode("utf-8")).hexdigest(), "product": productname, "deviceInfo": {"product": productname}, "deviceToken": tokenname}
}.items()}

cipher = AES.new(b64decode(ssecurity), AES.MODE_CBC, b"0102030405060708")

def get_params(sep):
    return b"POST" + sep + "/api/v3/ahaUnlock".encode("utf-8") + sep + b"&".join([k + b"=" + v for k, v in params.items()])

def add_sign():
    params[b"sign"] = binascii.hexlify(hmac.digest(bytes.fromhex("327442656f45794a54756e6d57554771376251483241626e306b324e686875724f61714266797843754c56676e3441566a3773776361776535337544556e6f"), get_params(b"\n"), "sha1"))

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
    response = requests.request("POST", Url(scheme="https", host=url, path="/api/v3/ahaUnlock").url, data=params, headers={"User-Agent": "XiaomiPCSuite"}, cookies=cookies)
    response.raise_for_status()
    return _decrypt(response.text)

def unlock_device_request(endpoint, params):
    request_params = {k.encode("utf-8") if isinstance(k, str) else k: v.encode("utf-8") if isinstance(v, str) else b64encode(json.dumps(v).encode("utf-8")) if not isinstance(v, bytes) else v for k, v in params.items()}
    cipher = AES.new(b64decode(ssecurity), AES.MODE_CBC, b"0102030405060708")

    def get_request_params(sep):
        return b"POST" + sep + endpoint.encode("utf-8") + sep + b"&".join([k + b"=" + v for k, v in request_params.items()])

    def add_sign():
        request_params[b"sign"] = binascii.hexlify(hmac.digest(bytes.fromhex("327442656f45794a54756e6d57554771376251483241626e306b324e686875724f61714266797843754c56676e3441566a3773776361776535337544556e6f"), get_request_params(b"\n"), "sha1"))

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
        response = requests.request("POST", Url(scheme="https", host=url, path=endpoint).url, data=request_params, headers={"User-Agent": "XiaomiPCSuite"}, cookies=cookies)
        response.raise_for_status()
        return _decrypt(response.text)

    return run()

add_nonce()
result = run()

log_m = "\n(Please share /sdcard/Download/log.txt on github.com/offici5l/MiTool/issues/5 or t.me/Offici5l_Group if you want assistance in improving the tool)\n"

if "code" in result:
    with open('/sdcard/Download/log.txt', 'a+') as log_file:
        log_file.write(f"code = {result['code']}, ")

if "description" in result:
    with open('/sdcard/Download/log.txt', 'a+') as log_file:
        log_file.write(f"description: {result['description']}, ")

if "descEN" in result:
    with open('/sdcard/Download/log.txt', 'a+') as log_file:
        log_file.write(f"descEN: {result['descEN']}, ")

if "encryptData" in result:
    unlock_token = result["encryptData"]
    input("Make sure your device is connected in fastboot mode. Connect your device using OTG, then press Enter when ready.")

    with open("token.bin", "wb") as token_file:
        token_file.write(bytes.fromhex(unlock_token))

    answer = input("Last step: Confirm that you want to unlock the device? (y/n): ")

    if answer.lower() == "y":
        os.system("fastboot stage token.bin")
        os.system("fastboot oem unlock")
        print(log_m)
    else:
        print("Cancel unlock...")
        print(log_m)
else:
    result_str = json.dumps(result, indent=2, ensure_ascii=False, separators=('\n', ': '))[1:-1].replace('"', '')
    print(colored(result_str, 'green'))
    print(log_m)
