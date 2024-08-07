#############################
#                           #
# https://github.com/0xNerv #
#                           #
#############################

import requests
import sys
from colorama import *
from threading import Thread, Lock
from queue import Queue
import time

banner = f'''              __ _           _           
 _ __  _   _ / _(_)_ __   __| | ___ _ __ 
| '_ \| | | | |_| | '_ \ / _` |/ _ \ '__| Creado por \033[1m{Fore.GREEN}0xNerv{Fore.RESET}\033[0m
| |_) | |_| |  _| | | | | (_| |  __/ |    Version {Fore.GREEN}\033[1m1.1\033[0m{Fore.RESET}
| .__/ \__, |_| |_|_| |_|\__,_|\___|_|    Herramienta de codigo abierto 
|_|    |___/                              https://github.com/0xNerv
'''
print(banner)

init(autoreset=True)

ssl = 'https://'

q = Queue()
lock = Lock()

def check_url(ssl, url):
    try:
        response = requests.get(url, timeout=6)
        if response.status_code == 200 or response.status_code == 401 or response.status_code == 201 or response.status_code == 301:
            with lock:
                if 'ftp' in url:
                    sys.stdout.write(f'\r\033[1m* {Fore.GREEN}{response.status_code}{Fore.RESET}\033[0m {Fore.BLUE}Encontrado{Fore.RESET}: \033[1m{url} ({Fore.RED}FTP{Fore.RESET})\033[0m\n')
                    return
                if 'mail' in url or 'correo' in url:
                    sys.stdout.write(f'\r\033[1m* {Fore.GREEN}{response.status_code}{Fore.RESET}\033[0m {Fore.BLUE}Encontrado{Fore.RESET}: \033[1m{url} ({Fore.BLUE}MAIL{Fore.RESET})\033[0m\n')
                    return
                if 'admin' in url:
                    sys.stdout.write(f'\r\033[1m* {Fore.GREEN}{response.status_code}{Fore.RESET}\033[0m {Fore.BLUE}Encontrado{Fore.RESET}: \033[1m{url} ({Fore.YELLOW}ADMIN!{Fore.RESET})\033[0m\n')
                    return
                if 'test' in url:
                    sys.stdout.write(f'\r\033[1m* {Fore.GREEN}{response.status_code}{Fore.RESET}\033[0m {Fore.BLUE}Encontrado{Fore.RESET}: \033[1m{url} ({Fore.YELLOW}TEST, VULNERABLE{Fore.RESET})\033[0m\n')
                    return
                if 'api' in url:
                    sys.stdout.write(f'\r\033[1m* {Fore.GREEN}{response.status_code}{Fore.RESET}\033[0m {Fore.BLUE}Encontrado{Fore.RESET}: \033[1m{url} ({Fore.MAGENTA}API{Fore.RESET})\033[0m\n')
                    return
                if 'blog' in url or 'cms' in url or 'wp' in url:
                    sys.stdout.write(f'\r\033[1m* {Fore.GREEN}{response.status_code}{Fore.RESET}\033[0m {Fore.BLUE}Encontrado{Fore.RESET}: \033[1m{url} ({Fore.BLUE}WordPress{Fore.RESET})\033[0m\n')
                    return
                if 'files' in url or 'storage' in url or 'assets' in url:
                    sys.stdout.write(f'\r\033[1m* {Fore.GREEN}{response.status_code}{Fore.RESET}\033[0m {Fore.BLUE}Encontrado{Fore.RESET}: \033[1m{url} ({Fore.YELLOW}FILES{Fore.RESET})\033[0m\n')
                    return
                if 'login' in url:
                    sys.stdout.write(f'\r\033[1m* {Fore.GREEN}{response.status_code}{Fore.RESET}\033[0m {Fore.BLUE}Encontrado{Fore.RESET}: \033[1m{url} ({Fore.RED}REGISTRO{Fore.RESET})\033[0m\n')
                    return
                sys.stdout.write(f'\r\033[1m* {Fore.GREEN}{response.status_code}{Fore.RESET}\033[0m {Fore.BLUE}Encontrado{Fore.RESET}: \033[1m{url}\033[0m\n')
    except requests.exceptions.ConnectionError:
        pass
    except requests.exceptions.Timeout:
        pass
    except KeyboardInterrupt:
        print('Ctrl + C')
        sys.exit()
        exit()

def worker(ssl):
    while True:
        item = q.get()
        if item is None:
            break
        url = f'{ssl}{item}'
        
        with lock:
            sys.stdout.write(f'\rBuscando: {url}                                             \r')
            pass
        check_url(ssl, url)
        time.sleep(0.05)
        q.task_done()

def main():
    global ssl

    if len(sys.argv) != 3:
        print('Uso: script.py <target> <mode>')
        print('Modo: "\033[1msubdomains\033[0m" para buscar subdominios, "\033[1mdirectories\033[0m" para buscar directorios.')
        
        return

    target = sys.argv[1]
    mode = sys.argv[2]

    if 'www.' in target:
        www = input(f"\033[1m¿Quieres reemplazar el 'www.'? [S/N] \033[0m")
        if www.lower() == 's':
           target = target.replace('www.','')
        print ("\033[F\033[K", end='')

    if 'https://' in target:
        target = target.replace('https://','')
        ssl = 'https://'
    if 'http://' in target:
        target = target.replace('http://','')
        ssl = 'http://'

    if mode == 'subdomains':
        with open('subdomains-10000.txt', 'r') as f:
            items = [line.strip() for line in f]
    elif mode == 'directories':
        with open('directories-10000.txt', 'r') as f:
            items = [line.strip() for line in f]
    else:
        print('Modo no reconocido. Use "subdomains\033[0m" o "\033[1mdirectories\033[0m".')
        return

    if ssl == 'https://':
       https = f'\033[1m{Fore.GREEN}ON\033[0m'
    else:
       https = f'\033[1m{Fore.RED}OFF\033[0m'
    print(f'Buscando {mode} de: \033[1m{target}\033[0m')
    print(f'SSL: \033[1m{https}\033[0m')
    print(f'Hilos: \033[1m30\033[0m')
    print(f'Lista: {mode}-10000.txt')
    sys.stdout.write('\rComprobando conexion ...')
    try:
        requests.get(url=f'{ssl}{target}', timeout=6)
        sys.stdout.write('\rComprobando conexion: '+Fore.GREEN+'✔ (200)    \n'+Fore.RESET)
    except requests.exceptions.ConnectionError:
        sys.stdout.write('\rComprobando conexion: '+Fore.RED+'❌      \n'+Fore.RESET)
        return
    except requests.exceptions.Timeout:
        sys.stdout.write('\rComprobando conexion: '+Fore.RED+'❌ (timeout)     \n'+Fore.RESET)
        return

    #print ('\n\033[1mBuscando ...\033[0m\n')
    print ('=======================================================')
    
    for item in items:
        if mode == 'subdomains':
            q.put(f'{item}.{target}')
        elif mode == 'directories':
            ultn = target[-1]
            if ultn == '/':
                target = target[:-1]

                
            q.put(f'{target}/{item}')

    num_threads = 30
    threads = []
    for _ in range(num_threads):
        t = Thread(target=worker, args=(ssl,))
        t.start()
        threads.append(t)

    q.join()

    for _ in range(num_threads):
        q.put(None)
    for t in threads:
        t.join()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print ('Ctrl + C')
        exit()
        sys.exit()
        exit()
