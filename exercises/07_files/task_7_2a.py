# -*- coding: utf-8 -*-
from sys import argv

'''
Задание 7.2a

Сделать копию скрипта задания 7.2.

Дополнить скрипт:
  Скрипт не должен выводить команды, в которых содержатся слова,
  которые указаны в списке ignore.

Ограничение: Все задания надо выполнять используя только пройденные темы.

'''

ignore = ['duplex', 'alias', 'Current configuration']

with open(argv[1]) as f:
    for line in f:
        if not line.startswith('!'):
            word_in_line = False
            for word in ignore:
                if word in line:
                    word_in_line = True
                    break

            if not word_in_line:
                print(line.rstrip())

