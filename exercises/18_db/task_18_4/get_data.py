import argparse
import sqlite3
from tabulate import tabulate

dflt_db_name = 'dhcp_snooping.db'
parser = argparse.ArgumentParser()
parser.add_argument('-db', dest='db_name', default=dflt_db_name,
                    help='db name')
parser.add_argument('key', nargs="?",
                    help="host key (parameter) to search")
parser.add_argument('value', nargs="?", help="value of key")
args = parser.parse_args()

def get(args):
    connection = sqlite3.connect(args.db_name)

    if args.key and args.value:
        try:
            with connection:
                print(f"Device info with parameters: {args.key} {args.value}")

                query = f'SELECT * FROM dhcp WHERE {args.key} = "{args.value}" and active="1"'
                result = list(connection.execute(query))
                if result:
                    print('\nActive fields:')
                    print(tabulate(result))

                query = f'SELECT * FROM dhcp WHERE {args.key} = "{args.value}" and active="0"'
                result = list(connection.execute(query))
                if result:
                    print('\nInactive fields:')
                    print(tabulate(result))

        except(sqlite3.OperationalError):
            print("Current parameter does not exist.")
            print('Available parameters: mac, ip, vlan, interface, switch')

    elif args.key or args.value:
        print('Please, give two or zero args')
    else:
        print('Table has these records:')

        query = "SELECT * FROM dhcp WHERE active='1'"
        result = list(connection.execute(query))
        if result:
            print('\nActive fields:')
            print(tabulate(result))

        query = "SELECT * FROM dhcp WHERE active='0'"
        result = list(connection.execute(query))
        if result:
            print('\nInactive fields:')
            print(tabulate(result))

get(args)

