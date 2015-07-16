#! /usr/bin/python
"""Makes a records in a table"""


from database import Model

from parser import calc_uniq_data
from parser import get_uniq_data


def get_model(user, database, table_name):
    """Open a cursor to perform database operations
    Args:
        user: username;
        database: name of a database;
        table_name: name of a table.
    Return: Cursor to perform database operations
    """
    cur = Model(user, database, table_name)
    cur.connect()
    cur.get_cursor()
    return cur


def create_table(cur, *args):
    """Creates a new table
    Args:
        *args: columns' name and columns' type.
    """
    cur.create_table(*args)


def insert_data(cur, file_name, key1, key2, uniq='data', *cols):
    """Inserts data into the table
    Args:
        cur: cursor;
        file_name: name of a log file;
        key1: first key;
        key2: second key
        uniq: switcher;
        cols: columns' name.
    """
    vals = {}
    if uniq == 'data':
        for item in get_uniq_data(file_name, key1, key2):
            vals['val1'] = item.get(key1, '')
            vals['val2'] = item.get(key2, '')
            cur.insert_into_table(*cols, **vals)
    elif uniq == 'calc':
        test_dict = calc_uniq_data(file_name, key1, key2)
        vals['val1'] = test_dict.get(key1, '')
        vals['val2'] = test_dict.get(key2, '')
        cur.insert_into_table(*cols, **vals)


def get_data(cur, val_id, cols=True, *columns):
    """Gets the data from the table by value of 'id'
    Args:
        cur: cursor;
        val_id: value of 'id';
        cols: switcher;
        columns: columns' name.
    Return: Value of each column which taken by 'id' value.
    """
    return cur.get_data_by_id(val_id, cols, *columns)


if __name__ == '__main__':
    cur = get_model('vboiko', 'postgres', 'data')
    create_table(cur, 'sites', 'VARCHAR', 'users', 'VARCHAR')
    insert_data(cur, 'access.log', 'user', 'indent', 'data', 'sites', 'users')
    print get_data(cur, 2, True, 'sites', 'users')

    cur_2 = get_model('vboiko', 'postgres', 'result')
    create_table(cur_2, 'uniq_users', 'VARCHAR', 'uniq_sites', 'VARCHAR')
    insert_data(cur_2, 'access.log', 'user', 'indent', 'calc', 'uniq_users', 'uniq_sites')
    print get_data(cur_2, 1, True, 'uniq_users', 'uniq_sites')
