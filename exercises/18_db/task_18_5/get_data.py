import argparse
import sqlite3
from tabulate import tabulate

parser = argparse.ArgumentParser()
parser.add_argument('field', nargs="?", help="A field name of the table")
parser.add_argument('record', nargs="?", help="A record in the table")
args = parser.parse_args()

def get_data(db_name):

    connection = sqlite3.connect(db_name)

    if args.field is None and args.record is None:

        print('Table has these records:')

        query = "SELECT * FROM dhcp where active='1'"
        result = list(connection.execute(query))
        if result:
            print('\nActive fields:')
            print(tabulate(result))

        query = "SELECT * FROM dhcp where active='0'"
        result = list(connection.execute(query))

        if result:
            print('\nInactive fields:')
            print(tabulate(result))

    else:
        try:
            with connection:

                query = 'SELECT * FROM dhcp WHERE {} = "{}" and active="1"'.format(args.field, args.record)
                result = list(connection.execute(query))

                print(f'Information about device with these parameters: {args.field} {args.record}')
                if result:
                    print('\nActive fields:')
                    print(tabulate(result))

                query = 'SELECT * FROM dhcp WHERE {} = "{}" and active="0"'.format(args.field, args.record)
                result = list(connection.execute(query))

                if result:
                    print('\nInactive fields:')
                    print(tabulate(result))

        except(sqlite3.OperationalError):
                print("Current parameter does not exist.")
                print('Available parameters: mac, ip, vlan, interface, switch')

get_data('dhcp_snooping.db')
