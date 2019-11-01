# -*- coding: utf-8 -*-
import yaml
from netmiko import ConnectHandler
from paramiko.ssh_exception import AuthenticationException
from netmiko.ssh_exception import NetMikoAuthenticationException
'''
Задание 19.1a

Скопировать функцию send_show_command из задания 19.1 и переделать ее таким образом,
чтобы обрабатывалось исключение, которое генерируется
при ошибке аутентификации на устройстве.

При возникновении ошибки, на стандартный поток вывода должно выводиться сообщение исключения.

Для проверки измените пароль на устройстве или в файле devices.yaml.
'''
command = 'sh ip int br'


def send_show_command(device, command):
    result = ''
    try:
        with ConnectHandler(**device) as ssh:
            ssh.enable()

            result = ssh.send_command(command)

        return result
    except (AuthenticationException, NetMikoAuthenticationException):
        print('Authentication failure: unable to connect')


with open('devices.yaml') as f:
    dict_device = yaml.safe_load(f)
    send_show_command(dict_device[0], command)
