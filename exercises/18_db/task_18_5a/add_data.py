# -*- coding: utf-8 -*-
import os
import yaml
import sqlite3
import re
from pprint import pprint
from datetime import datetime, timedelta

now = datetime.today().replace(microsecond=0)
week_ago = now - timedelta(days=7)

dflt_db_name = 'dhcp_snooping.db'
filesname = ['sw1_dhcp_snooping.txt', 'sw2_dhcp_snooping.txt', 'sw3_dhcp_snooping.txt']


def create_connection(db_name):

    return sqlite3.connect(db_name)


def add(db_name, filesname):
    connection = create_connection(db_name)

    try:
        with connection:
            connection.execute('UPDATE dhcp SET active=0')
    except:
        print('An error occured while updating data in the "dhcp" table')


    print('Updating table "dhcp" with new data...')
    for dhcp in parse_files(filesname):
        try:
            with connection:
                query = """UPDATE dhcp SET
                                   ip='{1}',
                                   vlan='{2}',
                                   interface='{3}',
                                   switch='{4}',
                                   active='1',
                                   last_active=datetime('now')
                            WHERE mac='{0}'""".format(*dhcp)

                connection.executescript(query)
        except sqlite3.IntegrityError as e:
            print(f'An error occured while updating data in the "dhcp" table: {dhcp}', e)

    try:
        with connection:
            query = f"DELETE FROM dhcp where last_active < '{week_ago}'"
            connection.execute(query)
    except:
         print('An error occured while deleting data')

    connection.close()


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
        add(dflt_db_name, filesname)

