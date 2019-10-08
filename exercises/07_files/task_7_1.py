# -*- coding: utf-8 -*-
'''
Задание 7.1

Аналогично заданию 4.6 обработать строки из файла ospf.txt
и вывести информацию по каждой в таком виде:
Protocol:              OSPF
Prefix:                10.0.24.0/24
AD/Metric:             110/41
Next-Hop:              10.0.13.3
Last update:           3d18h
Outbound Interface:    FastEthernet0/0

Ограничение: Все задания надо выполнять используя только пройденные темы.

'''
show = """
Protocol:              {}SPF
Prefix:                {}
AD/Metric:             {}
Next-Hop:              {}
Last update:           {}
Outbound Interface:    {}
"""

with open('ospf.txt') as f:
    for line in f:
        pro, pre, ad, via, n_hop, l_up, intf = line.split()
        print(show.format(pro, pre, ad.strip('[]'), n_hop.rstrip(','), l_up.rstrip(','), intf))

