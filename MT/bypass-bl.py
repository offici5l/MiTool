import os, re, base64, requests, time, json, hmac, hashlib, random, urllib, urllib.parse, secrets
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from base64 import b64encode, b64decode
from Cryptodome.Cipher import AES
from urllib.parse import urlparse

def check_mode_d():
    while True:
        status1 = os.popen("adb get-state 2>/dev/null").read().strip()
        if status1 == "sideload":
            print(f"\n{status1} mode \033[92mreboot\033[0m\n\n")
            os.popen("adb reboot")
            continue
        status2 = os.popen("fastboot devices 2>/dev/null | awk '{print $NF}'").read().strip()
        if status2 == "fastboot":
            print(f"\n{status2} mode \033[92mreboot\033[0m\n\n")
            os.popen("fastboot reboot")
            continue
        status3 = os.popen("adb get-state 2>/dev/null").read().strip()
        if status3 == "device":
            print(f"\n{status3} mode \033[92mDone\033[0m\n")
            break

print("\n\033[92mCheck if device is connected via OTG! ...\033[0m\n")

check_mode_d()

os.popen("adb logcat -c")

print("\nCleared logcat \033[92mDone\033[0m\n")

os.popen("adb shell svc wifi disable")

print("\nDisabled WiFi \033[92mDone\033[0m\n")

os.popen("adb shell svc data enable")

print("\nEnabled data service \033[92mDone\033[0m\n")

os.popen("adb shell am start --activity-clear-task -a android.settings.APPLICATION_DEVELOPMENT_SETTINGS >/dev/null 2>&1")

print("\nopen Developer options \033[92mDone\033[0m\n")

print("\n\033[92mNow bind your account in Mi Unlock status\033[0m\n")

account_bind_found = False

while True:
    process = os.popen("adb logcat *:S CloudDeviceStatus:V -d").read()
    args_found = False
    headers_found = False
    for output in process.split('\n'):
        if "CloudDeviceStatus: args:" in output:
            args = output.split('args:')[1].strip()
            args_found = True
        if "CloudDeviceStatus: headers:" in output:
            headers = output.split('headers:')[1].strip()
            headers_found = True
        if args_found and headers_found:
            account_bind_found = True
            print("\n\033[92mData successfully obtained\033[0m\n")
            os.system("adb shell svc data disable")
            print("\nDisable data service \033[92mDone\033[0m\n")
            break
    if account_bind_found:
        break

passargs = "20nr1aobv2xi8ax4"
argsiv = "0102030405060708"
cipherargs = AES.new(passargs.encode("utf-8"), AES.MODE_CBC, argsiv.encode("utf-8"))
decryptedargs = unpad(cipherargs.decrypt(base64.b64decode(args)), AES.block_size).decode("utf-8")
argsjson = json.loads(decryptedargs)
print("\ndecrypted args \033[92mdone\033[0m\n")
passheaders = b'20nr1aobv2xi8ax4'
headersiv = b'0102030405060708' 
cipherheaders = AES.new(passheaders, AES.MODE_CBC, headersiv)
decryptedheaders = cipherheaders.decrypt(base64.b64decode(headers)).rstrip(b'\0').decode('utf-8')
print("\ndecrypted headers \033[92mdone\033[0m\n")

user = argsjson["userId"]

print("\nXiaomi Account Regions:\n")
print("\033[92m1\033[0m - Global")
print("\033[92m2\033[0m - India")
print("\033[92m3\033[0m - China")
print("\033[92m4\033[0m - Russia")
print("\033[92m5\033[0m - Europe")

while True:
    user_choice = input(f"\nEnter \033[92mregion\033[0m for your account {user} : ")

    if user_choice.isdigit():
        choice_number = int(user_choice)
        if 1 <= choice_number <= 5:
            break
    print("Invalid input. Please enter a valid number between 1 and 5.")

region_mapping = {1: 'Global', 2: 'India', 3: 'China', 4: 'Russia', 5: 'Europe'}
final_region = region_mapping[choice_number]

region_urls = {
    "India": "https://in-unlock.update.intl.miui.com",
    "Global": "https://unlock.update.intl.miui.com",
    "China": "https://unlock.update.miui.com",
    "Russia": "https://ru-unlock.update.intl.miui.com",
    "Europe": "https://eu-unlock.update.intl.miui.com"
}

region = region_urls.get(final_region, '')

if not argsjson.get("cloudsp_nonce"):
    random_part_length = 42 - len("_3b1fa")
    random_part = secrets.token_hex(random_part_length // 2)
    argsjson["cloudsp_nonce"] = random_part + "_3b1fa"

if argsjson["rom_version"].startswith("V816"):
    argsjson["rom_version"] = argsjson["rom_version"].replace("V816", "V14")
    print("\nValue changed \033[92mdone\033[0m\n")

data = json.dumps(argsjson)

cookies = re.search(r"Cookie=\[(.*)\]", decryptedheaders).group(1).strip()
print("\nCookies obtained \033[92mdone\033[0m\n")

sign_key = "10f29ff413c89c8de02349cb3eb9a5f510f29ff413c89c8de02349cb3eb9a5f5"
message = f"POST\n/v1/unlock/applyBind\ndata={data}&sid=miui_sec_android"
hmac_digest = hmac.new(sign_key.encode("utf-8"), message.encode("utf-8"), hashlib.sha1).digest()
print("\nData encrypted \033[92mdone\033[0m\n")
signature = hmac_digest.hex()
print("\nData signature \033[92mdone\033[0m\n")

url = f"{region}/v1/unlock/applyBind"

headers = {
    "Cookie": cookies,
    "Content-Type": "application/x-www-form-urlencoded"
}

payload = {
    "data": data,
    "sid": "miui_sec_android",
    "sign": signature
}

print("\033[92mSending request...\033[0m")

response = requests.post(url, data=payload, headers=headers)

data = json.loads(response.text)

code = data['code']

if code == 0:
    print(data)
else:
    print(data)
    exit()

print("\nbypass \033[92mdone\033[0m\n")
print("\n\n\033[92mnow simply run command 'mitool 1' to initiate bootloader unlocking process.\033[0m\n\n    (\033[91mPlease note: avoid binding account again\033[0m)\n ")