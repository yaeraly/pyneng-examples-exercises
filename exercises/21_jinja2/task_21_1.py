# -*- coding: utf-8 -*-
import yaml
import os
from sys import argv
from jinja2 import Environment, FileSystemLoader

'''
Задание 21.1

Создать функцию generate_config.

Параметры функции:
* template - путь к файлу с шаблоном (например, "templates/for.txt")
* data_dict - словарь со значениями, которые надо подставить в шаблон

Функция должна возвращать строку с конфигурацией, которая была сгенерирована.

Проверить работу функции на шаблоне templates/for.txt и данных из файла data_files/for.yml.

'''


def generate_config(template, data_dict):
    template_dir, template_file = os.path.split(template)

    env = Environment(loader=FileSystemLoader(template_dir),
                      trim_blocks=True,
                      lstrip_blocks=True)
    template = env.get_template(template_file)

    return template.render(data_dict)


if __name__ in "__main__":
    with open(argv[2]) as f:
        data = yaml.safe_load(f)

    print(generate_config(argv[1], data))
