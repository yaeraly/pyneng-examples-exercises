# -*- coding: utf-8 -*-
import yaml
from netmiko import ConnectHandler
from paramiko.ssh_exception import AuthenticationException
from netmiko.ssh_exception import NetMikoAuthenticationException
from netmiko.ssh_exception import NetMikoTimeoutException

'''
Задание 19.2c

Скопировать функцию send_config_commands из задания 19.2b и переделать ее таким образом:

Если при выполнении команды возникла ошибка,
спросить пользователя надо ли выполнять остальные команды.

Варианты ответа [y]/n:
* y - выполнять остальные команды. Это значение по умолчанию, поэтому нажатие любой комбинации воспринимается как y
* n или no - не выполнять остальные команды

Функция send_config_commands по-прежнему должна возвращать кортеж из двух словарей:
* первый словарь с выводом команд, которые выполнились без ошибки
* второй словарь с выводом команд, которые выполнились с ошибками

Оба словаря в формате
* ключ - команда
* значение - вывод с выполнением команд

Проверить работу функции можно на одном устройстве.

Пример работы функции:

In [11]: result = send_config_commands(r1, commands)
Подключаюсь к 192.168.100.1...
Команда "logging 0255.255.1" выполнилась с ошибкой "Invalid input detected at '^' marker." на устройстве 192.168.100.1
Продолжать выполнять команды? [y]/n: y
Команда "logging" выполнилась с ошибкой "Incomplete command." на устройстве 192.168.100.1
Продолжать выполнять команды? [y]/n: n

In [12]: pprint(result)
({},
 {'logging': 'config term\n'
             'Enter configuration commands, one per line.  End with CNTL/Z.\n'
             'R1(config)#logging\n'
             '% Incomplete command.\n'
             '\n'
             'R1(config)#',
  'logging 0255.255.1': 'config term\n'
                        'Enter configuration commands, one per line.  End with '
                        'CNTL/Z.\n'
                        'R1(config)#logging 0255.255.1\n'
                        '                   ^\n'
                        "% Invalid input detected at '^' marker.\n"
                        '\n'
                        'R1(config)#'})

'''

# списки команд с ошибками и без:
commands_with_errors = ['logging 0255.255.1', 'logging', 'sh i']
correct_commands = ['logging buffered 20010', 'ip http server']

commands = commands_with_errors + correct_commands

def send_config_commands(device, config_commands, verbose=True):
    results_with_errors = {}
    correct_results = {}

    try:
        with ConnectHandler(**device) as ssh:
            if verbose:
                print(f'Connecting to {device["ip"]}')

            for command in config_commands:
                results = ''
                ssh.enable()
                results = ssh.send_config_set(command)
                index = results.find('end')

                if results.find('Invalid') > 0:
                    print(f"""Команда "{command}" выполнилась с ошибкой "Invalid input detected at '^' marker." на устройстве {device["ip"]}""")
                    results_with_errors.update({command: results[:index]})
                    answer = input('Продолжать выполнять команды? [y]/n: ')
                    if answer == 'n' or answer == 'no':
                        break
                elif results.find('Incomplete') > 0:
                    print(f"""Команда "{command}" выполнилась с ошибкой "Incomplete command." на устройстве {device["ip"]}""")
                    results_with_errors.update({command: results[:index]})
                    answer = input('Продолжать выполнять команды? [y]/n: ')
                    if answer == 'n' or answer == 'no':
                        break
                elif results.find('Ambiguous') > 0:
                    print(f"""Команда "{command}" выполнилась с ошибкой "Ambiguous command: "{command}"" на устройстве {device["ip"]}""")
                    results_with_errors.update({command: results[:index]})
                    answer = input('Продолжать выполнять команды? [y]/n: ')
                    if answer == 'n' or answer == 'no':
                        break
                else:
                    correct_results.update({command: results[:index]})

    except (AuthenticationException, NetMikoAuthenticationException):
        print('Authentication failure: unable to connect')
    except (NetMikoTimeoutException):
        print('Connection to device timed-out')

    return (correct_results, results_with_errors)

with open('devices.yaml') as f:
    dict_device = yaml.safe_load(f)
    send_config_commands(dict_device[0], commands)

