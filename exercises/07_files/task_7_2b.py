# -*- coding: utf-8 -*-
from sys import argv

'''
Задание 7.2b

Дополнить скрипт из задания 7.2a:
* вместо вывода на стандартный поток вывода,
  скрипт должен записать полученные строки в файл config_sw1_cleared.txt

При этом, должны быть отфильтрованы строки, которые содержатся в списке ignore.
Строки, которые начинаются на '!' отфильтровывать не нужно.

Ограничение: Все задания надо выполнять используя только пройденные темы.

'''

ignore = ['duplex', 'alias', 'Current configuration']

with open(argv[1]) as src, open('config_sw1_cleared.txt', 'w') as dst:
    for line in src:
        word_in_line = False
        for word in ignore:
            if word in line:
                word_in_line = True
                break

        if not word_in_line:
            dst.write(line)

