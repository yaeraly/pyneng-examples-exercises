#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3
import os
import yaml
import re
from tabulate import tabulate


def create_connection(db_name):

    connection = sqlite3.connect(db_name)

    return connection


def create_db(db_name, db_schema):

    if os.path.isfile(db_name):
        print('A database already exists')
    else:
        print('Creating a database...')
        connection = create_connection(db_name)

        sql_script = read_file(db_schema)

        connection.executescript(sql_script)

def read_file(file_name):

    with open(file_name) as file:
        file_content = file.read()

    return file_content


def add_data_switches(db_name, filename):

    connection = create_connection(db_name)

    data1 = parse_yml_file(str(filename[0]))
    query1 = 'INSERT INTO switches VALUES(?, ?)'
    print('Adding data to table "switches"...')
    for row in data1:
        try:
            with connection:
                connection.execute(query1, row)

        except(sqlite3.IntegrityError) as e:
            print(f'An error occured:({e}) while adding {row} to "switches" table')


def add_data(db_name, filesname):

    connection = create_connection(db_name)
    print('Adding data to table "dhcp"...')
    data2 = parse_files(filesname)
    query2 = 'INSERT INTO dhcp VALUES(?, ?, ?, ?, ?, ?)'

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
                    row = (mac, ip, vlan, intf, hostname, 1)
                    list_of_tuples.append(row)

    return list_of_tuples


def get_data(db_name, key, value):
    connection = create_connection(db_name)

    query = f'SELECT * FROM dhcp WHERE {key} = "{value}"'
    try:
        with connection:
            result = connection.execute(query)
            print(tabulate(list(result)))
    except(sqlite3.OperationalError):
        print("Current parameter does not exist.")
        print('Available parameters: mac, ip, vlan, interface, switch')


def get_all_data(db_name):
    connection = create_connection(db_name)

    query = 'SELECT * FROM dhcp'
    result = connection.execute(query)
    print(tabulate(list(result)))
