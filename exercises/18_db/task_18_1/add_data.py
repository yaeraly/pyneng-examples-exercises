# -*- coding: utf-8 -*-
import os
import yaml
import sqlite3
import re
from pprint import pprint

dflt_db_name = 'dhcp_snooping.db'
filesname = ['sw1_dhcp_snooping.txt', 'sw2_dhcp_snooping.txt', 'sw3_dhcp_snooping.txt']


def create_connection(db_name):

    return sqlite3.connect(db_name)


def add(db_name, filename, filesname):
    connection = create_connection(db_name)

    data1 = parse_yml_file(filename)
    query1 = 'INSERT INTO switches VALUES(?, ?)'
    print('Adding data to table "switches"...')
    for row in data1:
        try:
            with connection:
                connection.execute(query1, row)

        except(sqlite3.IntegrityError) as e:
            print(f'An error occured:({e}) while adding {row} to "switches" table')

    print('Adding data to table "dhcp"...')
    data2 = parse_files(filesname)
    query2 = 'INSERT INTO dhcp VALUES(?, ?, ?, ?, ?)'

    for row in data2:
        try:
            with connection:
                connection.execute(query2, row)
        except(sqlite3.IntegrityError) as e:
            print(f'An error occured:({e}) while adding {row} to "dhcp" table')


def parse_yml_file(file_name):
    """
    This function returns list of tuples;
    """
    with open(file_name) as file:
        data = yaml.safe_load(file)  # returns python dictionary from yaml file

    list_of_tuples = [(h_name, loc) for v in data.values() for h_name, loc in v.items()]

    return list_of_tuples


def parse_files(file_names):
    """
    This function parses files and
    returns list of tuples;
    """
    list_of_tuples = []

    regex = re.compile('(?P<mac>\S+) +'
                       '(?P<ip>\S+) +\S+ +\S+ +'
                       '(?P<vlan>\d+) +'
                       '(?P<intf>\S+)')

    for file_name in file_names:
        hostname = re.match('(.*?)[_]', file_name).group(1)
        with open(file_name) as file:
            for line in file:
                match = regex.search(line)
                if match:
                    mac, ip, vlan, intf = match.groups()
                    row = (mac, ip, vlan, intf, hostname)
                    list_of_tuples.append(row)

    return list_of_tuples

if __name__ == '__main__':
    if not os.path.exists(dflt_db_name):
        print('A database does not exist. Create a DB using "create_db.py"')
    else:
        add(dflt_db_name, 'switches.yml', filesname)

