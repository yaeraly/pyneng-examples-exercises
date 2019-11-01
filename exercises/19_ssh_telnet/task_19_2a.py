# -*- coding: utf-8 -*-
import yaml
from netmiko import ConnectHandler
from paramiko.ssh_exception import AuthenticationException
from netmiko.ssh_exception import NetMikoAuthenticationException
from netmiko.ssh_exception import NetMikoTimeoutException

'''
Задание 19.2a

Скопировать функцию send_config_commands из задания 19.2 и добавить параметр verbose,
который контролирует будет ли выводится на стандартный поток вывода
информация о том к какому устройству выполняется подключение.

verbose - это параметр функции send_config_commands, не параметр ConnectHandler!

По умолчанию, результат должен выводиться.

Пример работы функции:

In [13]: result = send_config_commands(r1, commands)
Подключаюсь к 192.168.100.1...

In [14]: result = send_config_commands(r1, commands, verbose=False)

In [15]:

Скрипт должен отправлять список команд commands на все устройства из файла devices.yaml с помощью функции send_config_commands.
'''

commands = [
    'logging 10.255.255.1', 'logging buffered 20010', 'no logging console'
]


def send_config_commands(device, config_commands, verbose=True):
    results = ''
    try:
        with ConnectHandler(**device) as ssh:
            ssh.enable()
            if verbose:
                print(f'Connecting to {device["ip"]}')
                results += ssh.send_config_set(config_commands)
            else:
                results += ssh.send_config_set(config_commands)

    except (AuthenticationException, NetMikoAuthenticationException):
        print('Authentication failure: unable to connect')
    except (NetMikoTimeoutException):
        print('Connection to device timed-out')
    return results


with open('devices.yaml') as f:
    dict_device = yaml.safe_load(f)
    result = send_config_commands(dict_device[0], commands, verbose=True)

print(result)

