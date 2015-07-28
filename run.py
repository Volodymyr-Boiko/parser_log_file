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


def create_table(cur, **kwargs):
    """Creates a new table
    Args:
        kwargs: columns' name and columns' type.
    """
    cur.create_table(**kwargs)


def del_table(cur):
    """Drops data-table"""
    cur.drop_table()


def insert_data(cur, file_name, key1, key2, uniq='data', arch=False, *cols):
    """Inserts data into the table
    Args:
        cur: cursor;
        file_name: name of a log file;
        key1: first key;
        key2: second key
        uniq: switcher;
        cols: columns' name.
    """
    if uniq == 'data':
        _insert_data_helper(cur, file_name, key1, key2, arch, *cols)
    elif uniq == 'calc':
        _insert_calc_helper(cur, file_name, key1, key2, arch, *cols)


def get_data(cur, val_id, *columns):
    """Gets the data from the table by value of 'id'
    Args:
        cur: cursor;
        val_id: value of 'id';
        cols: switcher;
        columns: columns' name.
    Return: Value of each column which taken by 'id' value.
    """
    return cur.get_data_by_id(val_id, *columns)


def update_data(cur, val_id, **kwargs):
    """Updates data_table
    Args:
        cur: cursor;
        id_vad: 'id' value
        kwargs: names of the columns and their values
    """
    cur.update_data_by_id(val_id, **kwargs)


def delete_data(cur, **kwargs):
    """Deletes data from a table
    Args:
        kwargs: column name and column value
    """
    cur.del_data(**kwargs)


def _insert_data_helper(cur, file_name, key1, key2, arch=False, *cols):
    """Inserts data into the table
    Args:
        cur: cursor;
        file_name: name of a log file;
        key1: first key;
        key2: second key
        cols: columns' name.
    """
    lst = []
    val = ['val1', 'val2']
    for item in get_uniq_data(file_name, key1, key2, arch):
        test_dic = dict(zip(val, item.values()))
        lst.append(test_dic)
    for value in lst:
        cur.insert_into_table(*cols, **value)


def _insert_calc_helper(cur, file_name, key1, key2, arch=False, *cols):
    """Inserts data into the table
    Args:
        cur: cursor;
        file_name: name of a log file;
        key1: first key;
        key2: second key
        cols: columns' name.
    """
    vals = {}
    test_dict = calc_uniq_data(file_name, key1, key2, arch)
    vals['val1'] = test_dict.get(key1, '')
    vals['val2'] = test_dict.get(key2, '')
    cur.insert_into_table(*cols, **vals)


if __name__ == '__main__':
    cur = get_model('vboiko', 'postgres', 'data_table')
    del_table(cur)
    create_table(cur, sites='VARCHAR', users='VARCHAR')
    insert_data(cur, 'access.log', 'user', 'indent', 'data', False, 'users',
                'sites')
    # update_data(cur, 1, sites=2, users='2')
    # delete_data(cur, sites="2", users='2')
    # print get_data(cur, 3, 'id', 'sites', 'users')
    # print get_data(cur, 4, 'id', 'sites', 'users')

    # cur_2 = get_model('vboiko', 'postgres', 'result')
    # create_table(cur_2, 'uniq_users', 'VARCHAR', 'uniq_sites', 'VARCHAR')
    # insert_data(cur_2, 'access.log', 'user', 'indent', 'calc', 'uniq_users', 'uniq_sites')
    # print get_data(cur_2, 1, True, 'uniq_users', 'uniq_sites')
