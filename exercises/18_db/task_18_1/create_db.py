# -*- coding: utf-8 -*-
import os
import sqlite3


# Default values:
DFLT_DB_NAME = 'dhcp_snooping.db'
DFLT_DB_SCHEMA = 'dhcp_snooping_schema.sql'


def create_database(db_name, db_schema):
    """
    This function first creates a connection object that
    represents the database.

    Then creates new tables where data will be stored.
    """
    print('Creating a database...')
    connection = sqlite3.connect(db_name)

    sql_script = read_file(db_schema)

    connection.executescript(sql_script)


def read_file(file_name):
    """
    This function reads the content of the file
    and returns the whole text as one string
    """
    with open(file_name) as file:
        file_content = file.read()

    return file_content


if __name__ in "__main__":

    if os.path.isfile(DFLT_DB_NAME):
        print('A database already exists')
    else:
        create_database(DFLT_DB_NAME, DFLT_DB_SCHEMA)

