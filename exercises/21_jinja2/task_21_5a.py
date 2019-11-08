# -*- coding: utf-8 -*-
import os
import yaml
from concurrent.futures import ThreadPoolExecutor
from netmiko import ConnectHandler, NetMikoAuthenticationException
from pprint import pprint
from jinja2 import Environment, FileSystemLoader
'''
Задание 21.5a

Создать функцию configure_vpn, которая использует шаблоны из задания 21.5 для настройки VPN на маршрутизаторах на основе данных в словаре data.

Параметры функции:
* src_device_params - словарь с параметрами подключения к устройству
* dst_device_params - словарь с параметрами подключения к устройству
* src_template - имя файла с шаблоном, который создает конфигурацию для одной строны туннеля
* dst_template - имя файла с шаблоном, который создает конфигурацию для второй строны туннеля
* vpn_data_dict - словарь со значениями, которые надо подставить в шаблоны

Функция должна настроить VPN на основе шаблонов и данных на каждом устройстве.
Функция возвращает вывод с набором команд с двух марушртизаторов (вывод, которые возвращает send_config_set).

При этом, в словаре data не указан номер интерфейса Tunnel, который надо использовать.
Номер надо определить самостоятельно на основе информации с оборудования.
Если на маршрутизаторе нет интерфейсов Tunnel, взять номер 0, если есть взять ближайший свободный номер,
но одинаковый для двух маршрутизаторов.

Например, если на маршрутизаторе src такие интерфейсы: Tunnel1, Tunnel4.
А на маршрутизаторе dest такие: Tunnel2, Tunnel3, Tunnel8.
Первый свободный номер одинаковый для двух маршрутизаторов будет 9.
И надо будет настроить интерфейс Tunnel 9.

Для этого задания нет теста!
'''

def send_commands(device, configs):

    try:
        with ConnectHandler(**device) as ssh:
            ssh.enable()
            result = ssh.send_config_set(configs)
            return result

    except() as err:
        print("Invalid username or password")


def configure_vpn(src_device_params,
                  dst_device_params,
                  src_template,
                  dst_template,
                  vpn_data_dict):

    template_dir, template_file1 = os.path.split(src_template)
    template_dir, template_file2 = os.path.split(dst_template)

    env = Environment(loader=FileSystemLoader(template_dir))

    temp1 = env.get_template(template_file1)
    temp2 = env.get_template(template_file2)

    vpn1_conf = temp1.render(vpn_data_dict).split('\n')
    vpn2_conf = temp2.render(vpn_data_dict).split('\n')

    output1 = send_commands(src_device_params, vpn1_conf)
    output2 = send_commands(dst_device_params, vpn2_conf)

    return output1, output2


if __name__ in "__main__":
    data = {
        'tun_num': 10,
        'wan_ip_1': '192.168.100.1',
        'wan_ip_2': '192.168.100.2',
        'tun_ip_1': '10.0.1.1 255.255.255.252',
        'tun_ip_2': '10.0.1.2 255.255.255.252'
    }
    template1 = 'templates/gre_ipsec_vpn_1.txt'
    template2 = 'templates/gre_ipsec_vpn_2.txt'

    with open('devices.yaml') as f:
        r1, r2 = yaml.safe_load(f)

    output1, output2 = configure_vpn(r1, r2, template1, template2, data)
    print(output1)
    print("-" * 65)
    print(output2)
