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


# def create_table(cur, col1, col2):
#     """Creates a new table
#     Args:
#         cur: cursor;
#         col1: first column's name;
#         col2: second column's name
#     """
#     cur.create_table(col1, col2)


def create_table(cur, *args):
    """Creates a new table
    Args:
        cur: cursor;
        col1: first column's name;
        col2: second column's name
    """
    cur.create_table(*args)


def insert_data(cur, col1, col2, file_name, key1, key2, uniq='data'):
    """Inserts data into the table
    Args:
        cur: cursor;
        col1: first column's name;
        col2: second column's name;
        file_name: name of a log file;
        key1: first key;
        key2: second key
    """
    if uniq == 'data':
        for item in get_uniq_data(file_name, key1, key2):
            val1 = item.get(key1, '')
            val2 = item.get(key2, '')
            cur.insert_into_table(col1, val1, col2, val2)
    elif uniq == 'calc':
        test_dict = calc_uniq_data(file_name, key1, key2)
        val1 = test_dict.get(key1, '')
        val2 = test_dict.get(key2, '')
        cur.insert_into_table(col1, val1, col2, val2)


def get_data(cur, val_id, col1, col2):
    """Gets the data from the table by value of 'id'
    Args:
        cur: cursor;
        val_id: value of 'id'.
    Return: Value of each column which taken by 'id' value.
    """
    return cur.get_data_by_id(val_id, col1, col2)


if __name__ == '__main__':
    cur = get_model('vboiko', 'postgres', 'boiko_1986_11129')
    create_table(cur, 'users', 'VARCHAR', 'sites', 'VARCHAR')
    # insert_data(cur, 'users', 'sites', 'access.log', 'user', 'indent')
    # print get_data(cur, 1, 'users', 'sites')

    # cur_2 = get_model('vboiko', 'postgres', 'boiko_29')
    # create_table(cur_2, 'uniq_users', 'uniq_sites')
    # insert_data(cur=cur_2, col1='uniq_users', col2='uniq_sites',
    #             file_name='access.log', key1='user', key2='indent', uniq='calc')
    # print get_data(cur_2, 6, 'uniq_users', 'uniq_sites')
