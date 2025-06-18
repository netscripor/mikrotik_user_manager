#!/usr/bin/env python3
import os
import sys
import argparse
import getpass
import time
from netmiko import ConnectHandler
from colorama import Fore, Style, init

init(autoreset=True)

def read_ip_list(file_path=None):
    ip_list = []
    if file_path:
        if not os.path.exists(file_path):
            print(Fore.RED + f"[!] Файл {file_path} не найден.")
            sys.exit(1)
        with open(file_path, 'r') as f:
            ip_list = [line.strip() for line in f if line.strip()]
    else:
        print(Fore.YELLOW + "Введите IP-адреса вручную. Для завершения введите 'end':")
        while True:
            line = input()
            if line.lower() == 'end':
                break
            ip_list.append(line.strip())
    return ip_list

def wait_for_user(ssh, username, retries=3, delay=1):
    """Проверка существования пользователя с повторными попытками"""
    for _ in range(retries):
        result = ssh.send_command(f"/user print where name={username}")
        if username in result:
            return True
        time.sleep(delay)
    return False

def connect_and_execute(ip, auth, mode, target_user, password=None, group="full", allowed_addresses=None, logf=None):
    router = {
        'device_type': 'mikrotik_routeros',
        'ip': ip,
        'username': auth['username'],
        'password': auth['password']
    }

    try:
        print(Fore.CYAN + f"[+] Подключение к {ip}")
        ssh = ConnectHandler(**router)
        result = ssh.send_command(f"/user print where name={target_user}")

        if mode == 'create':
            if target_user in result:
                msg = f"[-] Пользователь {target_user} уже существует на {ip}"
                print(Fore.YELLOW + msg)
                logf.write(msg + '\n')
            else:
                cmd = f"/user add name={target_user} password={password} group={group}"
                if allowed_addresses:
                    addr_list = ','.join(a.strip() for a in allowed_addresses.split(',') if a.strip())
                    cmd += f" address={addr_list}"
                ssh.send_command(cmd, expect_string=None, strip_prompt=False, strip_command=False)

                if wait_for_user(ssh, target_user):
                    msg = f"[+] Пользователь {target_user} создан на {ip}"
                    print(Fore.GREEN + msg)
                    logf.write(msg + '\n')
                else:
                    msg = f"[!] Ошибка: не удалось подтвердить создание {target_user} на {ip}"
                    print(Fore.RED + msg)
                    logf.write(msg + '\n')

        elif mode == 'delete':
            if target_user not in result:
                msg = f"[~] Пользователь {target_user} не найден на {ip}"
                print(Fore.YELLOW + msg)
                logf.write(msg + '\n')
            else:
                ssh.send_command_expect(f"/user remove {target_user}")
                if wait_for_user(ssh, target_user):
                    msg = f"[!] Не удалось удалить пользователя {target_user} на {ip}"
                    print(Fore.RED + msg)
                    logf.write(msg + '\n')
                else:
                    msg = f"[+] Пользователь {target_user} удалён на {ip}"
                    print(Fore.GREEN + msg)
                    logf.write(msg + '\n')

    except Exception as e:
        msg = f"[X] Ошибка подключения к {ip}: {e}"
        print(Fore.RED + msg)
        if logf:
            logf.write(msg + '\n')

def main():
    parser = argparse.ArgumentParser(description="Mikrotik User Manager — создание/удаление пользователей")
    parser.add_argument('--mode', required=True, choices=['create', 'delete'], help='Режим: create или delete')
    parser.add_argument('--file', help='Файл с IP-адресами устройств')
    parser.add_argument('--group', default='full', help='Группа для создаваемого пользователя (по умолчанию: full)')
    parser.add_argument('--address', help='Ограничение по IP (один или несколько через запятую)')

    args = parser.parse_args()
    ip_list = read_ip_list(args.file)

    username = input("Логин для подключения к Mikrotik: ")
    password = getpass.getpass("Пароль: ")
    target_user = input("Имя пользователя, с которым работаем (создание/удаление): ")

    new_password = None
    if args.mode == 'create':
        new_password = getpass.getpass("Пароль для нового пользователя: ")

    os.makedirs("logs", exist_ok=True)
    log_path = os.path.join("logs", f"{args.mode}_{target_user}.log")

    with open(log_path, 'w') as logf:
        for ip in ip_list:
            connect_and_execute(
                ip,
                auth={'username': username, 'password': password},
                mode=args.mode,
                target_user=target_user,
                password=new_password,
                group=args.group,
                allowed_addresses=args.address,
                logf=logf
            )

    print(Style.BRIGHT + f"\n[✓] Готово. Лог сохранён в {log_path}")

if __name__ == '__main__':
    main()
