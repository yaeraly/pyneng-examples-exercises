# -*- coding: utf-8 -*-
from draw_network_graph import draw_topology
from pprint import pprint
import yaml
'''
Задание 17.2b

Создать функцию transform_topology, которая преобразует топологию в формат подходящий для функции draw_topology.

Функция ожидает как аргумент имя файла в формате YAML, в котором хранится топология.

Функция должна считать данные из YAML файла, преобразовать их соответственно, чтобы функция возвращала словарь такого вида:
    {('R4', 'Fa 0/1'): ('R5', 'Fa 0/1'),
     ('R4', 'Fa 0/2'): ('R6', 'Fa 0/0')}

Функция transform_topology должна не только менять формат представления топологии, но и удалять дублирующиеся соединения (их лучше всего видно на схеме, которую генерирует draw_topology).

Проверить работу функции на файле topology.yaml. На основании полученного словаря надо сгенерировать изображение топологии с помощью функции draw_topology.
Не копировать код функции draw_topology.

Результат должен выглядеть так же, как схема в файле task_17_2b_topology.svg

При этом:
* Интерфейсы должны быть записаны с пробелом Fa 0/0
* Расположение устройств на схеме может быть другим
* Соединения должны соответствовать схеме
* На схеме не должно быть дублирующихся линков


> Для выполнения этого задания, должен быть установлен graphviz:
> apt-get install graphviz

> И модуль python для работы с graphviz:
> pip install graphviz

'''
def transform_topology(yaml_file_name):
    dict_from_yaml_file = {}
    connecting_device_dict = {}

    with open(yaml_file_name) as f:
        dict_from_yaml_file = yaml.safe_load(f)

    for l_device, values in dict_from_yaml_file.items():
         for l_intf, value in values.items():
             for r_device, r_intf in value.items():
                 key = tuple([l_device, l_intf])
                 value = tuple([r_device, r_intf])

                 if not key in connecting_device_dict.values():
                     connecting_device_dict[key] = {}
                     connecting_device_dict[key] = value

    return connecting_device_dict

draw_topology(transform_topology('topology.yaml'))

