# -*- coding: utf-8 -*-
import yaml
from netmiko import ConnectHandler
from paramiko.ssh_exception import AuthenticationException
from netmiko.ssh_exception import NetMikoAuthenticationException
from netmiko.ssh_exception import NetMikoTimeoutException
'''
Задание 19.2b

Скопировать функцию send_config_commands из задания 19.2a и добавить проверку на ошибки.

При выполнении каждой команды, скрипт должен проверять результат на такие ошибки:
 * Invalid input detected, Incomplete command, Ambiguous command

Если при выполнении какой-то из команд возникла ошибка,
функция должна выводить сообщение на стандартный поток вывода с информацией
о том, какая ошибка возникла, при выполнении какой команды и на каком устройстве, например:
Команда "logging" выполнилась с ошибкой "Incomplete command." на устройстве 192.168.100.1

Ошибки должны выводиться всегда, независимо от значения параметра verbose.
При этом, verbose по-прежнему должен контролировать будет ли выводиться сообщение:
Подключаюсь к 192.168.100.1...


Функция send_config_commands теперь должна возвращать кортеж из двух словарей:
* первый словарь с выводом команд, которые выполнились без ошибки
* второй словарь с выводом команд, которые выполнились с ошибками

Оба словаря в формате:
* ключ - команда
* значение - вывод с выполнением команд

Проверить работу функции можно на одном устройстве.


Пример работы функции send_config_commands:

In [16]: commands
Out[16]:
['logging 0255.255.1',
 'logging',
 'sh i',
 'logging buffered 20010',
 'ip http server']

In [17]: result = send_config_commands(r1, commands)
Подключаюсь к 192.168.100.1...
Команда "logging 0255.255.1" выполнилась с ошибкой "Invalid input detected at '^' marker." на устройстве 192.168.100.1
Команда "logging" выполнилась с ошибкой "Incomplete command." на устройстве 192.168.100.1
Команда "sh i" выполнилась с ошибкой "Ambiguous command:  "sh i"" на устройстве 192.168.100.1

In [18]: pprint(result, width=120)
({'ip http server': 'config term\n'
                    'Enter configuration commands, one per line.  End with CNTL/Z.\n'
                    'R1(config)#ip http server\n'
                    'R1(config)#',
  'logging buffered 20010': 'config term\n'
                            'Enter configuration commands, one per line.  End with CNTL/Z.\n'
                            'R1(config)#logging buffered 20010\n'
                            'R1(config)#'},
 {'sh i': 'config term\n'
       'Enter configuration commands, one per line.  End with CNTL/Z.\n'
       'R1(config)#sh i\n'
       '% Ambiguous command:  "sh i"\n'
       'R1(config)#',
  'logging': 'config term\n'
             'Enter configuration commands, one per line.  End with CNTL/Z.\n'
             'R1(config)#logging\n'
             '% Incomplete command.\n'
             '\n'
             'R1(config)#',
  'logging 0255.255.1': 'config term\n'
                        'Enter configuration commands, one per line.  End with CNTL/Z.\n'
                        'R1(config)#logging 0255.255.1\n'
                        '                   ^\n'
                        "% Invalid input detected at '^' marker.\n"
                        '\n'
                        'R1(config)#'})

In [19]: good, bad = result

In [20]: good.keys()
Out[20]: dict_keys(['logging buffered 20010', 'ip http server'])

In [21]: bad.keys()
Out[21]: dict_keys(['logging 0255.255.1', 'logging', 'sh i'])


Примеры команд с ошибками:
R1(config)#logging 0255.255.1
                   ^
% Invalid input detected at '^' marker.

R1(config)#logging
% Incomplete command.

R1(config)#sh i
% Ambiguous command:  "sh i"
'''

# списки команд с ошибками и без:
commands_with_errors = ['logging 0255.255.1', 'logging', 'do show ru']
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
                elif results.find('Incomplete') > 0:
                    print(f"""Команда "{command}" выполнилась с ошибкой "Incomplete command." на устройстве {device["ip"]}""")
                    results_with_errors.update({command: results[:index]})
                elif results.find('Ambiguous') > 0:
                    print(f"""Команда "{command}" выполнилась с ошибкой "Ambiguous command: "{command}"" на устройстве {device["ip"]}""")
                    results_with_errors.update({command: results[:index]})
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
